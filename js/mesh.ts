import * as niivue from "@niivue/niivue";
import * as lib from "./lib.ts";
import type { MeshModel, Model } from "./types.ts";

/**
 * Create a new NVMesh and attach the necessary event listeners
 * Returns the NVMesh and a cleanup function that removes the event listeners.
 */
function create_mesh(
	nv: niivue.Niivue,
	mmodel: MeshModel,
): [niivue.NVMesh, () => void] {
	const mesh = niivue.NVMesh.readMesh(
		mmodel.get("path").data.buffer, // buffer
		mmodel.get("path").name, // name (used to identify the mesh)
		nv.gl, // gl
		mmodel.get("opacity"), // opacity
		new Uint8Array(mmodel.get("rgba255")), // rgba255
		mmodel.get("visible"), // visible
	);
	for (const layer of mmodel.get("layers")) {
		// https://github.com/niivue/niivue/blob/10d71baf346b23259570d7b2aa463749adb5c95b/src/nvmesh.ts#L1432C5-L1455C6
		niivue.NVMeshLoaders.readLayer(
			layer.path.name,
			layer.path.data.buffer,
			mesh,
			layer.opacity ?? 0.5,
			layer.colormap ?? "warm",
			layer.colormapNegative ?? "winter",
			layer.useNegativeCmap ?? false,
			layer.cal_min ?? null,
			layer.cal_max ?? null,
		);
	}
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
	const curr_names = nv.meshes.map((m) => m.name);
	const new_names = mmodels.map(lib.unique_id);
	const update_type = lib.determine_update_type(curr_names, new_names);
	if (update_type === "add") {
		// We know that the new meshes are the same as the old meshes,
		// except for the last one. We can just add the last mesh.
		const mmodel = mmodels[mmodels.length - 1];
		const [mesh, cleanup] = create_mesh(nv, mmodel);
		disposer.register(mesh, cleanup);
		nv.addMesh(mesh);
		return;
	}

	// If we can't determine the update type, we need
	// to remove all the meshes
	disposer.disposeAll("mesh");

	// create each mesh and add one-by-one
	for (const mmodel of mmodels) {
		const [mesh, cleanup] = create_mesh(nv, mmodel);
		disposer.register(mesh, cleanup);
		nv.addMesh(mesh);
	}
}
