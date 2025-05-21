import type { AnyModel } from "@anywidget/types";
import type { Model, VolumeModel } from "./types.ts";

/**
 * Generates a unique file name for a volume (using the model id and the volume path)
 *
 * We need to keep track of the volumes from Python somehow, and the model_id is unique
 * to the volume sent from Python. This function generates a new filename for the volume
 * using the existing filename and model
 */
export function unique_id(vmodel: VolumeModel): string {
	const id = vmodel.get("id");
	const path = vmodel.get("path");
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
 * A class to keep track of disposers for callbacks for updating the scene.
 */
export class Disposer {
	#disposers = new Map<string, () => void>();

	register(
		obj: { id: string } | { id: string | undefined },
		disposer: () => void,
	): void {
		const id = obj.id || "";
		this.#disposers.set(id, disposer);
	}

	dispose(id: string): void {
		const dispose = this.#disposers.get(id);
		if (dispose) {
			dispose();
			this.#disposers.delete(id);
		}
	}

	disposeAll(): void {
		for (const dispose of this.#disposers.values()) {
			dispose();
		}
		this.#disposers.clear();
	}
}
