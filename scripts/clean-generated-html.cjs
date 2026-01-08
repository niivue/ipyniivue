#!/usr/bin/env node
// scripts/clean-generated-html.cjs
// Usage:
//   node scripts/clean-generated-html.cjs        # delete html, executed notebooks, thumbnails in OUT_DIR
//   OUT_DIR=tests-out/html node scripts/clean-generated-html.cjs
//   node scripts/clean-generated-html.cjs --dry-run

const { resolve, join } = require("node:path");
const {
	readdirSync,
	statSync,
	unlinkSync,
	rmdirSync,
	existsSync,
} = require("node:fs");

const OUT_DIR = process.env.OUT_DIR || "tests-out/html";
const DRY_RUN =
	process.argv.includes("--dry-run") || process.env.DRY_RUN === "1";

function isHtmlFile(name) {
	return /\.html$/i.test(name);
}
function isExecutedNotebook(name) {
	return /^executed_.*\.ipynb$/i.test(name) || /-executed\.ipynb$/i.test(name);
}
function isThumbnail(name) {
	return /\.(png|jpg|jpeg|webp)$/i.test(name);
}

function walkDir(dir) {
	const items = readdirSync(dir, { withFileTypes: true });
	const files = [];
	for (const it of items) {
		const full = join(dir, it.name);
		if (it.isDirectory()) {
			files.push(...walkDir(full));
		} else {
			files.push(full);
		}
	}
	return files;
}

(function main() {
	const outAbs = resolve(process.cwd(), OUT_DIR);
	if (!existsSync(outAbs)) {
		console.log(
			`[clean-generated-html] nothing to do — OUT_DIR does not exist: ${outAbs}`,
		);
		process.exit(0);
	}

	console.log(`[clean-generated-html] OUT_DIR = ${outAbs}`);
	if (DRY_RUN)
		console.log(
			"[clean-generated-html] running in dry-run mode (no files will be deleted)",
		);

	const allFiles = walkDir(outAbs);
	const toDelete = allFiles.filter((f) => {
		const name = f.split(/[\\/]/).pop();
		return isHtmlFile(name) || isExecutedNotebook(name) || isThumbnail(name);
	});

	if (toDelete.length === 0) {
		console.log(
			"[clean-generated-html] no generated html/executed notebooks/thumbnails found to delete.",
		);
		process.exit(0);
	}

	console.log(
		`[clean-generated-html] found ${toDelete.length} items to remove:`,
	);
	for (const p of toDelete) {
		console.log("  -", p);
	}

	if (DRY_RUN) {
		console.log("[clean-generated-html] dry-run complete; no files deleted.");
		process.exit(0);
	}

	// Delete files
	for (const f of toDelete) {
		try {
			unlinkSync(f);
			console.log(`[clean-generated-html] deleted ${f}`);
		} catch (err) {
			console.error(
				`[clean-generated-html] failed to delete ${f}:`,
				err?.message ? err.message : err,
			);
		}
	}

	// Optionally remove empty directories under OUT_DIR
	// Walk directories bottom-up and remove those that are empty
	const allDirs = Array.from(new Set(allFiles.map((p) => join(p, ".."))));
	// sort longest paths (deepest) first
	allDirs.sort((a, b) => b.length - a.length);
	for (const d of allDirs) {
		try {
			const entries = readdirSync(d);
			if (entries.length === 0) {
				rmdirSync(d);
				console.log(`[clean-generated-html] removed empty dir ${d}`);
			}
		} catch (err) {
			// ignore
		}
	}

	console.log("[clean-generated-html] done.");
})();
