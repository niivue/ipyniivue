import * as niivue from "@niivue/niivue";
import type { Model } from "./types.ts";

import { render_meshes } from "./mesh.ts";
import { render_volumes } from "./volume.ts";

export default {
	async render({ model, el }: { model: Model; el: HTMLElement }) {
		const canvas = document.createElement("canvas");
		const container = document.createElement("div");
		container.style.height = "300px";
		container.appendChild(canvas);
		el.appendChild(container);

		const nv = new niivue.Niivue(model.get("_opts") ?? {});
		nv.attachToCanvas(canvas);

		const vcleanups = new Map<string, () => void>();
		await render_volumes(nv, model, vcleanups);
		model.on("change:_volumes", () => render_volumes(nv, model, vcleanups));

		const mcleanups = new Map<string, () => void>();
		await render_meshes(nv, model, mcleanups);
		model.on("change:_meshes", () => render_meshes(nv, model, mcleanups));

		// Any time we change the options, we need to update the nv object
		// and redraw the scene.
		model.on("change:_opts", () => {
			nv.document.opts = { ...nv.opts, ...model.get("_opts") };
			nv.drawScene();
			nv.updateGLVolume();
		});

		// All the logic for cleaning up the event listeners and the nv object
		return () => {
			for (const [_, cleanup] of vcleanups) cleanup();
			vcleanups.clear();
			for (const [_, cleanup] of mcleanups) cleanup();
			mcleanups.clear();
			model.off("change:_volumes");
			model.off("change:_opts");
		};
	},
};
