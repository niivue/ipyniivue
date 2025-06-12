import { v4 as uuidv4 } from "@lukeed/uuid";
import * as niivue from "@niivue/niivue";

import { Disposer, gather_models } from "./lib.ts";
import { render_meshes } from "./mesh.ts";
import type {
	CustomMessagePayload,
	MeshModel,
	Model,
	VolumeModel,
} from "./types.ts";
import { render_volumes } from "./volume.ts";

// store all nv objects for the page
const nvMap = new Map<string, niivue.Niivue>();

// Attach model event handlers
function attachModelEventHandlers(
	nv: niivue.Niivue,
	model: Model,
	disposer: Disposer,
) {
	model.on("change:_volumes", () => {
		if (nv.canvas) {
			render_volumes(nv, model, disposer);
		}
	});
	model.on("change:_meshes", () => {
		if (nv.canvas) {
			render_meshes(nv, model, disposer);
		}
	});

	// Any time we change the options, we need to update the nv gl
	model.on("change:_opts", () => {
		console.log("Updating opts");
		nv.document.opts = { ...nv.opts, ...model.get("_opts") };
		nv.updateGLVolume();
	});

	// Other nv prop changes
	model.on("change:background_masks_overlays", () => {
		nv.backgroundMasksOverlays = model.get("background_masks_overlays");
		nv.updateGLVolume();
	});

	// Handle any message directions from the nv object.
	model.on("msg:custom", (payload: CustomMessagePayload) => {
		const { type, data } = payload;
		switch (type) {
			case "save_document": {
				const [fileName, compress] = data;
				nv.saveDocument(fileName, compress);
				break;
			}
			case "save_html": {
				const [fileName, canvasId] = data;
				// Note: currently fails as esm is inaccessible.
				// nv.saveHTML(fileName, canvasId, esm);
				break;
			}
			case "save_image": {
				const [filename, isSaveDrawing, volumeByIndex] = data;
				nv.saveImage({
					filename,
					isSaveDrawing,
					volumeByIndex,
				});
				break;
			}
			case "save_scene": {
				const [fileName] = data;
				nv.saveScene(fileName);
				break;
			}
			case "add_colormap": {
				const [name, cmap] = data;
				nv.addColormap(name, cmap);
				break;
			}
			case "set_gamma": {
				const [gamma] = data;
				nv.setGamma(gamma);
				break;
			}
			case "set_clip_plane": {
				const [clipPlane] = data;
				nv.setClipPlane(clipPlane);
				break;
			}
			case "set_mesh_shader": {
				const [meshId, shader] = data;
				nv.setMeshShader(meshId, shader);
				break;
			}
			case "resize_listener": {
				nv.resizeListener();
				break;
			}
			case "draw_scene": {
				nv.drawScene();
				break;
			}
			case "set_volume_render_illumination": {
				if (nv.gl) {
					let [gradientAmount] = data;
					if (gradientAmount === null) {
						gradientAmount = Number.NaN;
					} else {
						gradientAmount = Number(gradientAmount);
					}
					nv.setVolumeRenderIllumination(gradientAmount);
				}
				break;
			}
			case "load_png_as_texture": {
				const [pngUrl, textureNum] = data;
				nv.loadPngAsTexture(pngUrl, textureNum);
			}
		}
	});
}

