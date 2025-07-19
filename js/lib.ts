import type { AnyModel } from "./types.ts";

function delay(ms: number) {
	return new Promise((resolve) => setTimeout(resolve, ms));
}

function dataViewToBase64(dataView: DataView) {
	const uint8Array = new Uint8Array(dataView.buffer);
	let binaryString = "";
	const len = uint8Array.byteLength;
	for (let i = 0; i < len; i++) {
		binaryString += String.fromCharCode(uint8Array[i]);
	}
	return btoa(binaryString);
}

type TypedArray =
	| Float32Array
	| Uint32Array
	| Uint8Array
	| Int16Array
	| Float64Array
	| Uint16Array;

export function getArrayType(typedArray: TypedArray): string {
	if (typedArray instanceof Float32Array) return "float32";
	if (typedArray instanceof Uint32Array) return "uint32";
	if (typedArray instanceof Uint8Array) return "uint8";
	if (typedArray instanceof Int16Array) return "int16";
	if (typedArray instanceof Float64Array) return "float64";
	if (typedArray instanceof Uint16Array) return "uint16";
	throw new Error("Unsupported array type");
}

export async function sendChunkedData(
	model: AnyModel,
	dataProperty: string,
	arrayBuffer: ArrayBuffer,
	dataType: string,
	_chunkSize = 5 * 1024 * 1024,
	wait = 0,
) {
	const isMarimo = typeof model.send_sync_message === "undefined";

	const chunkSize = isMarimo
		? Math.min(_chunkSize, 2 * 1024 * 1024)
		: _chunkSize;

	const totalSize = arrayBuffer.byteLength;
	const totalChunks = Math.ceil(totalSize / chunkSize);
	let offset = 0;
	let chunkIndex = 0;

	while (offset < totalSize) {
		if (!isMarimo && !model._comm_live) {
			break;
		}

		const chunkEnd = Math.min(offset + chunkSize, totalSize);
		const chunk = arrayBuffer.slice(offset, chunkEnd);
		const chunkView = new DataView(chunk);

		const attributeName: string = `chunk_${dataProperty}_${chunkIndex}`;

		const data = {
			chunk_index: chunkIndex,
			total_chunks: totalChunks,
			data_type: dataType,
			chunk: isMarimo ? dataViewToBase64(chunkView) : chunkView,
		};
		const message: Record<string, object> = {};
		message[attributeName] = data;

		console.log("lib.sendChunkedData:", message);

		if (isMarimo) {
			model.onChange(message);
		} else {
			const msgId = model.send_sync_message(message);
			if (typeof model.rememberLastUpdateFor !== "undefined") {
				model.rememberLastUpdateFor(msgId);
			}
		}

		if (wait > 0) {
			await delay(wait);
		}

		offset = chunkEnd;
		chunkIndex += 1;
	}
}

export function gather_models<T extends AnyModel>(
	model: AnyModel,
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
