import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import * as niivue from "@niivue/niivue";
import esbuild from "esbuild";

global.window = {};

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const generateColormapsPlugin = {
	name: "generate-colormaps",
	setup(build) {
		build.onEnd((result) => {
			if (result?.errors?.length === 0) {
				const nv = new niivue.Niivue();
				const colormapNames = nv.colormaps();
				const colormapsTxtContent = colormapNames.join("\n");

				const outputPath = path.join(
					__dirname,
					"src",
					"ipyniivue",
					"static",
					"colormaps.txt",
				);

				fs.writeFileSync(outputPath, colormapsTxtContent, "utf8");
				console.log("Successfully generated colormaps.txt.");
			} else {
				console.error("Build failed, colormaps.txt not generated.");
			}
		});
	},
};

const generateShaderNamesPlugin = {
	name: "generate-shader-names",
	setup(build) {
		build.onEnd((result) => {
			if (result?.errors?.length === 0) {
				const nv = new niivue.Niivue();
				const shaderNames = nv.meshShaders.map((shader) => shader.Name);
				const shaderNamesTxtContent = shaderNames.join("\n");

				const outputPath = path.join(
					__dirname,
					"src",
					"ipyniivue",
					"static",
					"meshShaderNames.txt",
				);

				fs.writeFileSync(outputPath, shaderNamesTxtContent, "utf8");
				console.log("Successfully generated meshShaderNames.txt.");
			} else {
				console.error("Build failed, meshShaderNames.txt not generated.");
			}
		});
	},
};

async function build(isWatchMode) {
	const buildOptions = {
		entryPoints: ["js/widget.ts"],
		bundle: true,
		outfile: "src/ipyniivue/static/widget.js",
		plugins: [generateColormapsPlugin, generateShaderNamesPlugin],
		format: "esm",
		minify: true,
	};

	if (isWatchMode) {
		const ctx = await esbuild.context(buildOptions);
		await ctx.watch();
		console.log("Watching for changes...");
	} else {
		await esbuild.build(buildOptions).catch(() => process.exit(1));
	}
}

const isWatchMode = process.argv.includes("--watch");

build(isWatchMode).catch((e) => {
	console.error(e);
	process.exit(1);
});
