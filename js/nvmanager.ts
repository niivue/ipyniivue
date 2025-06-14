import type * as niivue from "@niivue/niivue";

const nvMapSymbol = Symbol.for("nvMap");

// biome-ignore lint/suspicious/noExplicitAny: globalThis
if (!(globalThis as any)[nvMapSymbol]) {
	// biome-ignore lint/suspicious/noExplicitAny: globalThis
	(globalThis as any)[nvMapSymbol] = new Map<string, niivue.Niivue>();
}

// biome-ignore lint/suspicious/noExplicitAny: globalThis
const nvMap = (globalThis as any)[nvMapSymbol] as Map<string, niivue.Niivue>;

export { nvMap };
