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

  model.on("change:opacity", () => {
    let value = model.get("opacity");
    nv.setOpacity(0, value);
  });

  model.on("change:colormap", () => {
    let value = model.get("colormap");
    nv.setColorMap(nv.volumes[0].id, value);
  });

  model.on("change:slice_type", () => {
    let value = model.get("slice_type");
    nv.setSliceType(value);
  });

  model.on("change:drag_mode", () => {
    let value = model.get("drag_mode");
    if (value == "DRAG_MODES.CONTRAST") {
      nv.opts.dragMode = nv.dragModes.contrast;
    }
    if (value == "DRAG_MODES.MEASUREMENT") {
      nv.opts.dragMode = nv.dragModes.measurement;
    }
    if (value == "DRAG_MODES.PAN") {
      nv.opts.dragMode = nv.dragModes.pan;
    }
  });
  
}

export default { render };
