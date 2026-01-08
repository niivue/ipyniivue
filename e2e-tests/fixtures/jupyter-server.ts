import { type ChildProcess, execSync, spawn } from "node:child_process";
import { mkdirSync, rmSync } from "node:fs";
import { mkdtempSync } from "node:fs";
import http from "node:http";
import { platform } from "node:os";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import process from "node:process";
import { test as base } from "@playwright/test";

console.log("🧩 [fixture module load] fixtures/jupyter-server.ts loaded");

type JupyterEnv = {
	staticUrl: string;
	jupyterProcess?: ChildProcess;
	outDir: string;
};

type JupyterFixture = {
	jupyterEnv: JupyterEnv;
};

const basePort = 8888;
const workerIndex = Number(process.env.PLAYWRIGHT_WORKER_INDEX ?? 0);
const JUPYTER_PORT = basePort + workerIndex;
const JUPYTER_URL = `http://127.0.0.1:${JUPYTER_PORT}`;
const workerScope = { scope: "worker" } as const;

async function waitForReady(url: string, timeout = 30_000) {
	const start = Date.now();
	while (Date.now() - start < timeout) {
		try {
			await new Promise<void>((resolve, reject) => {
				const req = http.get(url, (res) => {
					if (res.statusCode === 200) resolve();
					else reject(new Error(`status ${res.statusCode}`));
				});
				req.on("error", reject);
				req.setTimeout(2000, () => req.destroy());
			});
			return;
		} catch {
			await new Promise((r) => setTimeout(r, 300));
		}
	}
	throw new Error(`Timed out waiting for service at ${url}`);
}

function candidates(): string[] {
	const arr: string[] = [];
	if (process.env.PYTHON) arr.push(process.env.PYTHON);
	if (process.env.PYTHON_PATH) arr.push(process.env.PYTHON_PATH);
	arr.push("python3", "python");
	return Array.from(new Set(arr.filter(Boolean)));
}

async function trySpawnPython(
	args: string[],
	timeoutMs = 5000,
): Promise<ChildProcess | null> {
	const list = candidates();
	for (const cmd of list) {
		console.log(
			`[fixture] trying python candidate: "${cmd}" with args ${JSON.stringify(args)}`,
		);
		try {
			const child = spawn(cmd, args, {
				env: { ...process.env },
				stdio: ["pipe", "pipe", "pipe"],
			});

			let spawnError: Error | null = null;
			const errorHandler = (err: Error) => {
				spawnError = err;
			};

			child.once("error", errorHandler);

			const exitedEarly = await new Promise<boolean>((resolve) => {
				let settled = false;
				const onExit = () => {
					if (!settled) {
						settled = true;
						resolve(true);
					}
				};
				const onReady = () => {
					if (!settled) {
						settled = true;
						resolve(false);
					}
				};
				child.once("exit", onExit);
				child.stdout?.once("data", () => onReady());
				child.stderr?.once("data", () => onReady());
				setTimeout(() => onReady(), timeoutMs);
			});

			child.removeListener("error", errorHandler);

			if (spawnError) {
				console.error(
					`[fixture] spawn error for candidate ${cmd}:`,
					spawnError,
				);
				try {
					child.kill();
				} catch {}
				continue;
			}

			if (exitedEarly) {
				console.error(
					`[fixture] candidate ${cmd} exited immediately; not using it.`,
				);
				continue;
			}

			return child;
		} catch (err) {
			console.error(
				`[fixture] synchronous spawn failed for ${cmd}:`,
				(err as Error).message,
			);
		}
	}

	return null;
}

