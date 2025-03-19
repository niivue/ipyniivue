import * as niivue from "@niivue/niivue";
import type { Model } from "./types.ts";

import { Disposer } from "./lib.ts";
import { render_meshes } from "./mesh.ts";
import { render_volumes } from "./volume.ts";

export default {
	async render({ model, el }: { model: Model; el: HTMLElement }) {
		const disposer = new Disposer();
		const canvas = document.createElement("canvas");
		const container = document.createElement("div");
		container.style.height = `${model.get("height")}px`;
		container.appendChild(canvas);
		el.appendChild(container);

		const nv = new niivue.Niivue(model.get("_opts") ?? {});
		nv.attachToCanvas(canvas);

		await render_volumes(nv, model, disposer);
		model.on("change:_volumes", () => render_volumes(nv, model, disposer));
		await render_meshes(nv, model, disposer);
		model.on("change:_meshes", () => render_meshes(nv, model, disposer));

		nv.createEmptyDrawing();

		// Any time we change the options, we need to update the nv object
		// and redraw the scene.
		model.on("change:_opts", () => {
			nv.document.opts = { ...nv.opts, ...model.get("_opts") };
			nv.drawScene();
			nv.updateGLVolume();
		});
		model.on("change:height", () => {
			container.style.height = `${model.get("height")}px`;
		});

		// Handle any message directions from the nv object.
		model.on("msg:custom", (payload: { type: string; data }) => {
			const { type, data } = payload;
			switch (type) {
				case "save_document": {
					const { fileName, compress } = data;
					nv.saveDocument(fileName, compress);
					break;
				}
				case "save_html": {
					const { fileName, canvasId } = data;
					// Note: currently fails as esm is inaccesbile.
					// nv.saveHTML(fileName, canvasId, esm);
					break;
				}
				case "save_image": {
					nv.saveImage(data);
					break;
				}
				case "save_scene": {
					nv.saveScene(data);
					break;
				}
			}
		});

		// All the logic for cleaning up the event listeners and the nv object
		return () => {
			disposer.disposeAll();
			model.off("change:_volumes");
			model.off("change:_opts");
		};
	},
};
