import type { AnyModel } from "@anywidget/types";

export type VolumeModel = { model_id: string } & AnyModel<{
	path: { name: string; data: DataView };
	colormap: string;
	opacity: number;
    colorbar_visible: boolean;
	cal_min?: number;
	cal_max?: number;
	visible: boolean;
}>;

export type Model = AnyModel<{
	_volumes: string[];
	_opts: Record<string, unknown>;
}>
