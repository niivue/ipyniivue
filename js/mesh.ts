import * as niivue from "@niivue/niivue";
import * as lib from "./lib.ts";
import type {
	MeshLayerModel,
	MeshModel,
	Model,
	TypedBufferPayload,
} from "./types.ts";

import { v4 as uuidv4 } from "@lukeed/uuid";

const pendingMeshIds = new Set<string>();

export function addPendingMeshId(volumeId: string) {
	pendingMeshIds.add(volumeId);
}

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

	function outline_border_changed() {
		layer.outlineBorder = layerModel.get("outline_border");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	// other props
	function colormap_invert_changed() {
		layer.colormapInvert = layerModel.get("colormap_invert");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	function frame_4d_changed() {
		layer.frame4D = layerModel.get("frame_4d");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	function colorbar_visible_changed() {
		layer.colorbarVisible = layerModel.get("colorbar_visible");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	// set values not set by kwargs
	colormap_invert_changed();
	frame_4d_changed();
	colorbar_visible_changed();

	// Set up the event listeners
	layerModel.on("change:opacity", opacity_changed);
	layerModel.on("change:colormap", colormap_changed);
	layerModel.on("change:colormap_negative", colormap_negative_changed);
	layerModel.on("change:use_negative_cmap", use_negative_cmap_changed);
	layerModel.on("change:cal_min", cal_min_changed);
	layerModel.on("change:cal_max", cal_max_changed);
	layerModel.on("change:outline_border", outline_border_changed);

	layerModel.on("change:colormap_invert", colormap_invert_changed);
	layerModel.on("change:frame_4d", frame_4d_changed);
	layerModel.on("change:colorbar_visible", colorbar_visible_changed);

	// Return a cleanup function
	return () => {
		layerModel.off("change:opacity", opacity_changed);
		layerModel.off("change:colormap", colormap_changed);
		layerModel.off("change:colormap_negative", colormap_negative_changed);
		layerModel.off("change:use_negative_cmap", use_negative_cmap_changed);
		layerModel.off("change:cal_min", cal_min_changed);
		layerModel.off("change:cal_max", cal_max_changed);
		layerModel.off("change:outline_border", outline_border_changed);

		layerModel.off("change:colormap_invert", colormap_invert_changed);
		layerModel.off("change:frame_4d", frame_4d_changed);
		layerModel.off("change:colorbar_visible", colorbar_visible_changed);
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

	// other props
	function colormap_invert_changed() {
		mesh.colormapInvert = mmodel.get("colormap_invert");
		nv.updateGLVolume();
	}

	function colorbar_visible_changed() {
		mesh.colorbarVisible = mmodel.get("colorbar_visible");
		nv.updateGLVolume();
	}

	function mesh_shader_index_changed() {
		mesh.meshShaderIndex = mmodel.get("mesh_shader_index");
		nv.updateGLVolume();
		const meshIndex = nv.getMeshIndexByID(mesh.id);
		nv.onMeshShaderChanged(meshIndex, mesh.meshShaderIndex);
	}

	function fiber_radius_changed() {
		mesh.fiberRadius = mmodel.get("fiber_radius");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	function fiber_length_changed() {
		mesh.fiberLength = mmodel.get("fiber_length");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	function fiber_dither_changed() {
		mesh.fiberDither = mmodel.get("fiber_dither");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	function fiber_color_changed() {
		mesh.fiberColor = mmodel.get("fiber_color");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	function fiber_decimation_stride_changed() {
		mesh.fiberDecimationStride = mmodel.get("fiber_decimation_stride");
		mesh.updateMesh(nv.gl);
		nv.updateGLVolume();
	}

	function colormap_changed() {
		mesh.colormap = mmodel.get("colormap");
		nv.updateGLVolume();
	}

	// custom msgs
	function customMessageHandler(
		payload: TypedBufferPayload,
		buffers: DataView[],
	) {
		const handled = lib.handleBufferMsg(mesh, payload, buffers, () => {
			if (nv._gl) {
				mesh.updateMesh(nv.gl);
				nv.updateGLVolume();
			}
		});
		if (handled) {
			return;
		}
	}

	// set values not set by kwargs
	colormap_invert_changed();
	colorbar_visible_changed();
	mesh_shader_index_changed();
	fiber_radius_changed();
	fiber_length_changed();
	fiber_dither_changed();
	fiber_color_changed();
	fiber_decimation_stride_changed();

	mmodel.on("change:opacity", opacity_changed);
	mmodel.on("change:rgba255", rgba255_changed);
	mmodel.on("change:visible", visible_changed);

	mmodel.on("change:colormap_invert", colormap_invert_changed);
	mmodel.on("change:colorbar_visible", colorbar_visible_changed);
	mmodel.on("change:mesh_shader_index", mesh_shader_index_changed);
	mmodel.on("change:fiber_radius", fiber_radius_changed);
	mmodel.on("change:fiber_length", fiber_length_changed);
	mmodel.on("change:fiber_dither", fiber_dither_changed);
	mmodel.on("change:fiber_color", fiber_color_changed);
	mmodel.on("change:fiber_decimation_stride", fiber_decimation_stride_changed);
	mmodel.on("change:colormap", colormap_changed);

	mmodel.on("msg:custom", customMessageHandler);

	// Return a function to remove the event listeners
	return () => {
		mmodel.off("change:opacity", opacity_changed);
		mmodel.off("change:rgba255", rgba255_changed);
		mmodel.off("change:visible", visible_changed);

		mmodel.off("change:colormap_invert", colormap_invert_changed);
		mmodel.off("change:colorbar_visible", colorbar_visible_changed);
		mmodel.off("change:mesh_shader_index", mesh_shader_index_changed);
		mmodel.off("change:fiber_radius", fiber_radius_changed);
		mmodel.off("change:fiber_length", fiber_length_changed);
		mmodel.off("change:fiber_dither", fiber_dither_changed);
		mmodel.off("change:fiber_color", fiber_color_changed);
		mmodel.off(
			"change:fiber_decimation_stride",
			fiber_decimation_stride_changed,
		);
		mmodel.off("change:colormap", colormap_changed);

		mmodel.off("msg:custom", customMessageHandler);
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

	// Input data
	const backendId = mmodel.get("id");
	const existingIdx = nv.getMeshIndexByID(backendId);

	const path = mmodel.get("path")?.name ? mmodel.get("path") : null;
	const url = mmodel.get("url");
	const data = mmodel.get("data")?.byteLength ? mmodel.get("data") : null;

	if (existingIdx !== -1) {
		mesh = nv.meshes[existingIdx];
	} else if (path || data) {
		const dataBuffer = path?.data?.buffer || data?.buffer;
		const name = path?.name || mmodel.get("name");
		mesh = await niivue.NVMesh.readMesh(
			dataBuffer as ArrayBuffer,
			name,
			nv.gl,
			mmodel.get("opacity"),
			new Uint8Array(mmodel.get("rgba255")),
			mmodel.get("visible"),
		);
		mesh.id = backendId;
	} else if (url) {
		mesh = await niivue.NVMesh.loadFromUrl({
			url: url,
			gl: nv.gl,
			name: mmodel.get("name"),
			opacity: mmodel.get("opacity") ?? 1.0,
			rgba255: mmodel.get("rgba255") ?? [255, 255, 255, 255],
			visible: mmodel.get("visible") ?? true,
			layers: [],
		});
		mesh.id = backendId;
	} else {
		throw new Error("Invalid source for mesh");
	}

	// Save the id and name back to the model
	mmodel.set("name", mesh.name);
	mmodel.save_changes();

	// Gather MeshLayer models
	const layerIDs = mmodel.get("layers");

	if (layerIDs.length > 0) {
		// Use gather_models to fetch the MeshLayerModel instances
		const layerModels: MeshLayerModel[] =
			await lib.gather_models<MeshLayerModel>(mmodel, layerIDs);

		// Process layers
		for (const layerModel of layerModels) {
			const layerPath = layerModel.get("path")?.name
				? layerModel.get("path")
				: null;
			const layerUrl = layerModel.get("url");
			const layerData = layerModel.get("data")?.byteLength
				? layerModel.get("data")
				: null;

			const backendLayerId = layerModel.get("id");
			const existingLayerIdx = mesh.layers.findIndex(
				// biome-ignore lint/suspicious/noExplicitAny: NVMeshLayer isn't exported from niivue
				(l) => (l as any).id === backendLayerId,
			);

			// biome-ignore lint/suspicious/noExplicitAny: NVMeshLayer isn't exported from niivue
			let layer: any;

			if (existingLayerIdx !== -1) {
				layer = mesh.layers[existingLayerIdx];
			} else if (layerPath || layerData) {
				const layerDataBuffer = layerPath?.data?.buffer || layerData?.buffer;
				const layerName = layerPath?.name || layerModel.get("name");
				layer = await niivue.NVMeshLoaders.readLayer(
					layerName || "",
					layerDataBuffer as ArrayBuffer,
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
			} else if (layerUrl) {
				const response = await fetch(layerUrl);
				if (!response.ok) {
					throw Error(response.statusText);
				}
				const layerDataBuffer = await response.arrayBuffer();
				const layerName = layerModel.get("name");
				layer = await niivue.NVMeshLoaders.readLayer(
					layerName,
					layerDataBuffer as ArrayBuffer,
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
				throw new Error("Invalid source for mesh layer");
			}

			if (!layer) {
				continue;
			}

			// Set up event listeners
			const cleanup_layer_listeners = setup_layer_property_listeners(
				layer,
				layerModel,
				mesh,
				nv,
			);
			layerCleanupFunctions.push(cleanup_layer_listeners);
		}
	}

	mesh.updateMesh(nv.gl);

	// Send other data back to the model
	if (mesh.extentsMin && Array.isArray(mesh.extentsMin)) {
		mmodel.set("extents_min", mesh.extentsMin);
	}
	if (mesh.extentsMax && Array.isArray(mesh.extentsMax)) {
		mmodel.set("extents_max", mesh.extentsMax);
	}
	mmodel.save_changes();

	// Send pts and tris back to the model
	if (mesh.pts) {
		const dataType = lib.getArrayType(mesh.pts);
		lib.sendChunkedData(
			mmodel,
			"pts",
			mesh.pts.buffer as ArrayBuffer,
			dataType,
		);
	}
	if (mesh.tris) {
		const dataType = lib.getArrayType(mesh.tris);
		lib.sendChunkedData(
			mmodel,
			"tris",
			mesh.tris.buffer as ArrayBuffer,
			dataType,
		);
	}

	// Handle changes to the mesh properties
	const cleanup_mesh_listeners = setup_mesh_property_listeners(
		mesh,
		mmodel,
		nv,
	);

	return [
		mesh,
		() => {
			// Remove event listeners for mesh properties and layers
			cleanup_mesh_listeners();
			for (const cleanup of layerCleanupFunctions) {
				cleanup();
			}
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
		model.get("meshes"),
	);

	const backend_meshes = mmodels;
	const frontend_meshes = nv.meshes;

	const backend_mesh_map = new Map<string, MeshModel>();
	const frontend_mesh_map = new Map<string, niivue.NVMesh>();

	// Create backend mesh map
	let backendIndex = 0;
	for (const mmodel of backend_meshes) {
		const id = mmodel.get("id");
		backend_mesh_map.set(id, mmodel);
		backendIndex++;
	}

	// Create frontend mesh map
	let frontendIndex = 0;
	for (const mesh of frontend_meshes) {
		const id = mesh.id;
		frontend_mesh_map.set(id, mesh);
		frontendIndex++;
	}

	console.log("render_meshes called");
	console.log("backend_meshes:", backend_meshes, backend_meshes.length);
	console.log("frontend_meshes:", frontend_meshes, frontend_meshes.length);

	// add meshes
	for (const [id, mmodel] of backend_mesh_map.entries()) {
		if (!disposer.has(id)) {
			// Add or sync meshes as needed
			const [mesh, cleanup] = await create_mesh(nv, mmodel);
			disposer.register(mesh, cleanup);

			if (!frontend_mesh_map.has(id)) {
				nv.addMesh(mesh);
			}
		}

		pendingMeshIds.delete(id);
	}

	// remove meshes
	for (const [id, mesh] of frontend_mesh_map.entries()) {
		if (!backend_mesh_map.has(id) && !pendingMeshIds.has(id)) {
			// Remove mesh
			nv.removeMesh(mesh);
			disposer.dispose(mesh.id);
		}
	}

	// match frontend mesh order to backend order
	const new_meshes_order: niivue.NVMesh[] = [];
	for (const mmodel of backend_meshes) {
		const id = mmodel.get("id");
		const mesh = nv.meshes.find((m: niivue.NVMesh) => m.id === id);
		if (mesh && !pendingMeshIds.has(id)) {
			new_meshes_order.push(mesh);
		}
	}

	// Add pending meshes that haven't synced to backend yet
	for (const mesh of nv.meshes) {
		if (pendingMeshIds.has(mesh.id)) {
			new_meshes_order.push(mesh);
		}
	}

	nv.meshes = new_meshes_order;

	nv.updateGLVolume();
}
