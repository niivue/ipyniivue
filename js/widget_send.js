import "./widget.css";

import { Niivue } from "@niivue/niivue";

async function render({ model, el }) {
  let canvas = document.createElement("canvas");
  let container = document.createElement("div");
  container.style.height = "300px";
  container.appendChild(canvas);
  el.appendChild(container);
  let nv = new Niivue();
  nv.attachToCanvas(canvas);

  model.on("msg:custom", (msg) => {
    if (msg.type === "api") {
      console.log("API message received!");
      let funcname = msg.func;
      nv[funcname](...msg.args);
    }
  });
}

export default { render };
