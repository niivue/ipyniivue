import type { AnyModel } from "@anywidget/types";

interface File {
	name: string;
	data: DataView;
}

export type VolumeModel = { model_id: string } & AnyModel<{
	path: File;
	colormap: string;
	opacity: number;
	visible: boolean;
	colorbar_visible: boolean;
	cal_min?: number;
	cal_max?: number;
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

export type MeshModel = { model_id: string } & AnyModel<{
	path: File;
	rgba255: Array<number>;
	opacity: number;
	layers: Array<MeshLayer>;
	visible: boolean;
	fiber_radius: number;
	fiber_length: number;
	fiber_dither: number;
	fiber_color: string;
	fiber_decimation: number;
}>;

export type Model = AnyModel<{
	height: number;
	_volumes: Array<string>;
	_meshes: Array<string>;
	_opts: Record<string, unknown>;
	clipplane: Array<number>;
}>;
