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

  model.on("change:binary_value", () => {
    let dataView = model.get("binary_value"); // JavaScript DataView
    console.log("Here is the data");
    console.log(dataView);
    let image = new NVImage(dataView.buffer, "my_image.nii.gz");
    nv.addVolume(image);
  });
}

export default { render };
