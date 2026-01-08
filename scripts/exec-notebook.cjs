#!/usr/bin/env node
// scripts/exec-notebook.cjs
// Usage: node scripts/exec-notebook.cjs --notebook examples/foo.ipynb --outdir examples --htmlname foo.html
// Prints JSON to stdout: {"htmlPath":"...","executedNotebook":"..."}

const { spawnSync } = require('child_process');
const { resolve, dirname, basename, join } = require('path');
const { existsSync, mkdirSync, readdirSync, readFileSync } = require('fs');

function parseArgs() {
  const args = process.argv.slice(2);
  const out = {};
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--notebook') out.notebook = args[++i];
    else if (a === '--outdir') out.outdir = args[++i];
    else if (a === '--htmlname') out.htmlname = args[++i];
    else if (a === '--python') out.python = args[++i];
    else if (a === '--timeout') out.timeout = Number(args[++i]); // ms expected
  }
  return out;
}

function exitErr(msg, code = 1) {
  console.error(msg);
  process.exit(code);
}

function safeListDir(d) {
  try { return readdirSync(d); } catch (e) { return []; }
}

(async function main() {
  const {
    notebook,
    outdir = '.',
    htmlname,
    python = process.env.PYTHON || process.env.PYTHON_PATH || 'python3',
    timeout = 300000, // ms
  } = parseArgs();

  if (!notebook) exitErr('Missing --notebook argument');

  const repoRoot = resolve(process.cwd());
  const nbAbs = resolve(process.cwd(), notebook);

  // Prevent escaping repo root
  if (!nbAbs.startsWith(repoRoot + '/')) exitErr('Notebook must be inside the repo');

  if (!existsSync(nbAbs)) exitErr(`Notebook not found: ${nbAbs}`);

  const outDirAbs = resolve(process.cwd(), outdir);
  mkdirSync(outDirAbs, { recursive: true });

  const base = basename(nbAbs, '.ipynb');
  const executedBasename = `executed_${base}`; // NO extension here for --output
  const executedName = `${executedBasename}.ipynb`; // filename we expect to be written
  const htmlName = htmlname || `${base}.html`;

  const executedPath = join(outDirAbs, executedName);
  const htmlPath = join(outDirAbs, htmlName);

  // Convert JS timeout (ms) into seconds for ExecutePreprocessor.timeout
  const execTimeoutSeconds = Math.max(30, Math.floor(timeout / 1000));

  function run(cmd, args, opts = {}) {
    console.log(`[exec-notebook] ${cmd} ${args.map(a => a.includes(' ') ? JSON.stringify(a) : a).join(' ')}`);
    const sp = spawnSync(cmd, args, { stdio: 'inherit', timeout, env: { ...process.env }, ...opts });
    if (sp.error) exitErr(`Failed to spawn ${cmd}: ${sp.error.message}`);
    if (sp.status !== 0) exitErr(`${cmd} exited with code ${sp.status}`);
  }

  try {
    // 1) trust notebook
    run(python, ['-m', 'jupyter', 'trust', nbAbs]);

    // 2) execute -> written as executed_<base>.ipynb in outdir
    const allowErrorsFlag = process.env.ALLOW_ERRORS === '1' ? '--ExecutePreprocessor.allow_errors=True' : null;
    const executeArgs = [
      '-m', 'nbconvert',
      '--to', 'notebook',
      '--execute', nbAbs,
      '--output', executedBasename,       // basename WITHOUT extension
      '--output-dir', outDirAbs,
      `--ExecutePreprocessor.timeout=${execTimeoutSeconds}`
    ];
    if (allowErrorsFlag) executeArgs.push(allowErrorsFlag);

    run(python, executeArgs);

    // Check executed notebook exists
    if (!existsSync(executedPath)) {
      console.error(`[exec-notebook] ERROR: expected executed notebook not found at ${executedPath}`);
      console.error('[exec-notebook] Contents of output dir:', safeListDir(outDirAbs).join('\n  - '));
      exitErr('Executed notebook missing after nbconvert --execute');
    }

    // 3) export HTML from executed notebook
    // pass the executedPath as the input to nbconvert
    run(python, [
      '-m', 'nbconvert',
      '--to', 'html',
      executedPath,
      '--output', htmlName,
      '--output-dir', outDirAbs
    ]);

    // confirm html produced
    if (!existsSync(htmlPath)) {
      console.error(`[exec-notebook] ERROR: expected HTML not found at ${htmlPath}`);
      console.error('[exec-notebook] Contents of output dir:', safeListDir(outDirAbs).join('\n  - '));
      // If executedPath exists, print a small snippet of the JSON to show cell errors
      if (existsSync(executedPath)) {
        try {
          const j = JSON.parse(readFileSync(executedPath, 'utf8'));
          console.error('[exec-notebook] executed notebook metadata snippet:', JSON.stringify(j.metadata?.kernelspec || j.metadata?.language_info || {}, null, 2));
          // show whether any cell outputs contain errors
          const cellsWithErrors = (j.cells || []).filter(c => (c.outputs || []).some(o => o.ename || (o.output_type === 'error')));
          console.error(`[exec-notebook] executed notebook cells with errors: ${cellsWithErrors.length}`);
        } catch (pe) {
          console.error('[exec-notebook] failed to parse executed notebook for diagnostics:', pe.message);
        }
      }
      exitErr('HTML output missing after nbconvert --to html');
    }

    // Success: print JSON to stdout for caller to parse
    const result = {
      htmlPath,
      executedNotebook: executedPath,
    };
    // Write only one JSON line (easy for caller to parse)
    process.stdout.write(JSON.stringify(result) + '\n');
    process.exit(0);
  } catch (err) {
    exitErr(`Error during conversion: ${err && err.message ? err.message : String(err)}`);
  }
})();
