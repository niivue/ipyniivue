declare module '@niivue/niivue' {
    export class NVImage {
      static loadFromBase64(data: object): Promise<NVImage>;
    }
  
    export class Niivue {
      constructor(options: object);
    }
  }