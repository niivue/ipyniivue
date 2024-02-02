import "./widget.css";

import { Niivue } from "@niivue/niivue";

export async function render({ model, el }) {
  let canvas = document.createElement("canvas");
  let container = document.createElement("div");
  container.style.height = "300px";
  container.appendChild(canvas);
  el.appendChild(container);
  let nv = new Niivue();
  nv.attachToCanvas(canvas);
  // nv.loadVolumes([
  //   { url: "https://niivue.github.io/niivue/images/mni152.nii.gz" },
  // ]);
  model.on("msg:custom", (msg) => {
    if (msg.type === "setting_property") {
      if (msg.func === "setColorMap") {
        let mapping = {
          "nv.volumes[0].id": nv.volumes[0].id,
        };
        let funcname = msg.func;
        let [arg1, arg2] = msg.args;
        let arg1mapped = mapping[arg1];

        nv[funcname](arg1mapped, arg2);
        // smame as nv[funcname](nv.volumes[0].id, "green");
        console.log("Setting property message received!");
        return;
      }
      // setOpacity, setCrosshairColor , ...
      nv[msg.func](...msg.args);
    }
    if (msg.type === "api") {
      // API call for load volume, load mesh etc.
      console.log("API message received!");
      let funcname = msg.func;
      nv[funcname](...msg.args);
    }
  });
}
