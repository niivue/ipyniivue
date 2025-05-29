import type { AnyModel } from "@anywidget/types";

interface File {
	name: string;
	data: DataView;
}

export type VolumeModel = AnyModel<{
	path: File;
	id: string;
	name: string;
	colormap: string;
	opacity: number;
	visible: boolean;
	colorbar_visible: boolean;
	cal_min?: number;
	cal_max?: number;
	frame4D: number;
}>;

export type MeshModel = AnyModel<{
	path: File;
	id: string;
	name: string;
	rgba255: Array<number>;
	opacity: number;
	layers: Array<string>;
	visible: boolean;
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
}>;

export type Model = AnyModel<{
	id: string;
	height: number;
	_volumes: Array<string>;
	_meshes: Array<string>;
	_opts: Record<string, unknown>;
}>;

// Custom message datas
type SaveDocumentData = {
	fileName: string;
	compress: boolean;
};

type SaveHTMLData = {
	fileName: string;
	canvasId: string;
};

type SaveImageData = {
	fileName: string;
	saveDrawing: boolean;
	indexVolume: number;
};

type SaveSceneData = {
	fileName: string;
};

export type CustomMessagePayload =
	| { type: "save_document"; data: SaveDocumentData }
	| { type: "save_html"; data: SaveHTMLData }
	| { type: "save_image"; data: SaveImageData }
	| { type: "save_scene"; data: SaveSceneData };
