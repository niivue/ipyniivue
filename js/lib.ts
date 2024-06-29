import type { AnyModel } from "@anywidget/types";
import * as nv from "@niivue/niivue";
import type { Model } from "./types.ts";

/**
 * Generates a unique file name for a volume (using the model id and the volume path)
 *
 * We need to keep track of the volumes from Python somehow, and the model_id is unique
 * to the volume sent from Python. This function generates a new filename for the volume
 * using the existing filename and model
 */
export function unique_id(model: {
	model_id: string;
	get(name: "path"): { name: string };
}): string {
	const path = model.get("path");
	// take the first 6 characters of the model_id, it should be unique enough
	const id = model.model_id.slice(0, 6);
	return `${id}:${path.name}`;
}

export function gather_models<T extends AnyModel>(
	model: Model,
	ids: Array<string>,
): Promise<Array<T>> {
	// biome-ignore lint/suspicious/noExplicitAny:  we know the type of the models
	const models: Array<Promise<any>> = [];
	const widget_manager = model.widget_manager;
	for (const id of ids) {
		const model_id = id.slice("IPY_MODEL_".length);
		models.push(widget_manager.get_model(model_id));
	}
	return Promise.all(models);
}

/**
 * Determine what type of update is necessary to go from `old_arr` to `new_arr`.
 *
 * If cannot determine the update type, return "unknown". Only "add" is supported
 * for now.
 */
export function determine_update_type<T>(
	old_arr: Array<T>,
	new_arr: Array<T>,
): "add" | "unknown" {
	if (
		old_arr.length === new_arr.length - 1 &&
		old_arr.every((v, i) => new_arr[i] === v)
	) {
		return "add";
	}
	return "unknown";
}

/**
 * A class to keep track of disposers for callbacks for updating the scene.
 */
export class Disposer {
	#disposers = new Map<string, () => void>();
	register(obj: nv.NVMesh | nv.NVImage, disposer: () => void): void {
		const prefix = obj instanceof nv.NVMesh ? "mesh" : "image";
		this.#disposers.set(`${prefix}:${obj.name}`, disposer);
	}
	disposeAll(kind?: "mesh" | "image"): void {
		for (const [name, dispose] of this.#disposers) {
			if (!kind || name.startsWith(kind)) {
				dispose();
				this.#disposers.delete(name);
			}
		}
	}
}
