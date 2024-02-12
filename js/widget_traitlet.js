import "./widget.css";

import { Niivue, NVImage } from "@niivue/niivue";

async function render({ model, el }) {
  const options = { dragAndDropEnabled: false };
  let canvas = document.createElement("canvas");
  let container = document.createElement("div");
  container.style.height = "300px";
  container.appendChild(canvas);
  el.appendChild(container);
  let nv = new Niivue(options);
  nv.attachToCanvas(canvas);

  let file = model.get("file");
  let image = new NVImage(file.data.buffer, file.name);
  nv.addVolume(image);
}

export default { render };


