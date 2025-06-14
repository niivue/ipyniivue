import type { AnyModel } from "@anywidget/types";

interface File {
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

export type VolumeModel = AnyModel<{
	path: File;
	id: string;
	name: string;
	colormap: string;
	opacity: number;
	visible: boolean;
	colorbar_visible: boolean;
	cal_min: number;
	cal_max: number;
	frame4D: number;
	colormap_negative: string;
	// biome-ignore lint/suspicious/noExplicitAny: LUT or ColorMap type
	colormap_label: any;

	colormap_invert: boolean;
}>;

export type MeshModel = AnyModel<{
	path: File;
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
	path: File;
	id: string;
	opacity: number;
	colormap: string;
	colormap_negative: string;
	use_negative_cmap: boolean;
	cal_min: number;
	cal_max: number;
	outline_border: number;

	colormap_invert: boolean;
	frame4D: number;
	colorbar_visible: boolean;
}>;

export type Model = AnyModel<{
	id: string;
	height: number;
	_volumes: Array<string>;
	_meshes: Array<string>;
	_opts: Record<string, unknown>;

	background_masks_overlays: number;
	clip_plane_depth_azi_elev: [
		depth: number,
		azimuth: number,
		elevation: number,
	];
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
	  };

type SetColormapLabelData = [cm: ColorMap];

export type CustomMessagePayloadVolume = {
	type: "set_colormap_label";
	data: SetColormapLabelData;
};
