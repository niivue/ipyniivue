import "./widget.css";

import { Niivue, SLICE_TYPE } from "@niivue/niivue";

export async function render({ model, el }) {
  // let options = model.get("options");

  const options = {dragAndDropEnabled: false} 
  let canvas = document.createElement("canvas");
  let container = document.createElement("div");
  container.style.height = "300px";
  container.appendChild(canvas);
  el.appendChild(container);
  let nv = new Niivue(options);
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
    nv.setSliceType(SLICE_TYPE.MULTIPLANAR)
  });
}
