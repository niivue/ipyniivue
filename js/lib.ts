import type { NVConfigOptions, Niivue } from "@niivue/niivue";
import type { AnyModel, TypedBufferPayload, PyScene, Model } from "./types.ts";

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

export function deserializeOptions(
	options: Partial<Record<keyof NVConfigOptions, unknown>>,
): NVConfigOptions {
	const result: Partial<NVConfigOptions> = {};
	const specialValues: Record<string, number> = {
		Infinity: Number.POSITIVE_INFINITY,
		"-Infinity": Number.NEGATIVE_INFINITY,
		NaN: Number.NaN,
		"-0": -0,
	};

	for (const [key, value] of Object.entries(options) as [
		keyof NVConfigOptions,
		unknown,
	][]) {
		if (typeof value === "string" && value in specialValues) {
			// biome-ignore lint/suspicious/noExplicitAny: NVConfigOptions
			(result as any)[key] = specialValues[value];
		} else {
			// biome-ignore lint/suspicious/noExplicitAny: NVConfigOptions
			(result as any)[key] = value;
		}
	}

	return result as NVConfigOptions;
}

export function handleBufferMsg(
	// biome-ignore lint/suspicious/noExplicitAny: targetObject can be any
	targetObject: any,
	payload: TypedBufferPayload,
	buffers: DataView[],
	callback: () => void,
): boolean {
	const { type, data } = payload;

	switch (type) {
		case "buffer_change": {
			const attrName = data.attr;
			const dataType = data.type;
			const buffer = buffers[0].buffer;
			const TypedArrayConstructor = getTypedArrayConstructor(dataType);
			const typedArray = new TypedArrayConstructor(buffer);

			targetObject[attrName] = typedArray;

			callback();

			return true;
		}
		case "buffer_update": {
			const attrName = data.attr;
			const dataType = data.type;
			const indicesType = data.indices_type;
			const [indicesBuffer, valuesBuffer] = [
				buffers[0].buffer,
				buffers[1].buffer,
			];

			const IndicesArrayConstructor = getTypedArrayConstructor(indicesType);
			const ValuesArrayConstructor = getTypedArrayConstructor(dataType);

			const indicesArray = new IndicesArrayConstructor(indicesBuffer);
			const valuesArray = new ValuesArrayConstructor(valuesBuffer);

			const existingArray = targetObject[attrName] as TypedArray;

			if (!existingArray || existingArray.length === 0) {
				console.error(
					`Existing array ${attrName} is empty or not initialized.`,
				);
				return true;
			}

			applyDifferencesToTypedArray(existingArray, indicesArray, valuesArray);

			callback();

			return true;
		}
		default:
			return false;
	}
}

export type TypedArray =
	| Float32Array
	| Uint32Array
	| Uint8Array
	| Int16Array
	| Float64Array
	| Uint16Array;

type TypedArrayConstructor<T extends TypedArray = TypedArray> = new (
	buffer: ArrayBufferLike,
) => T;

const typeMapping: { [key: string]: TypedArrayConstructor } = {
	float32: Float32Array,
	uint32: Uint32Array,
	uint8: Uint8Array,
	int16: Int16Array,
	float64: Float64Array,
	uint16: Uint16Array,
};

const reverseTypeMapping = new Map<TypedArrayConstructor, string>(
	Object.entries(typeMapping).map(([typeStr, c]) => [c, typeStr]),
);

export function getArrayType(typedArray: TypedArray): string {
	for (const typeStr in typeMapping) {
		const c = typeMapping[typeStr];
		if (typedArray instanceof c) {
			return typeStr;
		}
	}
	throw new Error("Unsupported array type");
}

export function getTypedArrayConstructor(
	typeStr: string,
): TypedArrayConstructor {
	const c = typeMapping[typeStr];
	if (c) {
		return c;
	}
	throw new Error(`Unsupported data type: ${typeStr}`);
}

export function deserializeBufferToTypedArray(
	buffer: ArrayBuffer,
	typeStr: string,
): TypedArray {
	const TypedArrayConstructor = getTypedArrayConstructor(typeStr);
	return new TypedArrayConstructor(buffer);
}

export function applyDifferencesToTypedArray(
	array: TypedArray,
	indices: TypedArray,
	values: TypedArray,
): void {
	for (let i = 0; i < indices.length; i++) {
		const idx = indices[i];
		array[idx] = values[i];
	}
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
	// biome-ignore lint/suspicious/noExplicitAny: we know the type of the models
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