import * as niivue from "@niivue/niivue";
import * as lib from "./lib.ts";
import type { MeshLayerModel, MeshModel, Model } from "./types.ts";

import { v4 as uuidv4 } from "@lukeed/uuid";

/**
 * Set up event listeners to handle changes to the layer properties.
 * Returns a function to clean up the event listeners.
 */
function setup_layer_property_listeners(
	// biome-ignore lint/suspicious/noExplicitAny: NVMeshLayer isn't exported from niivue
	layer: any,
	layerModel: MeshLayerModel,
	mesh: niivue.NVMesh,
	nv: niivue.Niivue,
): () => void {
	function opacity_changed() {
		layer.opacity = layerModel.get("opacity");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	function colormap_changed() {
		layer.colormap = layerModel.get("colormap");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	function colormap_negative_changed() {
		layer.colormapNegative = layerModel.get("colormap_negative");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	function use_negative_cmap_changed() {
		layer.useNegativeCmap = layerModel.get("use_negative_cmap");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	function cal_min_changed() {
		layer.cal_min = layerModel.get("cal_min");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	function cal_max_changed() {
		layer.cal_max = layerModel.get("cal_max");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	// Set up the event listeners
	layerModel.on("change:opacity", opacity_changed);
	layerModel.on("change:colormap", colormap_changed);
	layerModel.on("change:colormap_negative", colormap_negative_changed);
	layerModel.on("change:use_negative_cmap", use_negative_cmap_changed);
	layerModel.on("change:cal_min", cal_min_changed);
	layerModel.on("change:cal_max", cal_max_changed);

	// Return a cleanup function
	return () => {
		layerModel.off("change:opacity", opacity_changed);
		layerModel.off("change:colormap", colormap_changed);
		layerModel.off("change:colormap_negative", colormap_negative_changed);
		layerModel.off("change:use_negative_cmap", use_negative_cmap_changed);
		layerModel.off("change:cal_min", cal_min_changed);
		layerModel.off("change:cal_max", cal_max_changed);
	};
}

/**
 * Set up event listeners to handle changes to the mesh properties.
 * Returns a function to clean up the event listeners.
 */
function setup_mesh_property_listeners(
	mesh: niivue.NVMesh,
	mmodel: MeshModel,
	nv: niivue.Niivue,
): () => void {
	function opacity_changed() {
		mesh.opacity = mmodel.get("opacity");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}
	function rgba255_changed() {
		mesh.rgba255 = new Uint8Array(mmodel.get("rgba255"));
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}
	function visible_changed() {
		mesh.visible = mmodel.get("visible");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	mmodel.on("change:opacity", opacity_changed);
	mmodel.on("change:rgba255", rgba255_changed);
	mmodel.on("change:visible", visible_changed);

	// Return a function to remove the event listeners
	return () => {
		mmodel.off("change:opacity", opacity_changed);
		mmodel.off("change:rgba255", rgba255_changed);
		mmodel.off("change:visible", visible_changed);
	};
}

/**
 * Create a new NVMesh and attach the necessary event listeners
 * Returns the NVMesh and a cleanup function that removes the event listeners.
 */
export async function create_mesh(
	nv: niivue.Niivue,
	mmodel: MeshModel,
): Promise<[niivue.NVMesh, () => void]> {
	let mesh: niivue.NVMesh;
	const layerCleanupFunctions: (() => void)[] = [];

	if (mmodel.get("path").name === "<fromfrontend>") {
		const idx = nv.meshes.findIndex((m) => m.id === mmodel.get("id"));
		mesh = nv.meshes[idx];
	} else {
		mesh = await niivue.NVMesh.readMesh(
			mmodel.get("path").data.buffer as ArrayBuffer, // buffer
			mmodel.get("path").name, // name (used to identify the mesh)
			nv.gl, // gl
			mmodel.get("opacity"), // opacity
			new Uint8Array(mmodel.get("rgba255")), // rgba255
			mmodel.get("visible"), // visible
		);
	}

	// Gather MeshLayer models
	const layerIDs = mmodel.get("layers");

	if (layerIDs.length > 0) {
		// Use gather_models to fetch the MeshLayerModel instances
		const layerModels: MeshLayerModel[] =
			await lib.gather_models<MeshLayerModel>(mmodel, layerIDs);

		// Add layers to the mesh
		layerModels.forEach(async (layerModel, layerIndex) => {
			// biome-ignore lint/suspicious/noExplicitAny: NVMeshLayer isn't exported from niivue
			let layer: any;
			if (
				layerModel.get("path").name !== "<fromfrontend>" &&
				layerModel.get("id") === ""
			) {
				layer = await niivue.NVMeshLoaders.readLayer(
					layerModel.get("path").name,
					layerModel.get("path").data.buffer,
					mesh,
					layerModel.get("opacity") ?? 0.5,
					layerModel.get("colormap") ?? "warm",
					layerModel.get("colormap_negative") ?? "winter",
					layerModel.get("use_negative_cmap") ?? false,
					layerModel.get("cal_min") ?? null,
					layerModel.get("cal_max") ?? null,
					layerModel.get("outline_border") ?? 0,
				);

				layer.id = uuidv4();
				mesh.layers.push(layer);
				layerModel.set("id", layer.id);
				layerModel.save_changes();
			} else {
				const idx = mesh.layers.findIndex(
					// biome-ignore lint/suspicious/noExplicitAny: NVMeshLayer isn't exported from niivue
					(l: any) => l.id === layerModel.get("id"),
				);
				layer = mesh.layers[idx];
			}
			if (!layer) {
				return;
			}

			// Set up event listeners for the layer properties
			const cleanup_layer_listeners = setup_layer_property_listeners(
				layer,
				layerModel,
				mesh,
				nv,
			);
			layerCleanupFunctions.push(cleanup_layer_listeners);
		});
	}

	mesh.updateMesh(nv.gl);

	mmodel.set("id", mesh.id);
	mmodel.set("name", mesh.name);
	mmodel.save_changes();

	// Handle changes to the mesh properties
	const cleanup_mesh_listeners = setup_mesh_property_listeners(
		mesh,
		mmodel,
		nv,
	);

	return [
		mesh,
		() => {
			// Remove event listeners for mesh properties
			cleanup_mesh_listeners();
		},
	];
}

export async function render_meshes(
	nv: niivue.Niivue,
	model: Model,
	disposer: lib.Disposer,
) {
	const mmodels = await lib.gather_models<MeshModel>(
		model,
		model.get("_meshes"),
	);

	const backend_meshes = mmodels;
	const frontend_meshes = nv.meshes;

	const backend_mesh_map = new Map<string, MeshModel>();
	const frontend_mesh_map = new Map<string, niivue.NVMesh>();

	// Create backend mesh map
	let backendIndex = 0;
	for (const mmodel of backend_meshes) {
		const id = mmodel.get("id") || `__temp_id__${backendIndex}`;
		backend_mesh_map.set(id, mmodel);
		backendIndex++;
	}

	// Create frontend mesh map
	let frontendIndex = 0;
	for (const mesh of frontend_meshes) {
		const id = mesh.id || `__temp_id__${frontendIndex}`;
		frontend_mesh_map.set(id, mesh);
		frontendIndex++;
	}

	// add meshes
	for (const [id, mmodel] of backend_mesh_map.entries()) {
		const fromFrontend = mmodel.get("path").name === "<fromfrontend>";
		const inFrontend = frontend_mesh_map.has(id);
		const emptyId = mmodel.get("id") === "";

		if (fromFrontend && !inFrontend) {
			// Cleanup meshes from frontend that no longer exist in the frontend
			disposer.dispose(id);
		} else if (!inFrontend || emptyId || (fromFrontend && inFrontend)) {
			// Add or sync meshes as needed
			const [mesh, cleanup] = await create_mesh(nv, mmodel);
			disposer.register(mesh, cleanup);
			if (!fromFrontend) {
				nv.addMesh(mesh);
			}
		}
	}

	// remove meshes
	for (const [id, mesh] of frontend_mesh_map.entries()) {
		if (!backend_mesh_map.has(id)) {
			// Remove mesh
			nv.removeMesh(mesh);
			disposer.dispose(mesh.id);
		}
	}

	// match frontend mesh order to backend order
	const new_meshes_order: niivue.NVMesh[] = [];
	let backendOrderIndex = 0;
	for (const mmodel of backend_meshes) {
		const id = mmodel.get("id") || "";
		const mesh = nv.meshes.find((m: niivue.NVMesh) => m.id === id);
		if (mesh) {
			new_meshes_order.push(mesh);
		} else {
			// handle case where mesh was just added and id isn't set yet
			const temp_id = `__temp_id__${backendOrderIndex}`;
			const mesh_temp = nv.meshes.find((m: niivue.NVMesh) => m.id === temp_id);
			if (mesh_temp) {
				new_meshes_order.push(mesh_temp);
			}
		}
		backendOrderIndex++;
	}
	nv.meshes = new_meshes_order;
	nv.updateGLVolume();
}
