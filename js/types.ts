import type { AnyModel as BaseAnyModel } from "@anywidget/types";
import type { NVConfigOptions } from "@niivue/niivue";
import type { NIFTI1 } from "nifti-reader-js";

export interface AnyModel<T extends object = object> extends BaseAnyModel<T> {
	send_sync_message(state: object, callbacks?: any): string;
	rememberLastUpdateFor(msgId: string): void;
	_comm_live: boolean;
	// marimo support, since marimo uses POST requests instead of websocket
	onChange: (value: Partial<T>) => void;
}

interface FileInput {
	name: string;
	data: DataView;
}

type ColorMap = {
	R: number[];
	G: number[];
	B: number[];
	A: number[];
	I: number[];
	min?: number;
	max?: number;
	labels?: string[];
};

type LUT = {
	lut: Uint8ClampedArray;
	min?: number;
	max?: number;
	labels?: string[];
};

type Graph = {
	LTWH: number[];
	opacity: number;
	vols: number[];
	autoSizeMultiplanar: boolean;
	normalizeValues: boolean;
	isRangeCalMinMax: boolean;

	plotLTWH?: number[];
	backColor?: number[];
	lineColor?: number[];
	textColor?: number[];
	lineThickness?: number;
	gridLineThickness?: number;
	lineAlpha?: number;
	lines?: number[][];
	selectedColumn?: number;
	lineRGB?: number[][];
};

export type VolumeModel = AnyModel<{
	path: FileInput;
	url: string;
	data: DataView;

	paired_img_path: FileInput;
	paired_img_url: string;
	paired_img_data: DataView;

	id: string;
	name: string;
	colormap: string;
	opacity: number;
	visible: boolean;
	colorbar_visible: boolean;
	cal_min: number;
	cal_max: number;
	frame_4d: number;
	colormap_negative: string;
	colormap_label: LUT;

	colormap_invert: boolean;
	n_frame_4d: number | null;

	hdr: Partial<NIFTI1>;
}>;

export type MeshModel = AnyModel<{
	path: FileInput;
	id: string;
	name: string;
	rgba255: Array<number>;
	opacity: number;
	layers: Array<string>;
	visible: boolean;

	colormap_invert: boolean;
	colorbar_visible: boolean;
	mesh_shader_index: number;
	fiber_radius: number;
	fiber_length: number;
	fiber_dither: number;
	fiber_color: string;
	fiber_decimation_stride: number;
	colormap: string;
}>;

export type MeshLayerModel = AnyModel<{
	path: FileInput;
	id: string;
	opacity: number;
	colormap: string;
	colormap_negative: string;
	use_negative_cmap: boolean;
	cal_min: number;
	cal_max: number;
	outline_border: number;

	colormap_invert: boolean;
	frame_4d: number;
	colorbar_visible: boolean;
}>;

export type Model = AnyModel<{
	height: number;
	volumes: Array<string>;
	meshes: Array<string>;
	opts: Partial<Record<keyof NVConfigOptions, unknown>>;

	background_masks_overlays: number;
	clip_plane_depth_azi_elev: [
		depth: number,
		azimuth: number,
		elevation: number,
	];
	draw_lut: LUT;
	draw_opacity: number;
	draw_fill_overwrites: boolean;
	graph: Graph;
}>;

// Custom message datas
type SaveDocumentData = [fileName: string, compress: boolean];

type SaveHTMLData = [fileName: string, canvasId: string];

type SaveImageData = [
	filename: string,
	isSaveDrawing: boolean,
	volumeByIndex: number,
];

type SaveSceneData = [fileName: string];

type AddColormapData = [name: string, cmap: ColorMap];

type SetGammaData = [gamma: number];

type SetVolumeRenderIlluminationData = [gradientAmount: number];

type LoadPngAsTextureData = [pngUrl: string, textureNum: number];

type SetRenderAzimuthElevationData = [azimuth: number, elevation: number];

type SetInterpolationData = [isNearest: boolean];

type SetDrawingEnabledData = [drawingEnabled: boolean];

type DrawOtsuData = [levels: number];

type MoveCrosshairInVoxData = [x: number, y: number, z: number];

type RemoveHazeData = [level: number, volIndex: number];

type LoadDrawingFromUrlData = [url: string, isBinarize: boolean];

export type CustomMessagePayload =
	| { type: "save_document"; data: SaveDocumentData }
	| { type: "save_html"; data: SaveHTMLData }
	| { type: "save_image"; data: SaveImageData }
	| { type: "save_scene"; data: SaveSceneData }
	| { type: "add_colormap"; data: AddColormapData }
	| { type: "set_gamma"; data: SetGammaData }
	| { type: "resize_listener"; data: [] }
	| { type: "draw_scene"; data: [] }
	| {
			type: "set_volume_render_illumination";
			data: SetVolumeRenderIlluminationData;
	  }
	| { type: "load_png_as_texture"; data: LoadPngAsTextureData }
	| {
			type: "set_render_azimuth_elevation";
			data: SetRenderAzimuthElevationData;
	  }
	| { type: "set_interpolation"; data: SetInterpolationData }
	| { type: "set_drawing_enabled"; data: SetDrawingEnabledData }
	| { type: "draw_otsu"; data: DrawOtsuData }
	| { type: "draw_grow_cut"; data: [] }
	| { type: "move_crosshair_in_vox"; data: MoveCrosshairInVoxData }
	| { type: "remove_haze"; data: RemoveHazeData }
	| { type: "draw_undo"; data: [] }
	| { type: "close_drawing"; data: [] }
	| { type: "load_drawing_from_url"; data: LoadDrawingFromUrlData };
