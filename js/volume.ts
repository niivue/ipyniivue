import * as niivue from "@niivue/niivue";
import * as lib from "./lib.ts";
import type { Model, VolumeModel } from "./types.ts";

/**
 * Set up event listeners to handle changes to the volume properties.
 * Returns a function to clean up the event listeners.
 */
function setup_volume_property_listeners(
	volume: niivue.NVImage,
	vmodel: VolumeModel,
	nv: niivue.Niivue,
): () => void {
	function colorbar_visible_changed() {
		volume.colorbarVisible = vmodel.get("colorbar_visible");
		nv.updateGLVolume();
	}

	function cal_min_changed() {
		volume.cal_min = vmodel.get("cal_min");
		nv.updateGLVolume();
	}

	function cal_max_changed() {
		volume.cal_max = vmodel.get("cal_max");
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

	function frame4D_changed() {
		volume.frame4D = vmodel.get("frame4D");
		nv.updateGLVolume();
	}

	function colormap_negative_changed() {
		volume.colormapNegative = vmodel.get("colormap_negative");
		nv.updateGLVolume();
	}

	// Accept either LUT or colormap as input
	function colormap_label_changed() {
		const newColormapLabel = vmodel.get("colormap_label");
		if (newColormapLabel && Array.isArray(newColormapLabel.lut)) {
			newColormapLabel.lut = new Uint8ClampedArray(newColormapLabel.lut);
			volume.colormapLabel = newColormapLabel;
		}
		nv.updateGLVolume();
	}

	// other props
	function colormap_invert_changed() {
		volume.colormapInvert = vmodel.get("colormap_invert");
		nv.updateGLVolume();
	}

	// set values not set by kwargs
	colormap_invert_changed();

	vmodel.on("change:colorbar_visible", colorbar_visible_changed);
	vmodel.on("change:cal_min", cal_min_changed);
	vmodel.on("change:cal_max", cal_max_changed);
	vmodel.on("change:colormap", colormap_changed);
	vmodel.on("change:opacity", opacity_changed);
	vmodel.on("change:frame4D", frame4D_changed);
	vmodel.on("change:colormap_negative", colormap_negative_changed);
	vmodel.on("change:colormap_label", colormap_label_changed);

	vmodel.on("change:colormap_invert", colormap_invert_changed);

	return () => {
		vmodel.off("change:colorbar_visible", colorbar_visible_changed);
		vmodel.off("change:cal_min", cal_min_changed);
		vmodel.off("change:cal_max", cal_max_changed);
		vmodel.off("change:colormap", colormap_changed);
		vmodel.off("change:opacity", opacity_changed);
		vmodel.off("change:frame4D", frame4D_changed);
		vmodel.off("change:colormap_negative", colormap_negative_changed);
		vmodel.off("change:colormap_label", colormap_label_changed);

		vmodel.off("change:colormap_invert", colormap_invert_changed);
	};
}

/**
 * Create a new NVImage and attach the necessary event listeners
 * Returns the NVImage and a cleanup function that removes the event listeners.
 */
async function create_volume(
	nv: niivue.Niivue,
	vmodel: VolumeModel,
): Promise<[niivue.NVImage, () => void]> {
	let volume: niivue.NVImage;
	if (vmodel.get("path").name === "<fromfrontend>") {
		const idx = nv.getVolumeIndexByID(vmodel.get("id"));
		volume = nv.volumes[idx];
	} else {
		volume = await niivue.NVImage.new(
			vmodel.get("path").data.buffer as ArrayBuffer, // dataBuffer
			vmodel.get("path").name, // name
			vmodel.get("colormap"), // colormap
			vmodel.get("opacity"), // opacity
			null, // pairedImgData
			vmodel.get("cal_min") ?? Number.NaN, // cal_min
			vmodel.get("cal_max") ?? Number.NaN, // cal_max
			true, // trustCalMinMax
			0.02, // percentileFrac
			false, // ignoreZeroVoxels
			false, // useQFormNotSForm
			vmodel.get("colormap_negative"), // colormapNegative
			vmodel.get("frame4D"), // frame4D
			0, // imageType
			Number.NaN, // cal_minNeg
			Number.NaN, // cal_maxNeg
			vmodel.get("colorbar_visible"), // colorbarVisible
			null, // colormapLabel
			0, //colormapType
			null, //zarrData
		);

		// Set colormap label
		const newColormapLabel = vmodel.get("colormap_label");
		if (newColormapLabel && Array.isArray(newColormapLabel.lut)) {
			newColormapLabel.lut = new Uint8ClampedArray(newColormapLabel.lut);
			volume.colormapLabel = newColormapLabel;
		}
	}

	vmodel.set("id", volume.id);
	vmodel.set("name", volume.name);
	vmodel.save_changes();

	// Handle changes to the volume properties
	const cleanup_volume_listeners = setup_volume_property_listeners(
		volume,
		vmodel,
		nv,
	);

	return [
		volume,
		() => {
			// Remove event listeners for volume properties
			cleanup_volume_listeners();
		},
	];
}

export async function render_volumes(
	nv: niivue.Niivue,
	model: Model,
	disposer: lib.Disposer,
) {
	const vmodels = await lib.gather_models<VolumeModel>(
		model,
		model.get("volumes"),
	);

	const backend_volumes = vmodels;
	const frontend_volumes = nv.volumes;

	const backend_volume_map = new Map<string, VolumeModel>();
	const frontend_volume_map = new Map<string, niivue.NVImage>();

	// create backend volume map, use 'id' value if available, otherwise use temp key
	let backendIndex = 0;
	for (const vmodel of backend_volumes) {
		const id = vmodel.get("id") || `__temp_id__${backendIndex}`;
		backend_volume_map.set(id, vmodel);
		backendIndex++;
	}

	// create frontend volume map
	let frontendIndex = 0;
	for (const volume of frontend_volumes) {
		const id = volume.id || `__temp_id__${frontendIndex}`;
		frontend_volume_map.set(id, volume);
		frontendIndex++;
	}

	console.log("render_volumes called");
	console.log("backend_volumes:", backend_volumes, backend_volumes.length);
	console.log("frontend_volumes:", frontend_volumes, frontend_volumes.length);

	// add volumes
	for (const [id, vmodel] of backend_volume_map.entries()) {
		const fromFrontend = vmodel.get("path").name === "<fromfrontend>";
		const inFrontend = frontend_volume_map.has(id);
		const emptyId = vmodel.get("id") === "";

		if (fromFrontend && !inFrontend) {
			// Cleanup volumes from frontend that no longer exist in the frontend
			disposer.dispose(id);
		} else if (!inFrontend || emptyId || (fromFrontend && inFrontend)) {
			// Add volumes that are missing or need syncing
			const [volume, cleanup] = await create_volume(nv, vmodel);
			disposer.register(volume, cleanup);
			if (!fromFrontend) {
				nv.addVolume(volume);
			}
		}
	}

	// remove volumes
	for (const [id, volume] of frontend_volume_map.entries()) {
		if (!backend_volume_map.has(id)) {
			// case: volume is in frontend but not in backend
			// result: remove volume
			nv.removeVolume(volume);
			disposer.dispose(volume.id);
		}
	}

	// match frontend volume order to backend order
	const new_volumes_order: niivue.NVImage[] = [];
	let backendOrderIndex = 0;
	for (const vmodel of backend_volumes) {
		const id = vmodel.get("id") || "";
		const volume = nv.volumes.find((v: niivue.NVImage) => v.id === id);
		if (volume) {
			new_volumes_order.push(volume);
		} else {
			// handle case where volume was just added and id isn't set yet
			const temp_id = `__temp_id__${backendOrderIndex}`;
			const volume_temp = nv.volumes.find(
				(v: niivue.NVImage) => v.id === temp_id,
			);
			if (volume_temp) {
				new_volumes_order.push(volume_temp);
			}
		}
		backendOrderIndex++;
	}
	nv.volumes = new_volumes_order;
	nv.updateGLVolume();
}
