import * as niivue from "@niivue/niivue";
import * as lib from "./lib.ts";
import type { MeshModel, Model } from "./types.ts";

/**
 * Create a new NVMesh and attach the necessary event listeners
 * Returns the NVMesh and a cleanup function that removes the event listeners.
 */
export async function create_mesh(
	nv: niivue.Niivue,
	mmodel: MeshModel,
): Promise<[niivue.NVMesh, () => void]> {
	let mesh: niivue.NVMesh;
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

	for (const layer of mmodel.get("layers")) {
		// https://github.com/niivue/niivue/blob/10d71baf346b23259570d7b2aa463749adb5c95b/src/nvmesh.ts#L1432C5-L1455C6
		niivue.NVMeshLoaders.readLayer(
			layer.path.name,
			layer.path.data.buffer as ArrayBuffer,
			mesh,
			layer.opacity ?? 0.5,
			layer.colormap ?? "warm",
			layer.colormapNegative ?? "winter",
			layer.useNegativeCmap ?? false,
			layer.cal_min ?? null,
			layer.cal_max ?? null,
		);
	}

	mesh.updateMesh(nv.gl);

	mmodel.set("id", mesh.id);
	mmodel.set("name", mesh.name);
	mmodel.save_changes();

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
	return [
		mesh,
		() => {
			mmodel.off("change:opacity", opacity_changed);
			mmodel.off("change:rgba255", rgba255_changed);
			mmodel.off("change:visible", visible_changed);
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
