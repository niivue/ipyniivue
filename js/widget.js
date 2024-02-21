// @ts-check
import { Niivue, NVImage } from "@niivue/niivue";

/**
 * Generates a unique file name for a volume (using the model id and the volume path)
 *
 * We need to keep track of the volumes from Python somehow, and the model_id is unique
 * to the volume sent from Python. This function generates a new filename for the volume
 * using the existing filename and model
 *
 * @param {import('./types').VolumeModel} model
 * @returns {string}
 */
function volume_id(model) {
  let path = model.get("path");
  // take the first 6 characters of the model_id, it should be unique enough
  let id = model.model_id.slice(0, 6);
  return id + ":" + path.name;
}

/**
 * Determine what type of update is necessary to go from `old_arr` to `new_arr`.
 *
 * If cannot determine the update type, return "unknown". Only "add" is supported
 * for now.
 *
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

/**
 * @param {import('./types').Model} model
 * @param {string[]} ids
 * @returns {Promise<Array<import('./types').VolumeModel>>}
 */
function gather_models(model, ids) {
  /** @type {Array<Promise<any>>} */
  let models = [];
  let widget_manager = model.widget_manager;
  for (let id of ids) {
    let model_id = id.slice("IPY_MODEL_".length);
    models.push(widget_manager.get_model(model_id));
  }
  return Promise.all(models);
}

/**
 * @param {import('./types').Model} model
 */
function gather_volume_models(model) {
  let ids = model.get("_volumes");
  return gather_models(model, ids);
}

/**
 * Create a new NVImage and attach the necessary event listeners
 * Returns the NVImage and a cleanup function that removes the event listeners.
 *
 * @param {Niivue} nv
 * @param {import('./types').VolumeModel} vmodel
 * @returns {[NVImage, () => void]}
 */
function create_volume(nv, vmodel) {
  let volume = new NVImage(
    vmodel.get("path").data.buffer, // dataBuffer
    volume_id(vmodel),              // name
    vmodel.get("colormap"),         // colormap
    vmodel.get("opacity"),          // opacity
    undefined,                      // pairedImgData
    vmodel.get("cal_min"),          // cal_min
    vmodel.get("cal_max"),          // cal_max
    undefined,                      // trustMinCalMinMax
    undefined,                      // percentileFrac
    undefined,                      // ignoreZeroVoxels
    vmodel.get("visible"),          // visible
    undefined,                      // useQFormNotSForm
    undefined,                      // colormapNegative
    undefined,                      // frame4D
    undefined,                      // imageType
    undefined,                      // cal_minNeg
    undefined,                      // cal_maxNeg
    vmodel.get("colorbar_visible"), // colorbarVisible
    undefined,                      // colormapLabel
  );
  function colorbar_visible_changed() {
    volume.colorbarVisible = vmodel.get("colorbar_visible");
    nv.updateGLVolume();
  }
  function cal_min_changed() {
    volume.cal_min = vmodel.get("cal_min");
    nv.updateGLVolume();
  }
  function cal_max_changed() {
    volume.cal_min = vmodel.get("cal_min");
    nv.updateGLVolume();
  }
  // NOTE: I don't think this does anything
  function visible_changed() {
    volume.visible = vmodel.get("visible");
    nv.updateGLVolume();
  }
  function colormap_changed() {
    volume.colormap = vmodel.get("colormap");
    nv.updateGLVolume();
  }
  function opacity_changed() {
    volume.opacity = vmodel.get("opacity");
    nv.updateGLVolume();
  }
  vmodel.on("change:colorbar_visible", colorbar_visible_changed);
  vmodel.on("change:cal_min", cal_min_changed);
  vmodel.on("change:cal_max", cal_max_changed);
  vmodel.on("change:visible", visible_changed);
  vmodel.on("change:colormap", colormap_changed);
  vmodel.on("change:opacity", opacity_changed);
  return [volume, () => {
    vmodel.off("change:colorbar_visible", colorbar_visible_changed);
    vmodel.off("change:cal_min", cal_min_changed);
    vmodel.off("change:cal_max", cal_max_changed);
    vmodel.off("change:visible", visible_changed);
    vmodel.off("change:colormap", colormap_changed);
    vmodel.off("change:opacity", opacity_changed);
  }]
}


/**
  * @param {Niivue} nv
  * @param {import("./types").Model} model
  * @param {Map<string, () => void>} cleanups
  */
async function render_volumes(nv, model, cleanups) {
  let vmodels = await gather_volume_models(model);
  let curr_names = nv.volumes.map(v => v.name);
  let new_names = vmodels.map(volume_id);
  let update_type = determine_update_type(curr_names, new_names);
  if (update_type === "add") {
    // We know that the new volumes are the same as the old volumes,
    // except for the last one. We can just add the last volume.
    let vmodel = vmodels[vmodels.length - 1];
    let [volume, cleanup] = create_volume(nv, vmodel);
    cleanups.set(volume.id, cleanup);
    nv.addVolume(volume);
    return;
  }
  // HERE can be the place to add more update types
  // ...

  // We don't know what the update type is, so we need to remove all volumes
  // and add the new ones.

  // clear all volumes
  for (let [_, cleanup] of cleanups) cleanup();
  cleanups.clear();

  // create each volume and add one-by-one
  for (let vmodel of vmodels) {
    let [volume, cleanup] = create_volume(nv, vmodel);
    cleanups.set(volume.id, cleanup);
    nv.addVolume(volume);
  }
}

export default {
  /** @param {{ model: import("./types").Model, el: HTMLElement }} ctx */
  render({ model, el }) {

    let canvas = document.createElement("canvas");
    let container = document.createElement("div");
    container.style.height = "300px";
    container.appendChild(canvas);
    el.appendChild(container);

    let nv = new Niivue(model.get("_opts") ?? {});
    nv.attachToCanvas(canvas);

    /** @type {Map<string, () => void>} */
    let vcleanups = new Map();
    render_volumes(nv, model, vcleanups);
    // Any time we change the volumes, we need to update the nv object
    model.on("change:_volumes", () => render_volumes(nv, model, vcleanups));

    // Any time we change the options, we need to update the nv object
    // and redraw the scene.
    model.on("change:_opts", () => {
      nv.opts = { ...nv.opts, ...model.get("_opts") };
      nv.drawScene();
      nv.updateGLVolume();
    });

    // All the logic for cleaning up the event listeners and the nv object
    return () => {
      for (let [_, cleanup] of vcleanups) cleanup();
      vcleanups.clear();
      model.off("change:_volumes");
      model.off("change:_opts");
    }
  }
}
