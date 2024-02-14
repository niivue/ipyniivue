import "./widget.css";

import { Niivue } from "@niivue/niivue";

async function render({ model, el }) {
  let canvas = document.createElement("canvas");
  let container = document.createElement("div");
  container.style.height = "300px";
  container.appendChild(canvas);
  el.appendChild(container);
  let nv = new Niivue();
  let value = model.get("volume");
  nv.attachToCanvas(canvas);
  if (value != "") {
    nv.loadVolumes(value);
  }

  model.on("change:volume", async () => {
    value = model.get("volume");
    console.log("volume changed");
    console.log(value);
    await nv.loadVolumes(value);
  });
}

export default { render };
