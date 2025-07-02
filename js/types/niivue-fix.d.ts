import { Niivue } from "@niivue/niivue";

declare module "@niivue/niivue" {
	interface Niivue {
		setMeshShader(meshId: string, shader: string): void;
	}
}
