//https://stackoverflow.com/a/9458996
export function arrayBufferToBase64(buffer: ArrayBuffer) {
  let binary = '';
  const bytes = new Uint8Array(buffer);
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

//https://developer.chrome.com/blog/how-to-convert-arraybuffer-to-and-from-string/
export function arrayBufferToString(buffer: ArrayBuffer) {
  const bytes = new Uint8Array(buffer);
  return String.fromCharCode.apply(null, [...bytes]);
}

export function stringToArrayBuffer(str: string) {
  const buf = new ArrayBuffer(str.length);
  const bufView = new Uint8Array(buf);
  for (let i = 0, strLen = str.length; i < strLen; i++) {
    bufView[i] = str.charCodeAt(i);
  }
  return buf;
}

//NVImage filtering
type FilteredNVImage = {
  dataBuffer: ArrayBuffer;
  name: string;
  colormap: string;
  opacity: number;
  pairedImgData: ArrayBuffer;
  cal_min: number;
  cal_max: number;
  trustCalMinMax: boolean;
  percentileFrac: number;
  ignoreZeroVoxels: boolean;
  visible: boolean;
  useQFormNotSForm: boolean;
  colormapNegative: string;
  frame4D: number;
  imageType: any; //todo. Just an int or create type declaration?
  cal_minNeg: number;
  cal_maxNeg: number;
  colorbarVisible: boolean;
  colormapLabel: any; //idk if array or just general object
  id: string;
};

export function filterNVImage(obj: any): FilteredNVImage {
  return {
    dataBuffer: obj.dataBuffer,
    name: obj.name,
    colormap: obj.colormap,
    opacity: obj.opacity,
    pairedImgData: obj.pairedImgData,
    cal_min: obj.cal_min,
    cal_max: obj.cal_max,
    trustCalMinMax: obj.trustCalMinMax,
    percentileFrac: obj.percentileFrac,
    ignoreZeroVoxels: obj.ignoreZeroVoxels,
    visible: obj.visible,
    useQFormNotSForm: obj.useQFormNotSForm,
    colormapNegative: obj.colormapNegative,
    frame4D: obj.frame4D,
    imageType: obj.imageType,
    cal_minNeg: obj.cal_minNeg,
    cal_maxNeg: obj.cal_maxNeg,
    colorbarVisible: obj.colorbarVisible,
    colormapLabel: obj.colormapLabel,
    id: obj.id,
  };
}

//NVMesh filtering
type FilteredNVMesh = {
  pts: number[];
  tris: number[];
  name: string;
  rgba255: number[];
  opacity: number;
  visible: boolean;
  connectome: any; //todo.
  dpg: any[] | null,
  dps: any[] | null,
  dpv: any[] | null,
  colorbarVisible: boolean;
  id: string;
};

export function filterNVMesh(obj: any): FilteredNVMesh {
  return {
    pts: obj.pts,
    tris: obj.tris,
    name: obj.name,
    rgba255: obj.rgba255,
    opacity: obj.opacity,
    visible: obj.visible,
    connectome: obj.connectome,
    dpg: obj.dpg,
    dps: obj.dps,
    dpv: obj.dpv,
    colorbarVisible: obj.colorbarVisible,
    id: obj.id,
  };
}