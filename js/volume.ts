import * as niivue from "@niivue/niivue";
import * as lib from "./lib.ts";
import type { Model, TypedBufferPayload, VolumeModel } from "./types.ts";

import type { NIFTI1, NIFTI2 } from "nifti-reader-js";

function getNIFTIData(hdr: NIFTI1 | NIFTI2): Partial<NIFTI1> {
	const data: Partial<NIFTI1> = {
		littleEndian: hdr.littleEndian,
		dim_info: hdr.dim_info,
		dims: hdr.dims,
		intent_p1: hdr.intent_p1,
		intent_p2: hdr.intent_p2,
		intent_p3: hdr.intent_p3,
		intent_code: hdr.intent_code,
		datatypeCode: hdr.datatypeCode,
		numBitsPerVoxel: hdr.numBitsPerVoxel,
		slice_start: hdr.slice_start,
		slice_end: hdr.slice_end,
		slice_code: hdr.slice_code,
		pixDims: hdr.pixDims,
		vox_offset: hdr.vox_offset,
		scl_slope: hdr.scl_slope,
		scl_inter: hdr.scl_inter,
		xyzt_units: hdr.xyzt_units,
		cal_max: hdr.cal_max,
		cal_min: hdr.cal_min,
		slice_duration: hdr.slice_duration,
		toffset: hdr.toffset,
		description: hdr.description,
		aux_file: hdr.aux_file,
		intent_name: hdr.intent_name,
		qform_code: hdr.qform_code,
		sform_code: hdr.sform_code,
		quatern_b: hdr.quatern_b,
		quatern_c: hdr.quatern_c,
		quatern_d: hdr.quatern_d,
		qoffset_x: hdr.qoffset_x,
		qoffset_y: hdr.qoffset_y,
		qoffset_z: hdr.qoffset_z,
		affine: hdr.affine,
		magic: hdr.magic,
		extensionFlag: hdr.extensionFlag,
	};

	return data;
}

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

	function frame_4d_changed() {
		volume.frame4D = vmodel.get("frame_4d");
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

	// custom msgs
	function customMessageHandler(
		payload: TypedBufferPayload,
		buffers: DataView[],
	) {
		const handled = lib.handleBufferMsg(volume, payload, buffers, () =>
			nv.updateGLVolume(),
		);
		if (handled) {
			return;
		}
	}

	// set values not set by kwargs
	colormap_invert_changed();

	vmodel.on("change:colorbar_visible", colorbar_visible_changed);
	vmodel.on("change:cal_min", cal_min_changed);
	vmodel.on("change:cal_max", cal_max_changed);
	vmodel.on("change:colormap", colormap_changed);
	vmodel.on("change:opacity", opacity_changed);
	vmodel.on("change:frame_4d", frame_4d_changed);
	vmodel.on("change:colormap_negative", colormap_negative_changed);
	vmodel.on("change:colormap_label", colormap_label_changed);

	vmodel.on("change:colormap_invert", colormap_invert_changed);

	vmodel.on("msg:custom", customMessageHandler);

	return () => {
		vmodel.off("change:colorbar_visible", colorbar_visible_changed);
		vmodel.off("change:cal_min", cal_min_changed);
		vmodel.off("change:cal_max", cal_max_changed);
		vmodel.off("change:colormap", colormap_changed);
		vmodel.off("change:opacity", opacity_changed);
		vmodel.off("change:frame_4d", frame_4d_changed);
		vmodel.off("change:colormap_negative", colormap_negative_changed);
		vmodel.off("change:colormap_label", colormap_label_changed);

		vmodel.off("change:colormap_invert", colormap_invert_changed);

		vmodel.off("msg:custom", customMessageHandler);
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

	// Input data
	const fromFrontend = vmodel.get("path").name === "<fromfrontend>";

	const path = vmodel.get("path").name ? vmodel.get("path") : null;
	const url = vmodel.get("url");
	const data = vmodel.get("data")?.byteLength ? vmodel.get("data") : null;

	const paired_img_path = vmodel.get("paired_img_path").name
		? vmodel.get("paired_img_path")
		: null;
	const paired_img_url = vmodel.get("paired_img_url") ?? "";
	const paired_img_data = vmodel.get("paired_img_data")?.byteLength
		? vmodel.get("paired_img_data")
		: null;

	// Paired image data
	let pairedImgData: ArrayBuffer | null = null;
	if (paired_img_data) {
		pairedImgData = paired_img_data.buffer as ArrayBuffer;
	} else if (paired_img_path) {
		pairedImgData = paired_img_path.data.buffer as ArrayBuffer;
	}

	if (fromFrontend) {
		const idx = nv.getVolumeIndexByID(vmodel.get("id"));
		volume = nv.volumes[idx];
	} else if (path || data) {
		const dataBuffer = path?.data?.buffer || data?.buffer;
		const name = path?.name || vmodel.get("name");
		volume = await niivue.NVImage.new(
			dataBuffer as ArrayBuffer,
			name,
			vmodel.get("colormap"),
			vmodel.get("opacity"),
			pairedImgData,
			vmodel.get("cal_min") ?? Number.NaN,
			vmodel.get("cal_max") ?? Number.NaN,
			true,
			0.02,
			false,
			false,
			vmodel.get("colormap_negative"),
			vmodel.get("frame_4d"),
			0,
			Number.NaN,
			Number.NaN,
			vmodel.get("colorbar_visible"),
			null,
			0,
			null,
		);
	} else if (url) {
		volume = await niivue.NVImage.loadFromUrl({
			url: url,
			name: vmodel.get("name"),
			colormap: vmodel.get("colormap"),
			opacity: vmodel.get("opacity"),
			urlImgData: paired_img_url,
			cal_min: vmodel.get("cal_min") ?? Number.NaN,
			cal_max: vmodel.get("cal_max") ?? Number.NaN,
			trustCalMinMax: true,
			percentileFrac: 0.02,
			ignoreZeroVoxels: false,
			useQFormNotSForm: false,
			colormapNegative: vmodel.get("colormap_negative"),
			frame4D: vmodel.get("frame_4d"),
			imageType: 0,
			colorbarVisible: vmodel.get("colorbar_visible"),
		});
	} else {
		throw new Error("Invalid source for volume");
	}

	// Set colormap label
	const newColormapLabel = vmodel.get("colormap_label");
	if (newColormapLabel && Array.isArray(newColormapLabel.lut)) {
		newColormapLabel.lut = new Uint8ClampedArray(newColormapLabel.lut);
		volume.colormapLabel = newColormapLabel;
	}

	vmodel.set("id", volume.id);
	vmodel.set("n_frame_4d", volume.nFrame4D ?? null);
	vmodel.set("colormap", volume.colormap);
	if (volume.hdr !== null) {
		vmodel.set("hdr", getNIFTIData(volume.hdr));
	}
	vmodel.save_changes();
	if (volume.img) {
		const dataType = lib.getArrayType(volume.img);
		lib.sendChunkedData(
			vmodel,
			"img",
			volume.img.buffer as ArrayBuffer,
			dataType,
		);
	}

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
