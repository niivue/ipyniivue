import { Niivue, NVImage } from "@niivue/niivue";

/**
 * @param {{ id: string; get(key: "path"): { name: string }}} model
 * @param {string} name
 * @returns {string}
 */
function volume_id(model) {
  let path = model.get("path");
  return model.model_id + ":" + path.name;
}

/**
  * @template T
  * @param {Array<T>} old_arr
  * @param {Array<T>} new_arr
  * @returns {"add" | "unknown"}
  */
function determine_update_type(old_arr, new_arr) {
  if (
    old_arr.length === (new_arr.length - 1) &&
    old_arr.every((v, i) => new_arr[i] === v)
  ) {
    return "add";
  }
  return "unknown";
}

function gather_models(model, ids) {
  /** @type {Array<Promise<unknown>>} */
  let models = [];
  let widget_manager = model.widget_manager;
  for (let id of ids) {
    let model_id = id.slice("IPY_MODEL_".length);
    models.push(widget_manager.get_model(model_id));
  }
  return Promise.all(models);
}

/**
 * @param {Niivue} nv
 */
function create_volume(nv, vmodel) {
  let volume = new NVImage(
    vmodel.get("path").data.buffer,
    volume_id(vmodel),
    vmodel.get("colormap"),
    vmodel.get("opacity"),
  );
  function colormap_changed() {
    nv.setColormap(volume.id, vmodel.get("colormap"));
  }
  function opacity_changed() {
    let idx = nv.volumes.findIndex(v => v === volume);
    nv.setOpacity(idx, vmodel.get("opacity"));
  }
  vmodel.on("change:colormap", colormap_changed);
  vmodel.on("change:opacity", opacity_changed);
  return [volume, () => {
    vmodel.off("change:colormap", colormap_changed);
    vmodel.off("change:opacity", opacity_changed);
  }]
}


/**
  * @param {Niivue} nv
  * @param {any} model
  * @param {Map<string, () => void>} cleanups
  */
async function render_volumes(nv, model, cleanups) {
  let vmodels = await gather_models(model, model.get("_volumes"));
  let curr_names = nv.volumes.map(v => v.name);
  let new_names = vmodels.map(volume_id);
  let update_type = determine_update_type(curr_names, new_names);
  if (update_type === "add") {
    let vmodel = vmodels[vmodels.length - 1];
    let [volume, cleanup] = create_volume(nv, vmodel);
    cleanups.set(volume.id, cleanup);
    nv.addVolume(volume);
    return;
  }
  // cleanup all existing volumes
  for (let [_, cleanup] of cleanups) cleanup();
  cleanups.clear();
  for (let vmodel of vmodels) {
    let [volume, cleanup] = create_volume(nv, vmodel);
    cleanups.set(volume.id, cleanup);
    nv.addVolume(volume);
  }
}

export default {
  render({ model, el }) {
    /** @type {Map<string, () => void>} */
    let cleanups = new Map();
    let canvas = document.createElement("canvas");
    let container = document.createElement("div");
    container.style.height = "300px";
    container.appendChild(canvas);
    el.appendChild(container);

    let nv = new Niivue(model.get("_opts") ?? {});
    nv.attachToCanvas(canvas);

    render_volumes(nv, model, cleanups);
    model.on("change:_volumes", () => render_volumes(nv, model, cleanups));
    model.on("change:_opts", () => {
      nv.opts = { ...nv.opts, ...model.get("_opts") };
      nv.drawScene();
      nv.updateGLVolume();
    });
    return () => {
      for (let [_, cleanup] of cleanups) cleanup();
      cleanups.clear();
      model.off("change:_volumes");
      model.off("change:_opts");
    }
  }
}