// Attach Niivue event handlers
function attachNiivueEventHandlers(nv: niivue.Niivue, model: Model) {
	nv.onImageLoaded = async (volume: niivue.NVImage) => {
		// Check if the volume is already in the backend
		const volumeID = volume.id;
		const volumeModels = await gather_models<VolumeModel>(
			model,
			model.get("_volumes"),
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
				opacity: volume.opacity,
				colormap: volume.colormap,
				colorbar_visible: volume.colorbarVisible,
				cal_min: volume.cal_min,
				cal_max: volume.cal_max,
				frame4D: volume.frame4D,
				colormap_negative: volume.colormapNegative,
				colormap_label: volume.colormapLabel,
				index: nv.getVolumeIndexByID(volume.id),
			};

			// Send a custom message to the backend to add the volume with the index
			model.send({
				event: "add_volume",
				data: volumeData,
			});
		}

		model.send({
			event: "image_loaded",
			data: {
				id: volume.id,
			},
		});
	};

	nv.onMeshLoaded = async (mesh: niivue.NVMesh) => {
		// Check if the mesh is already in the backend
		const meshID = mesh.id;
		const meshModels = await gather_models<MeshModel>(
			model,
			model.get("_meshes"),
		);

		const backendMeshIds = meshModels.map((mmodel) => mmodel?.get("id") || "");

		if (!backendMeshIds.includes(meshID)) {
			// Mesh is new; create a new MeshModel in the backend

			// Prepare layers data
			// biome-ignore lint/suspicious/noExplicitAny: NVMeshLayer isn't exported from niivue
			const layersData = mesh.layers.map((layer: any) => {
				if (!layer.id) {
					layer.id = uuidv4();
				}
				return {
					path: "<fromfrontend>",
					opacity: layer.opacity,
					colormap: layer.colormap,
					colormap_negative: layer.colormapNegative,
					use_negative_cmap: layer.useNegativeCmap,
					cal_min: layer.cal_min,
					cal_max: layer.cal_max,
					outline_border: layer.outlineBorder,
					id: layer.id,
				};
			});

			const meshData = {
				path: "<fromfrontend>",
				id: mesh.id,
				name: mesh.name,
				rgba255: Array.from(mesh.rgba255),
				opacity: mesh.opacity,
				layers: layersData,
				visible: mesh.visible,
				index: nv.getMeshIndexByID(mesh.id),
			};

			// Send a custom message to the backend to add the mesh
			model.send({
				event: "add_mesh",
				data: meshData,
			});
		}

		model.send({
			event: "mesh_loaded",
			data: {
				id: mesh.id,
			},
		});
	};

	// update other event handlers
	nv.onAzimuthElevationChange = (azimuth: number, elevation: number) => {
		model.send({
			event: "azimuth_elevation_change",
			data: { azimuth, elevation },
		});
	};

	nv.onClickToSegment = (data: { mm3: number; mL: number }) => {
		model.send({
			event: "click_to_segment",
			data,
		});
	};

	nv.onClipPlaneChange = (clipPlane: number[]) => {
		model.send({
			event: "clip_plane_change",
			data: clipPlane,
		});
	};

	// todo: can add more properties, see niivue/packages/niivue/src/nvdocument.ts
	nv.onDocumentLoaded = (document: niivue.NVDocument) => {
		model.send({
			event: "document_loaded",
			data: {
				title: document.title || "",
				opts: document.opts || {},
				volumes: document.volumes.map((volume) => volume.id),
				meshes: document.meshes.map((mesh) => mesh.id),
			},
		});
	};

	nv.onDragRelease = (params: niivue.DragReleaseParams) => {
		model.send({
			event: "drag_release",
			data: {
				frac_start: params.fracStart,
				frac_end: params.fracEnd,
				vox_start: params.voxStart,
				vox_end: params.voxEnd,
				mm_start: params.mmStart,
				mm_end: params.mmEnd,
				mm_length: params.mmLength,
				tile_idx: params.tileIdx,
				ax_cor_sag: params.axCorSag,
			},
		});
	};

	nv.onFrameChange = (volume: niivue.NVImage, index: number) => {
		model.send({
			event: "frame_change",
			data: {
				id: volume.id,
				index,
			},
		});
	};

	nv.onIntensityChange = (volume: niivue.NVImage) => {
		model.send({
			event: "intensity_change",
			data: {
				id: volume.id,
			},
		});
	};

	// biome-ignore lint/suspicious/noExplicitAny: location has unknown type in niivue library
	nv.onLocationChange = (location: any) => {
		model.send({
			event: "location_change",
			data: {
				ax_cor_sag: location.axCorSag,
				frac: location.frac,
				mm: location.mm,
				string: location.string || "",
				values: location.values,
				vox: location.vox,
				xy: location.xy,
			},
		});
	};

	// biome-ignore lint/suspicious/noExplicitAny: LoadFromUrlParams does not exist type niivue
	nv.onMeshAddedFromUrl = (meshOptions: any, mesh: niivue.NVMesh) => {
		model.send({
			event: "mesh_added_from_url",
			data: {
				url: meshOptions.url,
				headers: meshOptions?.headers || {},
				mesh: {
					id: mesh.id,
					name: mesh.name,
					rgba255: Array.from(mesh.rgba255),
					opacity: mesh.opacity,
					visible: mesh.visible,
				},
			},
		});
	};

	// biome-ignore lint/suspicious/noExplicitAny: UIData does not exist type niivue
	nv.onMouseUp = (data: any) => {
		model.send({
			event: "mouse_up",
			data: {
				is_dragging: data.isDragging,
				mouse_pos: data.mousePos,
				frac_pos: data.fracPos,
			},
		});
	};

	// biome-ignore lint/suspicious/noExplicitAny: ImageFromUrlOptions does not exist type niivue
	nv.onVolumeAddedFromUrl = (imageOptions: any, volume: niivue.NVImage) => {
		model.send({
			event: "volume_added_from_url",
			data: {
				url: imageOptions.url,
				url_image_data: imageOptions?.urlImageData || "",
				headers: imageOptions?.headers || {},
				name: imageOptions?.name || "",
				colormap: imageOptions?.colorMap || "gray",
				opacity: imageOptions?.opacity || 1,
				cal_min: imageOptions?.cal_min || Number.NaN,
				cal_max: imageOptions?.cal_max || Number.NaN,
				trust_cal_min_max: imageOptions?.trustCalMinMax || true,
				percentile_frac: imageOptions?.percentileFrac || 0.02,
				use_qform_not_sform: imageOptions?.useQFormNotSForm || false,
				alpha_threshold: imageOptions?.alphaThreshold || false,
				colormap_negative: imageOptions?.colormapNegative || "",
				cal_min_neg: imageOptions?.cal_minNeg || Number.NaN,
				cal_max_neg: imageOptions?.cal_maxNeg || Number.NaN,
				colorbar_visible: imageOptions?.colorbarVisible || true,
				ignore_zero_voxels: imageOptions?.ignoreZeroVoxels || false,
				image_type: imageOptions?.imageType || 0,
				frame4D: imageOptions?.frame4D || 0,
				colormap_label: imageOptions?.colormapLabel || null,
				//paired_img_data: imageOptions?.pairedImgData || null, //support? or no?
				limit_frames4D: imageOptions?.limitFrames4D || Number.NaN,
				is_manifest: imageOptions?.isManifest || false,
				//url_img_data: imageOptions?.urlImgData || null, //support? or no?

				volume: {
					id: volume.id,
					name: volume.name,
					colormap: volume.colormap,
					opacity: volume.opacity,
					colorbar_visible: volume.colorbarVisible,
					cal_min: volume.cal_min,
					cal_max: volume.cal_max,
				},
			},
		});
	};

	nv.onVolumeUpdated = () => {
		model.send({
			event: "volume_updated",
		});
	};
}

