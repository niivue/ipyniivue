// scripts/generate-notebook-gallery.cjs
// Node script to create thumbnails from notebooks and produce gallery-like index.html
//
// Usage:
//   node scripts/generate-notebook-gallery.cjs
//
// Options via environment variables:
//   NOTEBOOKS_DIR  (default: ./notebooks)
//   OUT_DIR        (default: ./gallery)
//   PYTHON         (default: python3) - used only if nbconvert is needed

const fs = require("node:fs");
const path = require("node:path");
const { execSync } = require("node:child_process");
const { chromium } = require("playwright"); // make sure playwright is installed

const NOTEBOOKS_DIR =
	process.env.NOTEBOOKS_DIR || path.resolve(process.cwd(), "notebooks");
const OUT_DIR = process.env.OUT_DIR || path.resolve(process.cwd(), "examples");
const THUMBS_DIR = path.join(OUT_DIR, "thumbnails");
const PYTHON = process.env.PYTHON || "python3";

// Helpers
function slugify(name) {
	return name
		.replace(/[^a-zA-Z0-9-_\.]/g, "-")
		.replace(/-+/g, "-")
		.replace(/(^-|-$)/g, "");
}
function ensureDir(dir) {
	if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}
function listNotebooks(dir) {
	if (!fs.existsSync(dir)) return [];
	return fs
		.readdirSync(dir)
		.filter((f) => f.toLowerCase().endsWith(".ipynb"))
		.sort();
}

async function screenshotLastCanvasFromHtml(htmlPath, outPngPath) {
	const fileUrl = `file://${path.resolve(htmlPath)}`;
	const browser = await chromium.launch({ args: ["--no-sandbox"] });
	try {
		const page = await browser.newPage({
			viewport: { width: 1200, height: 800 },
		});
		await page.goto(fileUrl, { waitUntil: "networkidle" });
		// wait briefly for client-side canvas drawing
		await page.waitForTimeout(500);

		const canvases = await page.$$("canvas");
		if (!canvases || canvases.length === 0) {
			await page.close();
			return false;
		}
		const last = canvases[canvases.length - 1];
		// Ensure the canvas is visible / scrolled into view
		await last.scrollIntoViewIfNeeded();
		// screenshot element
		await last.screenshot({ path: outPngPath });
		await page.close();
		return true;
	} finally {
		await browser.close();
	}
}

function tryFindHtmlForNotebook(nbPath) {
	const dir = path.dirname(nbPath);
	const base = path.basename(nbPath, ".ipynb");

	const candidates = [
		path.join(dir, `${base}.html`),
		path.join(dir, `${base}-executed.html`),
		path.join(dir, `${base}_executed.html`),
		path.join(dir, `executed_${base}.html`),
		path.join(dir, `${base}-output.html`),
	];
	for (const c of candidates) if (fs.existsSync(c)) return c;
	// also check OUT_DIR for matches
	const outCandidate = path.join(OUT_DIR, `${base}.html`);
	if (fs.existsSync(outCandidate)) return outCandidate;

	return null;
}

function generateExecutedHtml(nbPath, htmlOutPath) {
	const cmd = `${PYTHON} -m nbconvert --to html --execute "${nbPath}" --output "${path.basename(
		htmlOutPath,
	)}" --output-dir "${path.dirname(htmlOutPath)}" --ExecutePreprocessor.timeout=120`;
	console.log("[nbconvert] running:", cmd);
	execSync(cmd, { stdio: "inherit", env: { ...process.env } });
}

