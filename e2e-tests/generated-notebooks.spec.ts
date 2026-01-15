import { existsSync, readdirSync, statSync } from "node:fs";
import { basename, relative, resolve, sep } from "node:path";
import { expect, test } from "@playwright/test";

const HTML_DIR = resolve(process.cwd(), "tests-out/html");
const HTML_EXT = ".html";

/** static skip list (relative path or basename) */
const SKIPPED_NOTEBOOKS = new Set<string>(["example_sideview.html"]);

function normalizeRelPath(p: string) {
	return p.split(/\\/g).join("/").replace(/^\.\//, "");
}

function findHtmlFiles(dir: string): string[] {
	if (!existsSync(dir)) return [];
	const entries = readdirSync(dir);
	let files: string[] = [];
	for (const e of entries) {
		const full = resolve(dir, e);
		const st = statSync(full);
		if (st.isDirectory()) files = files.concat(findHtmlFiles(full));
		else if (st.isFile() && full.endsWith(HTML_EXT)) files.push(full);
	}
	return files;
}

function makeNames(filePath: string) {
	const rel = normalizeRelPath(relative(HTML_DIR, filePath));
	const testName = rel;
	const screenshotBase = rel.split("/").join("-").replace(/\./g, "-");
	const screenshotName = `${screenshotBase}-canvas.png`;
	return { testName, screenshotName, rel };
}

/**
 * Defensive generator: define either a skipped test (with an explicit skip reason)
 * or the real test. Also print collection-time debug info for confirmation.
 */
test.describe("ipyniivue static HTML (e2e) — generated from examples", () => {
	if (!existsSync(HTML_DIR)) {
		console.log(`[prepare-e2e] HTML_DIR missing: ${HTML_DIR}`);
		test.skip(true, `Missing generated HTML directory: ${HTML_DIR}`);
		return;
	}

	const htmlFiles = findHtmlFiles(HTML_DIR);
	console.log(
		`[prepare-e2e] Found ${htmlFiles.length} html files under ${HTML_DIR}`,
	);

	for (const htmlFile of htmlFiles) {
		const { testName, screenshotName, rel } = makeNames(htmlFile);
		const base = basename(rel);

		const title = `renders ${testName} — canvas has WebGL and matches snapshot`;

		// define the real test (only when not skipped)
		test(title, async ({ page }) => {
			const shouldSkip =
				SKIPPED_NOTEBOOKS.has(rel) || SKIPPED_NOTEBOOKS.has(base);

			// debug summary visible at collection time
			console.log(`[prepare-e2e] define: ${rel}  shouldSkip=${shouldSkip}`);
			if (shouldSkip) test.skip(shouldSkip, `${testName} in exclude list`);

			if (!existsSync(htmlFile)) {
				throw new Error(`Missing generated HTML: ${htmlFile}`);
			}

			const url = `file://${htmlFile}`;
			await page.goto(url, { waitUntil: "load" });

			const canvas = page.locator("canvas").first();
			await expect(canvas).toBeVisible({ timeout: 60_000 });

			const hasGL = await canvas.evaluate(
				(c: HTMLCanvasElement) =>
					!!(c.getContext("webgl2") || c.getContext("webgl")),
			);
			expect(hasGL).toBe(true);

			await page.waitForTimeout(500);

			await expect(canvas).toHaveScreenshot(screenshotName, {
				threshold: 0.2,
				maxDiffPixelRatio: 0.01,
			});
		});
	}
});