export const test = base.extend<JupyterFixture>({
	// jupyterEnv is a worker-scoped fixture that starts Jupyter + a static server,
	// pre-executes the notebook into a worker-local temp dir, and yields the info.
	// @ts-ignore -- Playwright's types expect a test-scoped fixture here; we intentionally provide a worker-scoped fixture.
	jupyterEnv: [
		async (_params: unknown, use: (arg0: JupyterEnv) => Promise<void>) => {
			console.log(
				`🟢 [fixture] Starting Jupyter (worker ${workerIndex}) on port ${JUPYTER_PORT}`,
			);

			const args = [
				"-m",
				"jupyter",
				"lab",
				"--no-browser",
				`--port=${JUPYTER_PORT}`,
				"--ServerApp.token=",
				"--ServerApp.password=",
				"--NotebookApp.token=",
				"--NotebookApp.password=",
				"--ServerApp.allow_origin=*",
				"--ServerApp.disable_check_xsrf=True",
			];

			const proc = await trySpawnPython(args, 3000);
			if (!proc) {
				console.error("[fixture] could not spawn Jupyter. Diagnostics:");
				console.error("  platform:", platform());
				console.error(
					"  PYTHON env:",
					process.env.PYTHON,
					"PYTHON_PATH:",
					process.env.PYTHON_PATH,
				);
				console.error("  PATH:", process.env.PATH);
				throw new Error(
					'Failed to spawn a Python runtime for "python -m jupyter lab". Ensure python/jupyter are installed and accessible.',
				);
			}

			// --- PREP: generate executed notebook + HTML into a worker-local temp directory ---
			const ROOT_TMP = mkdtempSync(join(tmpdir(), "jupyter-out-"));
			const OUT_DIR = join(ROOT_TMP, `worker-${workerIndex}`);
			mkdirSync(OUT_DIR, { recursive: true });

			const NOTEBOOK = "examples/basic_multiplanar.ipynb";
			const EXECUTED_NOTEBOOK_NAME = "executed_basic_multiplanar.ipynb";
			const EXECUTED_HTML_NAME = "basic_multiplanar.html";
			const executedNotebookPath = join(OUT_DIR, EXECUTED_NOTEBOOK_NAME);

			try {
				const pythonExec =
					process.env.PYTHON || process.env.PYTHON_PATH || "python3";

				console.log(`[fixture] trusting notebook ${NOTEBOOK}`);
				execSync(`${pythonExec} -m jupyter trust "${NOTEBOOK}"`, {
					env: { ...process.env },
					stdio: "inherit",
				});

				console.log(
					`[fixture] pre-executing notebook ${NOTEBOOK} -> ${executedNotebookPath}`,
				);
				execSync(
					`${pythonExec} -m nbconvert --to notebook --execute "${NOTEBOOK}" --output "${EXECUTED_NOTEBOOK_NAME}" --output-dir "${OUT_DIR}" --ExecutePreprocessor.timeout=300`,
					{
						env: { ...process.env },
						stdio: "inherit",
						timeout: 5 * 60 * 1000,
					},
				);

				console.log(
					`[fixture] exporting HTML from executed notebook -> ${join(OUT_DIR, EXECUTED_HTML_NAME)}`,
				);
				execSync(
					`${pythonExec} -m nbconvert --to html "${executedNotebookPath}" --output "${EXECUTED_HTML_NAME}" --output-dir "${OUT_DIR}"`,
					{
						env: { ...process.env },
						stdio: "inherit",
						timeout: 60 * 1000,
					},
				);

				console.log("[fixture] pre-execution + HTML export complete");
			} catch (err) {
				console.warn(
					"[fixture] warning: pre-execution/html export failed:",
					err,
				);
				// allow tests to continue if you want; else rethrow
			}

			// --- START a local static server to serve OUT_DIR so Playwright can request it via http ---
			const STATIC_PORT = 9000 + workerIndex;
			const STATIC_URL = `http://127.0.0.1:${STATIC_PORT}`;

			const staticArgs = [
				"-m",
				"http.server",
				`${STATIC_PORT}`,
				"--bind",
				"127.0.0.1",
				"--directory",
				OUT_DIR,
			];
			const staticProc = await trySpawnPython(staticArgs, 3000);
			if (!staticProc) {
				console.error(
					"[fixture] could not spawn static HTTP server to serve generated HTML.",
				);
				try {
					proc.kill();
				} catch {}
				throw new Error(
					"Failed to spawn static HTTP server (python -m http.server).",
				);
			}

			staticProc.stdout?.on("data", (d) => {
				const s = d.toString();
				console.log(`[static stdout] ${s.trim()}`);
			});
			staticProc.stderr?.on("data", (d) => {
				const s = d.toString();
				console.error(`[static stderr] ${s.trim()}`);
			});
			staticProc.on("error", (err) => {
				console.error("[static proc] error event:", err);
			});

			try {
				await waitForReady(`${STATIC_URL}/`, 30_000);
				console.log(
					`✅ [fixture] Static server ready at ${STATIC_URL} serving ${OUT_DIR}`,
				);
			} catch (err) {
				console.error(
					"[fixture] static server did not become ready:",
					(err as Error).message,
				);
				try {
					staticProc.kill();
				} catch {}
				try {
					proc.kill();
				} catch {}
				throw err;
			}

			console.log(
				`[fixture] spawned jupyter pid=${proc.pid} — streaming stdout/stderr below`,
			);
			proc.stdout?.on("data", (d) => {
				console.log(`[jupyter stdout] ${d.toString().trim()}`);
			});
			proc.stderr?.on("data", (d) => {
				console.error(`[jupyter stderr] ${d.toString().trim()}`);
			});

			// Attempt to wait for Jupyter to be ready (best-effort)
			try {
				await waitForReady(`${JUPYTER_URL}/lab/api/settings`, 60_000);
				console.log(`✅ [fixture] Jupyter ready at ${JUPYTER_URL}`);
			} catch (err) {
				console.error(
					"[fixture] Jupyter did not become ready:",
					(err as Error).message,
				);
			}

			// Build the environment object and yield it to tests
			const env: JupyterEnv = {
				staticUrl: STATIC_URL,
				jupyterProcess: proc,
				outDir: OUT_DIR,
			};

			await use(env);

			// teardown: kill static server and jupyter, remove temp dir
			console.log(`🔴 [fixture] Killing static server pid=${staticProc.pid}`);
			try {
				staticProc.kill();
			} catch (e) {
				console.error("failed to kill staticProc", e);
			}

			console.log(
				`🔴 [fixture] Killing Jupyter pid=${proc.pid} on port ${JUPYTER_PORT}`,
			);
			try {
				proc.kill();
			} catch (e) {
				console.error("failed to kill jupyter proc", e);
			}

			console.log(`[fixture] removing temp output dir ${OUT_DIR}`);
			try {
				rmSync(OUT_DIR, { recursive: true, force: true });
			} catch (e) {
				console.error("failed to remove out dir", e);
			}
		},
		workerScope,
	] as unknown,
});

export { expect } from "@playwright/test";
