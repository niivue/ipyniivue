import type { AnyModel } from "@anywidget/types";

interface File {
	name: string;
	data: DataView;
}

export type VolumeModel = AnyModel<{
	path: File;
	id: string;
	colormap: string;
	opacity: number;
	visible: boolean;
	colorbar_visible: boolean;
	cal_min?: number;
	cal_max?: number;
	frame4D: number;
}>;

interface MeshLayer {
	path: File;
	opacity: number;
	colormap: string;
	colormapNegative: string;
	useNegativeCmap: boolean;
	cal_min?: number;
	cal_max?: number;
}

export type MeshModel = AnyModel<{
	path: File;
	id: string;
	rgba255: Array<number>;
	opacity: number;
	layers: Array<MeshLayer>;
	visible: boolean;
}>;

export type Model = AnyModel<{
	height: number;
	_volumes: Array<string>;
	_meshes: Array<string>;
	_opts: Record<string, unknown>;
}>;
