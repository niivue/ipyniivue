//https://github.com/martinRenou/ipycanvas/blob/master/src/utils.ts

export function getTypedArray(dataview: any, metadata: any) {
    switch (metadata.dtype) {
      case 'int8':
        return new Int8Array(dataview.buffer);
        break;
      case 'uint8':
        return new Uint8Array(dataview.buffer);
        break;
      case 'int16':
        return new Int16Array(dataview.buffer);
        break;
      case 'uint16':
        return new Uint16Array(dataview.buffer);
        break;
      case 'int32':
        return new Int32Array(dataview.buffer);
        break;
      case 'uint32':
        return new Uint32Array(dataview.buffer);
        break;
      case 'float32':
        return new Float32Array(dataview.buffer);
        break;
      case 'float64':
        return new Float64Array(dataview.buffer);
        break;
      default:
        throw 'Unknown dtype ' + metadata.dtype;
        break;
    }
  }