declare module '@niivue/niivue' {
  export class NVImage {
    constructor(args: object);
    static loadFromBase64(data: object): any;
  }

  export class NVMesh {
    constructor(args: object);
  }

  export class Niivue {
    constructor(options: object);
  }
}