async function processNotebook(nbFilename) {
	const nbPath = path.join(NOTEBOOKS_DIR, nbFilename);
	const base = path.basename(nbFilename, ".ipynb");
	const slug = slugify(base);
	const thumbPath = path.join(THUMBS_DIR, `${slug}.png`);

	console.log(`\n[processing] ${nbFilename}`);

	// read notebook JSON
	let nbJson;
	try {
		nbJson = JSON.parse(fs.readFileSync(nbPath, "utf8"));
	} catch (err) {
		console.warn(`[warn] cannot parse notebook ${nbPath}:`, err.message);
		return { name: nbFilename, ok: false };
	}

	// find last image/png or jpeg in cell outputs
	let lastImageBase64 = null;
	for (const cell of nbJson.cells || []) {
		if (!cell.outputs) continue;
		for (const out of cell.outputs) {
			if (out.data?.["image/png"]) {
				const data = out.data["image/png"];
				lastImageBase64 = Array.isArray(data) ? data.join("") : data;
			} else if (out.data?.["image/jpeg"]) {
				const data = out.data["image/jpeg"];
				lastImageBase64 = Array.isArray(data) ? data.join("") : data;
			} else if (
				out.text &&
				typeof out.text === "string" &&
				out.text.startsWith("data:image/png;base64,")
			) {
				lastImageBase64 = out.text.split(",")[1];
			}
		}
	}

	ensureDir(THUMBS_DIR);

	if (lastImageBase64) {
		// write PNG
		fs.writeFileSync(thumbPath, Buffer.from(lastImageBase64, "base64"));
		console.log(
			`[thumb] embedded image/png extracted -> ${path.relative(process.cwd(), thumbPath)}`,
		);
		return {
			name: nbFilename,
			thumbnail: path.relative(OUT_DIR, thumbPath).split(path.sep).join("/"),
			ok: true,
		};
	}

	// No embedded image. Try to find HTML with canvas (for screenshot)
	let htmlPath = tryFindHtmlForNotebook(nbPath);
	if (!htmlPath) {
		// try to create an executed HTML in the OUT_DIR (this is optional/slow)
		console.log(
			"[info] no pre-existing HTML found; attempting nbconvert to generate executed HTML (slow)",
		);
		const htmlOutPath = path.join(OUT_DIR, `${slug}.html`);
		try {
			generateExecutedHtml(nbPath, htmlOutPath);
			htmlPath = htmlOutPath;
		} catch (err) {
			console.warn("[warn] nbconvert failed:", err.message);
			// we don't fail outright — just mark as no thumbnail and continue
			return { name: nbFilename, ok: true, thumbnail: null };
		}
	}

	// Render HTML and screenshot last canvas
	try {
		const ok = await screenshotLastCanvasFromHtml(htmlPath, thumbPath);
		if (!ok) {
			console.warn("[warn] no <canvas> found in HTML:", htmlPath);
			return { name: nbFilename, ok: true, thumbnail: null };
		}
		console.log(
			`[thumb] canvas screenshot -> ${path.relative(process.cwd(), thumbPath)}`,
		);
		return {
			name: nbFilename,
			thumbnail: path.relative(OUT_DIR, thumbPath).split(path.sep).join("/"),
			ok: true,
		};
	} catch (err) {
		console.warn("[warn] error rendering HTML/canvas:", err.message);
		return { name: nbFilename, ok: true, thumbnail: null };
	}
}

function makeIndexHtmlForNotebooks(items) {
	// items: [{ name, linkRel, thumbRel }]
	return `<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Notebooks</title>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; padding: 24px; background:#f6f7fb; color:#111;}
    h1 { margin-bottom: 6px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 18px; }
    .card { border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); overflow: hidden; background: #fff; text-align: center; padding: 8px; }
    .card img { display: block; width: 100%; height: 160px; object-fit: cover; background: #eee; }
    .caption { font-size: 13px; padding: 8px 6px; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    a { color: inherit; text-decoration: none; }
    .placeholder { width:100%; height:160px; display:flex; align-items:center; justify-content:center; background:#e9edf6; color:#6b7280; font-size:14px; }
    code { background:#fff; padding:2px 6px; border-radius:4px; }
  </style>
</head>
<body>
  <h1>Notebooks</h1>
  <p>Browse raw notebooks (click to download/open).</p>
  <div class="grid">
    ${items
			.map(
				(it) => `
      <div class="card">
        <a href="${it.linkRel}" title="${it.name}">
          ${it.thumbRel ? `<img src="${it.thumbRel}" alt="${it.name} thumbnail"/>` : `<div class="placeholder">No thumbnail</div>`}
          <div class="caption">${it.name}</div>
        </a>
      </div>
    `,
			)
			.join("\n")}
  </div>
</body>
</html>`;
}

(async () => {
	ensureDir(OUT_DIR);
	ensureDir(THUMBS_DIR);

	const notebooks = listNotebooks(NOTEBOOKS_DIR);
	if (notebooks.length === 0) {
		console.error("[error] no notebooks found in", NOTEBOOKS_DIR);
		process.exit(1);
	}

	const results = [];
	for (const nb of notebooks) {
		try {
			const res = await processNotebook(nb);
			results.push(res);
		} catch (err) {
			console.error("[error] failed to process", nb, err);
			results.push({ name: nb, ok: false, thumbnail: null });
		}
	}

	// Prepare items for the examples/index.html (links to .ipynb files)
	const items = results.map((r) => {
		const nbAbs = path.join(NOTEBOOKS_DIR, r.name);
		// link relative to the NOTEBOOKS_DIR (index.html will be placed in NOTEBOOKS_DIR)
		const linkRel =
			path.relative(NOTEBOOKS_DIR, nbAbs).split(path.sep).join("/") || r.name;
		const thumbRel = r.thumbnail
			? path
					.relative(NOTEBOOKS_DIR, path.join(OUT_DIR, r.thumbnail))
					.split(path.sep)
					.join("/")
			: null;
		return { name: r.name, linkRel, thumbRel };
	});

	// write index.html under NOTEBOOKS_DIR (so /examples/index.html links to /examples/<notebook>.ipynb)
	const notebooksIndexPath = path.join(NOTEBOOKS_DIR, "index.html");
	fs.writeFileSync(
		notebooksIndexPath,
		makeIndexHtmlForNotebooks(items),
		"utf8",
	);
	console.log("\n[done] notebooks index written to", notebooksIndexPath);
	console.log(
		`[summary] ${items.length} entries listed, thumbnails in ${path.relative(process.cwd(), THUMBS_DIR)}`,
	);
})();
