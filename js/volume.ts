import * as niivue from "@niivue/niivue";
import * as lib from "./lib.ts";
import type { Model, VolumeModel } from "./types.ts";

/**
 * Create a new NVImage and attach the necessary event listeners
 * Returns the NVImage and a cleanup function that removes the event listeners.
 */
function create_volume(
	nv: niivue.Niivue,
	vmodel: VolumeModel,
): [niivue.NVImage, () => void] {
	const volume = new niivue.NVImage(
		vmodel.get("path").data.buffer, // dataBuffer
		lib.unique_id(vmodel), // name
		vmodel.get("colormap"), // colormap
		vmodel.get("opacity"), // opacity
		undefined, // pairedImgData
		vmodel.get("cal_min"), // cal_min
		vmodel.get("cal_max"), // cal_max
		undefined, // trustMinCalMinMax
		undefined, // percentileFrac
		undefined, // ignoreZeroVoxels
		undefined, // useQFormNotSForm
		undefined, // colormapNegative
		undefined, // frame4D
		undefined, // imageType
		undefined, // cal_minNeg
		undefined, // cal_maxNeg
		vmodel.get("colorbar_visible"), // colorbarVisible
		undefined, // colormapLabel
	);
	function colorbar_visible_changed() {
		volume.colorbarVisible = vmodel.get("colorbar_visible");
		nv.updateGLVolume();
	}
	function cal_min_changed() {
		volume.cal_min = vmodel.get("cal_min");
		nv.updateGLVolume();
	}
	function cal_max_changed() {
		volume.cal_min = vmodel.get("cal_min");
		nv.updateGLVolume();
	}
	function colormap_changed() {
		volume.colormap = vmodel.get("colormap");
		nv.updateGLVolume();
	}
	function opacity_changed() {
		volume.opacity = vmodel.get("opacity");
		nv.updateGLVolume();
	}
	vmodel.on("change:colorbar_visible", colorbar_visible_changed);
	vmodel.on("change:cal_min", cal_min_changed);
	vmodel.on("change:cal_max", cal_max_changed);
	vmodel.on("change:colormap", colormap_changed);
	vmodel.on("change:opacity", opacity_changed);
	return [
		volume,
		() => {
			vmodel.off("change:colorbar_visible", colorbar_visible_changed);
			vmodel.off("change:cal_min", cal_min_changed);
			vmodel.off("change:cal_max", cal_max_changed);
			vmodel.off("change:colormap", colormap_changed);
			vmodel.off("change:opacity", opacity_changed);
		},
	];
}

export async function render_volumes(
	nv: niivue.Niivue,
	model: Model,
	cleanups: Map<string, () => void>,
) {
	const vmodels = await lib.gather_models<VolumeModel>(
		model,
		model.get("_volumes"),
	);
	const curr_names = nv.volumes.map((v) => v.name);
	const new_names = vmodels.map(lib.unique_id);
	const update_type = lib.determine_update_type(curr_names, new_names);
	if (update_type === "add") {
		// We know that the new volumes are the same as the old volumes,
		// except for the last one. We can just add the last volume.
		const vmodel = vmodels[vmodels.length - 1];
		const [volume, cleanup] = create_volume(nv, vmodel);
		cleanups.set(volume.id, cleanup);
		nv.addVolume(volume);
		return;
	}
	// HERE can be the place to add more update types
	// ...

	// We don't know what the update type is, so we need to remove all volumes
	// and add the new ones.

	// clear all volumes
	for (const [_, cleanup] of cleanups) cleanup();
	cleanups.clear();

	// create each volume and add one-by-one
	for (const vmodel of vmodels) {
		const [volume, cleanup] = create_volume(nv, vmodel);
		cleanups.set(volume.id, cleanup);
		nv.addVolume(volume);
	}
}
