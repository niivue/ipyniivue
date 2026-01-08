import { test, expect } from '@playwright/test';
import { resolve } from 'node:path';
import { existsSync } from 'node:fs';

test.describe('ipyniivue static HTML (e2e)', () => {
  const HTML_DIR = resolve(process.cwd(), 'tests-out/html');
  const HTML_FILE = resolve(HTML_DIR, 'basic_multiplanar.html');

  test('renders widget, canvas has WebGL, and matches snapshot', async ({ page }) => {
    if (!existsSync(HTML_FILE)) {
      throw new Error(`Missing generated HTML: ${HTML_FILE}`);
    }

    const url = `file://${HTML_FILE}`;
    await page.goto(url, { waitUntil: 'networkidle' });

    const canvas = page.locator('canvas').first();
    await expect(canvas).toBeVisible({ timeout: 60_000 });

    // Verify WebGL context exists
    const hasGL = await canvas.evaluate((c: HTMLCanvasElement) =>
      !!(c.getContext('webgl2') || c.getContext('webgl'))
    );
    expect(hasGL).toBe(true);

    // Give the renderer a moment to settle (important for deterministic snapshots)
    await page.waitForTimeout(500);

    // 🔒 Snapshot test of the canvas
    await expect(canvas).toHaveScreenshot('basic_multiplanar-canvas.png', {
    threshold: 0.2,
    maxDiffPixelRatio: 0.01,
    });

  });
});