export default {
	async initialize({ model }: { model: Model }) {
		const id = model.get("id");
		console.log("Initializing called on model:", id);
		const disposer = new Disposer();

		let nv = nvMap.get(model.get("id"));

		if (!nv) {
			console.log("Creating new Niivue instance");
			nv = new niivue.Niivue(model.get("_opts") ?? {});
			nvMap.set(model.get("id"), nv);
		}

		// Attach model event handlers
		attachModelEventHandlers(nv, model, disposer);

		// Attach niivue event handlers
		attachNiivueEventHandlers(nv, model);

		// Logic for cleaning up the event listeners and the nv object
		return () => {
			disposer.disposeAll();

			model.off("change:_volumes");
			model.off("change:_meshes");
			model.off("change:_opts");
			model.off("change:height");
			model.off("msg:custom");

			model.off("change:background_masks_overlays");

			// remove the nv instance
			nvMap.delete(model.get("id"));
		};
	},
	async render({ model, el }: { model: Model; el: HTMLElement }) {
		const nv = nvMap.get(model.get("id"));
		if (!nv) {
			console.error("Niivue instance not found for model", model.get("id"));
			return;
		}

		const disposer = new Disposer();

		if (!nv.canvas?.parentNode) {
			console.log("drawing first render");

			// Create a container div and set its height
			const container = document.createElement("div");
			container.style.height = `${model.get("height")}px`;
			el.appendChild(container);

			// Create a new canvas and attach it to the container
			const canvas = document.createElement("canvas");
			container.appendChild(canvas);

			// Handle height changes
			model.off("change:height");
			model.on("change:height", () => {
				container.style.height = `${model.get("height")}px`;
			});

			// Attach nv to canvas
			nv.attachToCanvas(canvas, nv.opts.isAntiAlias);

			// Load initial volumes and meshes
			await render_volumes(nv, model, disposer);
			await render_meshes(nv, model, disposer);
		} else {
			console.log("moving render around");

			// Ensure the canvas is attached to the container
			if (nv.canvas.parentNode?.parentNode) {
				nv.canvas.parentNode.parentNode.removeChild(nv.canvas.parentNode);
			}

			// Attach
			el.appendChild(nv.canvas.parentNode);
		}

		// Drawing setup
		nv.setDrawingEnabled(nv.opts.drawingEnabled);

		// Return cleanup function, runs when page reloaded or cell run again
		return () => {
			// only want to run disposer when nv widget is removed, not when it is re-displayed

			if (nv.canvas?.parentNode?.parentNode) {
				nv.canvas.parentNode.parentNode.removeChild(nv.canvas.parentNode);
			}
		};
	},
};
