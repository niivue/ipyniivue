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
