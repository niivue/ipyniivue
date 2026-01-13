// scripts/generate-gallery.js
const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");
const { chromium } = require("playwright"); // make sure playwright is installed
const util = require("node:util");

const NOTEBOOKS_DIR =
	process.env.NOTEBOOKS_DIR || path.resolve(process.cwd(), "notebooks");
const OUT_DIR = process.env.OUT_DIR || path.resolve(process.cwd(), "gallery");
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
	return fs.readdirSync(dir).filter((f) => f.toLowerCase().endsWith(".ipynb"));
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

	// Candidate names: base.html, base-executed.html, base_executed.html, executed_base.html
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

	// nothing found
	return null;
}

function generateExecutedHtml(nbPath, htmlOutPath) {
  // Use nbconvert to execute and export html. This may be slow for many notebooks.
  // Use spawnSync + arg array to avoid shell word-splitting when PYTHON path contains spaces.
  const pythonExec = process.env.PYTHON || "python3";
  const outputName = path.basename(htmlOutPath); // e.g. worldspace2.html
  const outputDir = path.dirname(htmlOutPath);

  const args = [
    "-m",
    "nbconvert",
    "--to",
    "html",
    "--execute",
    nbPath,
    "--output",
    outputName,
    "--output-dir",
    outputDir,
    "--ExecutePreprocessor.timeout=120",
  ];

  console.log("[nbconvert] running:", pythonExec, args.join(" "));
  const res = spawnSync(pythonExec, args, {
    stdio: "inherit",
    env: { ...process.env },
    shell: false, // important: do not run through a shell
  });

  if (res.error) {
    // e.g. ENOENT if pythonExec doesn't exist
    throw res.error;
  }
  if (res.status !== 0) {
    throw new Error(`nbconvert failed with exit code ${res.status}`);
  }
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

	// find last image/png in cell outputs
	let lastImageBase64 = null;
	for (const cell of nbJson.cells || []) {
		if (!cell.outputs) continue;
		for (const out of cell.outputs) {
			if (out.data?.["image/png"]) {
				// output may be array or string
				const data = out.data["image/png"];
				if (Array.isArray(data)) lastImageBase64 = data.join("");
				else lastImageBase64 = data;
			} else if (out.data?.["image/jpeg"]) {
				const data = out.data["image/jpeg"];
				if (Array.isArray(data)) lastImageBase64 = data.join("");
				else lastImageBase64 = data;
			} else if (
				out.text &&
				typeof out.text === "string" &&
				out.text.startsWith("data:image/png;base64,")
			) {
				lastImageBase64 = out.text.split(",")[1];
			}
		}
	}

	// attempt to locate an HTML corresponding to this notebook (may be null)
	let foundHtmlPath = tryFindHtmlForNotebook(nbPath);

	if (lastImageBase64) {
		// write PNG
		ensureDir(THUMBS_DIR);
		fs.writeFileSync(thumbPath, Buffer.from(lastImageBase64, "base64"));
		console.log(
			`[thumb] embedded image/png extracted -> ${path.relative(process.cwd(), thumbPath)}`,
		);

		// compute htmlRel if we previously found an HTML
		let htmlRel = null;
		if (foundHtmlPath && fs.existsSync(foundHtmlPath)) {
			htmlRel = path.relative(OUT_DIR, foundHtmlPath).split(path.sep).join("/");
		}

		return {
			name: nbFilename,
			thumbnail: path.relative(OUT_DIR, thumbPath).split(path.sep).join("/"),
			ok: true,
			htmlRel, // may be null
		};
	}

	// No embedded image. Try to find HTML with canvas
	let htmlPath = foundHtmlPath;
	if (!htmlPath) {
		// try to create an executed HTML in the OUT_DIR
		console.log(
			"[info] no pre-existing HTML found; attempting nbconvert to generate executed HTML (slow)",
		);
		const htmlOutPath = path.join(OUT_DIR, `${slug}.html`);
		try {
			generateExecutedHtml(nbPath, htmlOutPath);
			htmlPath = htmlOutPath;
		} catch (err) {
			console.warn("[warn] nbconvert failed:", err.message);
			return {
				name: nbFilename,
				ok: false,
				reason: "no image and nbconvert failed",
			};
		}
	}

	// Render HTML and screenshot last canvas
	try {
		ensureDir(THUMBS_DIR);
		const ok = await screenshotLastCanvasFromHtml(htmlPath, thumbPath);
		if (!ok) {
			console.warn("[warn] no <canvas> found in HTML:", htmlPath);
			return { name: nbFilename, ok: false, reason: "no canvas in HTML" };
		}
		console.log(
			`[thumb] canvas screenshot -> ${path.relative(process.cwd(), thumbPath)}`,
		);

		// htmlRel relative to OUT_DIR (so gallery/index.html can link to it)
		const htmlRel = path.relative(OUT_DIR, htmlPath).split(path.sep).join("/");

		return {
			name: nbFilename,
			thumbnail: path.relative(OUT_DIR, thumbPath).split(path.sep).join("/"),
			ok: true,
			htmlRel,
		};
	} catch (err) {
		console.warn("[warn] error rendering HTML/canvas:", err.message);
		return { name: nbFilename, ok: false, reason: err.message };
	}
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
			results.push({ name: nb, ok: false, reason: err.message });
		}
	}

	// Generate gallery HTML
	const items = results
		.filter((r) => r.ok && r.thumbnail)
		.map((r) => {
			// nbRel is still a fallback link to the notebook itself
			const nbRel = path
				.relative(OUT_DIR, path.join(NOTEBOOKS_DIR, r.name))
				.split(path.sep)
				.join("/");
			// prefer htmlRel (if present), otherwise fall back to notebook link
			const linkRel = r.htmlRel ? r.htmlRel : nbRel;
			const thumbRel = r.thumbnail.split(path.sep).join("/");
			return { name: r.name, linkRel, thumbRel };
		});

	const galleryHtml = `<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Notebook Gallery</title>
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; padding: 24px; }
    h1 { margin-bottom: 12px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
    .card { border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); overflow: hidden; background: #fff; text-align: center; padding: 8px; }
    .card img { display: block; width: 100%; height: 160px; object-fit: cover; background: #eee; }
    .caption { font-size: 13px; padding: 8px 6px; color: #333; }
    a { color: inherit; text-decoration: none; }
    .meta { font-size: 12px; color: #666; margin-top: 4px; }
  </style>
</head>
<body>
  <h1>Notebook Gallery</h1>
  <p>Generated: ${new Date().toISOString()}</p>
  <div class="grid">
    ${items
			.map(
				(it) => `
      <div class="card">
        <a href="${it.linkRel}" title="${it.name}">
          <img src="${it.thumbRel}" alt="${it.name} thumbnail"/>
          <div class="caption">${it.name}</div>
        </a>
      </div>
    `,
			)
			.join("\n")}
  </div>
</body>
</html>
`;

	const galleryPath = path.join(OUT_DIR, "index.html");
	fs.writeFileSync(galleryPath, galleryHtml, "utf8");
	console.log("\n[done] gallery written to", galleryPath);
	console.log(
		`[summary] ${items.length} thumbnails created, ${results.length - items.length} notebooks skipped or failed.`,
	);
})();
