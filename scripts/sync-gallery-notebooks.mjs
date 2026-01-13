import { execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const JN_DIR = path.resolve("external/jupyter-notebooks");
const DEST = path.resolve("gallery/notebooks-src");

const JN_REPO = "https://github.com/niivue/jupyter-notebooks.git";
const JN_BRANCH = "main";

/**
 * Utilities
 */
function run(cmd, opts = {}) {
	console.log(`> ${cmd}`);
	execSync(cmd, { stdio: "inherit", ...opts });
}

function rmrf(p) {
	if (fs.existsSync(p)) {
		fs.rmSync(p, { recursive: true, force: true });
	}
}

function copyDir(src, dest) {
	fs.mkdirSync(dest, { recursive: true });
	for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
		const s = path.join(src, entry.name);
		const d = path.join(dest, entry.name);
		if (entry.isDirectory()) {
			copyDir(s, d);
		} else {
			fs.copyFileSync(s, d);
		}
	}
}

/**
 * Step 1: Ensure jupyter-notebooks is present and up to date
 */
if (!fs.existsSync(JN_DIR)) {
	console.log("📥 jupyter-notebooks not found — cloning latest");
	fs.mkdirSync(path.dirname(JN_DIR), { recursive: true });
	run(`git clone --depth=1 --branch ${JN_BRANCH} ${JN_REPO} ${JN_DIR}`);
} else {
	console.log("🔄 Updating jupyter-notebooks to latest");
	run(`git fetch origin ${JN_BRANCH}`, { cwd: JN_DIR });
	run(`git reset --hard origin/${JN_BRANCH}`, { cwd: JN_DIR });
	run("git clean -fd", { cwd: JN_DIR });
}

/**
 * Step 2: Copy notebooks into gallery source
 */
console.log(`🧹 Removing old gallery notebooks: ${DEST}`);
rmrf(DEST);

console.log(`📚 Copying notebooks from ${JN_DIR} → ${DEST}`);
copyDir(JN_DIR, DEST);

console.log("✅ Gallery notebooks synced from latest jupyter-notebooks");
