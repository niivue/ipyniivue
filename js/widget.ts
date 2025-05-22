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

		nv.onImageLoaded = async (volume: niivue.NVImage) => {
			// Check if the volume is already in the backend
			const volumeID = volume.id;
			const volumeModels = await Promise.all(
				model.get("_volumes").map(async (v: string) => {
					const modelID = v.slice("IPY_MODEL_".length);
					const vmodel = await model.widget_manager.get_model(modelID);
					return vmodel;
				}),
			);

			const backendVolumeIds = volumeModels.map(
				(vmodel) => vmodel?.get("id") || "",
			);

			if (!backendVolumeIds.includes(volumeID)) {
				// Volume is new; create a new VolumeModel in the backend
				// volume.toUint8Array().slice().buffer for data
				const volumeData = {
					path: "<fromfrontend>",
					id: volume.id,
					name: volume.name,
					colormap: volume.colormap,
					opacity: volume.opacity,
					colorbar_visible: volume.colorbarVisible,
					cal_min: volume.cal_min,
					cal_max: volume.cal_max,
					index: nv.getVolumeIndexByID(volume.id),
				};

				// Send a custom message to the backend to add the volume with the index
				model.send({
					event: "add_volume",
					data: volumeData,
				});
			}
		};

		nv.onMeshLoaded = async (mesh: niivue.NVMesh) => {
			// Check if the mesh is already in the backend
			const meshID = mesh.id;
			const meshModels = await Promise.all(
				model.get("_meshes").map(async (m: string) => {
					const modelID = m.slice("IPY_MODEL_".length);
					const mmodel = await model.widget_manager.get_model(modelID);
					return mmodel;
				}),
			);

			const backendMeshIds = meshModels.map(
				(mmodel) => mmodel?.get("id") || "",
			);

			if (!backendMeshIds.includes(meshID)) {
				// Mesh is new; create a new MeshModel in the backend
				const meshData = {
					path: "<fromfrontend>",
					id: mesh.id,
					name: mesh.name,
					rgba255: Array.from(mesh.rgba255),
					opacity: mesh.opacity,
					layers: [], //don't send layers for now
					visible: mesh.visible,
					index: nv.meshes.findIndex((m) => m.id === mesh.id),
				};

				// Send a custom message to the backend to add the mesh
				model.send({
					event: "add_mesh",
					data: meshData,
				});
			}
		};

		await render_volumes(nv, model, disposer);
		model.on("change:_volumes", () => render_volumes(nv, model, disposer));
		await render_meshes(nv, model, disposer);
		model.on("change:_meshes", () => render_meshes(nv, model, disposer));

		nv.createEmptyDrawing();

		// Any time we change the options, we need to update the nv gl
		model.on("change:_opts", () => {
			nv.document.opts = { ...nv.opts, ...model.get("_opts") };
			nv.updateGLVolume();
		});
		model.on("change:height", () => {
			container.style.height = `${model.get("height")}px`;
		});

		// Define specific types for each case
		type SaveDocumentData = {
			fileName: string;
			compress: boolean;
		};

		type SaveHTMLData = {
			fileName: string;
			canvasId: string;
		};

		type SaveImageData = {
			fileName: string;
			saveDrawing: boolean;
			indexVolume: number;
		};

		type SaveSceneData = {
			fileName: string;
		};

		type CustomMessagePayload =
			| { type: "save_document"; data: SaveDocumentData }
			| { type: "save_html"; data: SaveHTMLData }
			| { type: "save_image"; data: SaveImageData }
			| { type: "save_scene"; data: SaveSceneData };

		// Handle any message directions from the nv object.
		model.on("msg:custom", (payload: CustomMessagePayload) => {
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
					const { fileName, saveDrawing, indexVolume } = data;
					nv.saveImage({
						filename: fileName,
						isSaveDrawing: saveDrawing,
						volumeByIndex: indexVolume,
					});
					break;
				}
				case "save_scene": {
					const { fileName } = data;
					nv.saveScene(fileName);
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
