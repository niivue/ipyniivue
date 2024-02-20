import "./widget.css";

import { Niivue, NVImage, SLICE_TYPE } from "@niivue/niivue";

async function render({ model, el }) {
  const options = { dragAndDropEnabled: false };
  let canvas = document.createElement("canvas");
  let container = document.createElement("div");
  container.style.height = "300px";
  container.appendChild(canvas);
  el.appendChild(container);
  let nv = new Niivue(options);
  nv.attachToCanvas(canvas);

  console.log("volume");
  console.log(nv.volumes); // this will be []

  function render_volumes() {
    let new_volumes = model.get("_volumes");
    console.log(new_volumes);
    new_volumes.forEach(async (volume_file) => {
      let image = new NVImage(volume_file.data.buffer, volume_file.name);
      await nv.addVolume(image);
    });
  }

  render_volumes(); // initial render
  model.on("change:_volumes", render_volumes); //later render

  // let image = new NVImage(volume_file.data.buffer, volume_file.name);
  // await nv.addVolume(image);

  // let volume_file = model.get("volume_file");
  // let image = new NVImage(volume_file.data.buffer, volume_file.name);
  // await nv.addVolume(image);

  // model.on("change:volume_file", async() => {
  //   let volume_file = model.get("volume_file");
  //   let image = new NVImage(volume_file.data.buffer, volume_file.name);
  //   await nv.addVolume(image);
  // });

  // model.on("change:opacity", () => {
  //   let value = model.get("opacity");
  //   nv.setOpacity(0, value);
  // });

  // model.on("change:colormap", () => {
  //   let value = model.get("colormap");
  //   nv.setColorMap(nv.volumes[0].id, value);
  // });

  // model.on("change:slice_type", () => {
  //   let value = model.get("slice_type");
  //   nv.setSliceType(value);
  // });

  // model.on("change:drag_mode", () => {
  //   let value = model.get("drag_mode");
  //   if (value == "DRAG_MODES.CONTRAST") {
  //     nv.opts.dragMode = nv.dragModes.contrast;
  //   }
  //   if (value == "DRAG_MODES.MEASUREMENT") {
  //     nv.opts.dragMode = nv.dragModes.measurement;
  //   }
  //   if (value == "DRAG_MODES.PAN") {
  //     nv.opts.dragMode = nv.dragModes.pan;
  //   }
  // });
}

export default { render };
