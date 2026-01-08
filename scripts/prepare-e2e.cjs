#!/usr/bin/env node
// scripts/prepare-e2e.cjs
//
// Prepare static HTML for E2E tests by executing notebooks and exporting HTML.
// Uses scripts/exec-notebook.cjs for the heavy lifting.
//
// Usage: node scripts/prepare-e2e.cjs
// Environment:
//   NOTEBOOKS_DIR  (default: examples)
//   OUT_DIR        (default: tests-out/html)
//   PYTHON         (optional, forwarded to exec-notebook)
//   TIMEOUT        (ms timeout forwarded to exec-notebook, default 300000)
//   RETRY_ALLOW_ERRORS (if "0", don't retry with ALLOW_ERRORS; default "1")

const { spawnSync } = require('child_process');
const { resolve, basename, join } = require('path');
const { existsSync, mkdirSync, readdirSync, statSync } = require('fs');

const NOTEBOOKS_DIR = process.env.NOTEBOOKS_DIR || 'examples';
const OUT_DIR = process.env.OUT_DIR || 'tests-out/html';
const PYTHON = process.env.PYTHON || process.env.PYTHON_PATH || 'python3';
const TIMEOUT = process.env.TIMEOUT ? Number(process.env.TIMEOUT) : 300000;
const RETRY_ALLOW_ERRORS = process.env.RETRY_ALLOW_ERRORS === '0' ? false : true;

function listNotebooks(dir) {
  const abs = resolve(process.cwd(), dir);
  if (!existsSync(abs)) return [];
  return readdirSync(abs).filter(f => f.toLowerCase().endsWith('.ipynb')).map(f => join(dir, f));
}

function runExecNotebook(notebookPath, outDir, options = {}) {
  const nodeCmd = process.execPath; // node
  const scriptPath = join(__dirname, 'exec-notebook.cjs');
  const args = [scriptPath, '--notebook', notebookPath, '--outdir', outDir];
  if (options.htmlname) args.push('--htmlname', options.htmlname);
  if (options.python) args.push('--python', options.python);
  if (options.timeoutMs) args.push('--timeout', String(options.timeoutMs));

  // spawnSync node so we can capture stdout (exec-notebook prints JSON on success)
  const spawnEnv = { ...process.env, ...(options.extraEnv || {}) };

  console.log(`[prepare-e2e] running: ${nodeCmd} ${args.map(a => a.includes(' ') ? JSON.stringify(a) : a).join(' ')}`);
  const sp = spawnSync(nodeCmd, args, { env: spawnEnv, encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 });

  return {
    status: sp.status,
    signal: sp.signal,
    stdout: sp.stdout || '',
    stderr: sp.stderr || '',
    error: sp.error,
  };
}

(async function main() {
  try {
    const notebooks = listNotebooks(NOTEBOOKS_DIR);
    if (notebooks.length === 0) {
      console.error(`[prepare-e2e] No notebooks found in "${NOTEBOOKS_DIR}". Nothing to prepare.`);
      process.exit(1);
    }

    // ensure out dir exists
    const outAbs = resolve(process.cwd(), OUT_DIR);
    mkdirSync(outAbs, { recursive: true });
    console.log(`[prepare-e2e] will write HTML into ${outAbs}`);

    const summary = {
      total: notebooks.length,
      succeeded: [],
      failed: [],
    };

    for (const nbRel of notebooks) {
      const nbName = basename(nbRel);
      const expectedHtmlName = basename(nbRel, '.ipynb') + '.html';
      const expectedHtmlPath = join(outAbs, expectedHtmlName);

      console.log(`\n[e2e] processing ${nbRel} -> expect ${expectedHtmlPath}`);

      // Short-circuit: if expected HTML already exists and looks non-empty, skip execution
      try {
        if (existsSync(expectedHtmlPath)) {
          const s = statSync(expectedHtmlPath);
          if (s.size > 0) {
            console.log(`[e2e] ✔ skipping ${nbName} — existing HTML found at ${expectedHtmlPath}`);
            summary.succeeded.push({ notebook: nbRel, html: expectedHtmlPath });
            continue; // next notebook
          } else {
            console.log(`[e2e] found ${expectedHtmlPath} but file is empty; will re-generate`);
          }
        }
      } catch (err) {
        console.warn(`[e2e] warning checking existing HTML for ${nbName}:`, err && err.message ? err.message : String(err));
      }

      // First attempt: normal
      const res = runExecNotebook(nbRel, OUT_DIR, { python: PYTHON, timeoutMs: TIMEOUT });

      if (res.status === 0) {
        // parse stdout for JSON
        try {
          // exec-notebook prints a single JSON line on success
          const lastLine = (res.stdout || '').trim().split(/\r?\n/).filter(Boolean).slice(-1)[0] || '';
          const parsed = JSON.parse(lastLine);
          console.log(`[e2e] ✔ ${nbName} -> HTML: ${parsed.htmlPath}`);
          summary.succeeded.push({ notebook: nbRel, html: parsed.htmlPath });
          continue;
        } catch (err) {
          console.warn(`[e2e] Warning: ${nbName} exited 0 but output could not be parsed as JSON. stdout snippet:`);
          console.warn(res.stdout.slice(0, 2000));
          // treat as failure to be safe
        }
      } else {
        console.warn(`[e2e] ✗ first pass failed for ${nbName} (status=${res.status})`);
        if (res.stderr) {
          console.warn(`[e2e] stderr (first pass):\n${res.stderr.split('\n').slice(0, 200).join('\n')}`);
        }
      }

      // Retry with ALLOW_ERRORS=1 unless disabled
      if (RETRY_ALLOW_ERRORS) {
        console.log(`[e2e] retrying ${nbName} with ALLOW_ERRORS=1`);
        const res2 = runExecNotebook(nbRel, OUT_DIR, {
          python: PYTHON,
          timeoutMs: TIMEOUT,
          extraEnv: { ...process.env, ALLOW_ERRORS: '1' },
        });

        if (res2.status === 0) {
          try {
            const lastLine = (res2.stdout || '').trim().split(/\r?\n/).filter(Boolean).slice(-1)[0] || '';
            const parsed = JSON.parse(lastLine);
            console.log(`[e2e] ✔ ${nbName} (with ALLOW_ERRORS) -> HTML: ${parsed.htmlPath}`);
            summary.succeeded.push({ notebook: nbRel, html: parsed.htmlPath });
            continue;
          } catch (err) {
            console.warn(`[e2e] Warning: retry for ${nbName} exited 0 but JSON parse failed. stdout snippet:`);
            console.warn(res2.stdout.slice(0, 2000));
          }
        } else {
          console.warn(`[e2e] ✗ retry failed for ${nbName} (status=${res2.status})`);
          if (res2.stderr) {
            console.warn(`[e2e] stderr (retry):\n${res2.stderr.split('\n').slice(0, 200).join('\n')}`);
          }
        }
      } else {
        console.log('[e2e] RETRY_ALLOW_ERRORS=0; skipping retry with ALLOW_ERRORS');
      }

      // If we reach here, notebook failed
      summary.failed.push({ notebook: nbRel });
      console.error(`[e2e] ✗ failed for ${nbName}`);
    }

    // Summary
    console.log('\n=== prepare-e2e summary ===');
    console.log(`Notebooks discovered: ${summary.total}`);
    console.log(`Succeeded: ${summary.succeeded.length}`);
    summary.succeeded.forEach(s => console.log(`  - ${s.notebook} -> ${s.html}`));
    console.log(`Failed: ${summary.failed.length}`);
    summary.failed.forEach(f => console.log(`  - ${f.notebook}`));

    if (summary.failed.length > 0) {
      console.error('\n[prepare-e2e] ERROR: Some notebooks failed to generate HTML. See logs above.');
      process.exit(2);
    }

    console.log('\n[prepare-e2e] All notebooks processed successfully.');
    process.exit(0);
  } catch (err) {
    console.error('[prepare-e2e] Unexpected error:', err && err.stack ? err.stack : String(err));
    process.exit(99);
  }
})();
