# Niivue - Original Gallery

# [Basic multiplanar](https://niivue.github.io/niivue/features/basic.multiplanar.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/e6594c33-9b4e-4eda-9d82-47dbd244a50b.png)


</td>
<td>

	
```javascript
import * as niivue from "../dist/index.js";

var drop = document.getElementById("sliceType");
drop.onchange = function () {
  let st = parseInt(document.getElementById("sliceType").value);
  nv1.setSliceType(st);
};
function handleIntensityChange(data) {
  document.getElementById("intensity").innerHTML = "&nbsp;&nbsp;" + data.string;
  console.log(data);
}
var volumeList1 = [
  {
    url: "../images/mni152.nii.gz",
    colormap: "gray",
    visible: true,
    opacity: 1,
  },
  {
    url: "../images/hippo.nii.gz",
    colormap: "red",
    visible: true,
    opacity: 1,
  },
];
var nv1 = new niivue.Niivue({
  dragAndDropEnabled: true,
  onLocationChange: handleIntensityChange,
});
// nv1.setRadiologicalConvention(false);
// nv1.opts.multiplanarForceRender = true;
nv1.attachTo("gl1");
await nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeMultiplanar);

```
</td>
</tr>
</table>



# [Sync mesh](https://niivue.github.io/niivue/features/sync.mesh.html)


<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/faf5065b-1cb7-4f06-b1fd-e7e6f7bfdc00.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
document
  .getElementById("sliceType")
  .addEventListener("change", changeSliceType);
function changeSliceType() {
  let st = parseInt(document.getElementById("sliceType").value);
  nv1.setSliceType(st);
  nv2.setSliceType(st);
}
document.getElementById("check10").addEventListener("change", doCheck10Click);
function doCheck10Click() {
  nv1.setHighResolutionCapable(this.checked);
}
var dxslider = document.getElementById("dxSlider");
dxslider.oninput = function () {
  let dx = parseFloat(this.value);
  if (dx > 10) dx = Infinity;
  nv1.setMeshThicknessOn2D(dx);
};
function handleIntensityChange(data) {
  document.getElementById("intensity").innerHTML = "&nbsp;&nbsp;" + data.string;
}
function handleIntensityChange2(data) {
  document.getElementById("intensity2").innerHTML =
    "&nbsp;&nbsp;" + data.string;
}
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  onLocationChange: handleIntensityChange,
  backColor: [1, 1, 1, 1],
});
nv1.attachTo("gl1");
nv1.setHighResolutionCapable(false);
nv1.opts.isOrientCube = true;
var volumeList1 = [{ url: "../images/mni152.nii.gz" }];
await nv1.loadVolumes(volumeList1);
await nv1.loadMeshes([{ url: "../images/BrainMesh_ICBM152.lh.mz3" }]);
nv1.setMeshShader(0, "Outline");
nv1.opts.multiplanarForceRender = true;
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.setSliceMM(true);
nv1.setClipPlane([0, 180, 40]);
//
var nv2 = new niivue.Niivue({
  show3Dcrosshair: true,
  onLocationChange: handleIntensityChange2,
  backColor: [1, 1, 1, 1],
});
nv2.attachTo("gl2");
nv2.setHighResolutionCapable(true);
await nv2.loadVolumes(volumeList1);
await nv2.loadMeshes([{ url: "../images/BrainMesh_ICBM152.lh.mz3" }]);
nv2.opts.multiplanarForceRender = true;
nv2.setSliceType(nv2.sliceTypeMultiplanar);
nv2.setSliceMM(true);
nv2.setClipPlane([0, 180, 40]);
nv1.syncWith(nv2, { "3d": true, "2d": true });

	
```
</td>
</tr>
</table>




# [Bidirectional Sync](https://niivue.github.io/niivue/features/sync.bidirectional.html)


<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/50572e13-4f07-4bd3-993a-2eceee1df071.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
layout.onchange = function () {
  nv1.setMultiplanarLayout(this.value);
  nv2.setMultiplanarLayout(this.value);
  nv3.setMultiplanarLayout(this.value);
};
canvasHeight.onchange = function () {
  gl1.height = this.value;
  gl2.height = this.value;
  gl3.height = this.value;
  nv1.resizeListener();
  nv2.resizeListener();
  nv3.resizeListener();
};
function handleIntensityChange(data) {
  document.getElementById("intensity").innerHTML = "&nbsp;&nbsp;" + data.string;
}
function handleIntensityChange2(data) {
  document.getElementById("intensity2").innerHTML =
    "&nbsp;&nbsp;" + data.string;
}
function handleIntensityChange3(data) {
  document.getElementById("intensity3").innerHTML =
    "&nbsp;&nbsp;" + data.string;
}
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  onLocationChange: handleIntensityChange,
  backColor: [1, 1, 1, 1],
});
nv1.attachTo("gl1");
var volumeList1 = [{ url: "../images/pcasl.nii.gz" }];
await nv1.loadVolumes(volumeList1);
var nv2 = new niivue.Niivue({
  show3Dcrosshair: true,
  onLocationChange: handleIntensityChange2,
  backColor: [1, 1, 1, 1],
});
nv2.attachTo("gl2");
var nv3 = new niivue.Niivue({
  show3Dcrosshair: true,
  onLocationChange: handleIntensityChange3,
  backColor: [1, 1, 1, 1],
});
nv3.attachTo("gl3");
var volumeList2 = [{ url: "../images/mni152.nii.gz" }];
var volumeList3 = [{ url: "../images/mni152.nii.gz" }];
await nv2.loadVolumes(volumeList2);
await nv3.loadVolumes(volumeList3);
// make sure all views can control each other
nv1.broadcastTo([nv2, nv3], { "3d": true, "2d": true });
nv2.broadcastTo([nv1, nv3], { "3d": true, "2d": true });
nv3.broadcastTo([nv1, nv2], { "3d": true, "2d": true });

	
```
</td>
</tr>
</table>

# [Color maps for voxels](https://niivue.github.io/niivue/features/colormaps.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/4b352732-9dc5-4616-ae0f-66a07ef8aa41.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var slider = document.getElementById("gammaSlider");
slider.oninput = function () {
  nv1.setGamma(this.value * 0.01);
};
invertCheck.onchange = function () {
  nv1.volumes[0].colormapInvert = this.checked;
  nv1.updateGLVolume();
};
selectCheck.onchange = function () {
  if (this.checked) nv1.setSelectionBoxColor([0, 1, 0, 0.7]);
  else nv1.setSelectionBoxColor([1, 1, 1, 0.5]);
};
crossCheck.onchange = function () {
  if (this.checked) nv1.setCrosshairColor([0, 1, 0, 1]);
  else nv1.setCrosshairColor([1, 0, 0, 1]);
};
wideCheck.onchange = function () {
  if (this.checked) nv1.setCrosshairWidth(3);
  else nv1.setCrosshairWidth(1);
};
function doCustom() {
  var val = document.getElementById("scriptText").value;
  val +=
    ';let key = "Custom";\n' +
    "nv1.addColormap(key, cmap);\n" +
    "nv1.volumes[0].colormap = key;\n" +
    "nv1.updateGLVolume();";
  val && eval(val);
}
‚
document.getElementById("saveBmp").addEventListener("click", doSaveBmp);
function doSaveBmp() {
  nv1.saveScene("ScreenShot.png");
}
var volumeList1 = [
  {
    url: "../images/mni152.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
];
var nv1 = new niivue.Niivue({ backColor: [0.3, 0.3, 0.3, 1] });
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
nv1.opts.multiplanarForceRender = true;
nv1.opts.isColorbar = true;
let cmaps = nv1.colormaps();
let cmapEl = document.getElementById("colormaps");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setColormap(nv1.volumes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}


	
```
</td>
</tr>
</table>

# [Color maps for meshes](https://niivue.github.io/niivue/features/colormaps.mesh.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/12e1ba84-fd9b-458d-b583-8c328bc6eaaf.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
invertCheck.onchange = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "colormapInvert", this.checked);
  nv1.updateGLVolume();
};
curveSlider.onchange = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value * 0.1);
};
opacitySlider.onchange = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "opacity", this.value * 0.1);
};
document.getElementById("saveBmp").addEventListener("click", doSaveBmp);
function doSaveBmp() {
  nv1.saveScene("ScreenShot.png");
}
var meshLHLayersList1 = [
  {
    url: "../images/BrainMesh_ICBM152.lh.curv",
    colormap: "gray",
    cal_min: 0.3,
    cal_max: 0.5,
    opacity: 0.7,
  },
  {
    url: "../images/BrainMesh_ICBM152.lh.motor.mz3",
    cal_min: 1.64,
    cal_max: 5,
    colormap: "warm",
    colormapNegative: "winter",
    useNegativeCmap: true,
    opacity: 0.7,
  },
];
var nv1 = new niivue.Niivue({ backColor: [0.3, 0.3, 0.3, 1] });
let cmaps = nv1.colormaps();
let cmapEl = document.getElementById("colormaps");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "colormap", cmaps[i]);
    nv1.updateGLVolume();
  };
  cmapEl.appendChild(btn);
}
nv1.attachTo("gl1");
nv1.opts.isColorbar = true;
await nv1.loadMeshes([
  { url: "../images/BrainMesh_ICBM152.lh.mz3", layers: meshLHLayersList1 },
]);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "colorbarVisible", false);

	
```
</td>
</tr>
</table>

# [Background masks overlays](https://niivue.github.io/niivue/features/mask.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/81455b3b-a076-4e7e-8ec9-1bfedd28609c.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
var volumeList1 = [
  {
    url: "../images/fslmean.nii.gz", //"./RAS.nii.gz", "./spm152.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
  {
    url: "../images/fslt.nii.gz", //"./RAS.nii.gz", "./spm152.nii.gz",
    colormap: "redyell",
    cal_min: 0.05,
    cal_max: 5.05,
    opacity: 0.9,
    visible: true,
  },
];
var nv1 = new niivue.Niivue({ show3Dcrosshair: true });
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeRender);
nv1.setClipPlane([0.15, 270, 0]);
nv1.setRenderAzimuthElevation(45, 45);
document.getElementById("check1").addEventListener("change", checkClick);
function checkClick() {
  nv1.backgroundMasksOverlays = this.checked;
  nv1.updateGLVolume();
}

	
```
</td>
</tr>
</table>

# [Alpha and asymmetric statistical thresholds](https://niivue.github.io/niivue/features/alphathreshold.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/7b37d48d-5052-4ccf-a24f-946a10f1c450.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
document.getElementById("check1").addEventListener("change", doCheckClick);
function doCheckClick() {
  if (this.checked) nv1.setColormapNegative(nv1.volumes[1].id, "winter");
  else nv1.setColormapNegative(nv1.volumes[1].id, "");
  nv1.drawScene();
}
document.getElementById("check2").addEventListener("change", doCheck2Click);
function doCheck2Click() {
  nv1.volumes[1].alphaThreshold = this.checked;
  nv1.updateGLVolume();
}
document.getElementById("check3").addEventListener("change", doCheck3Click);
function doCheck3Click() {
  nv1.setInterpolation(!document.getElementById("check3").checked);
}
document.getElementById("check5").addEventListener("change", doCheck5Click);
function doCheck5Click() {
  nv1.setSliceMM(this.checked);
}
var slider = document.getElementById("slide");
slider.oninput = function () {
  nv1.volumes[1].cal_min = 0.1 * this.value;
  nv1.updateGLVolume();
};
var slider2 = document.getElementById("slide2");
slider2.oninput = function () {
  nv1.overlayOutlineWidth = 0.25 * this.value;
  nv1.updateGLVolume();
};
var slider3 = document.getElementById("slide3");
slider3.oninput = function () {
  nv1.volumes[1].cal_minNeg = -6;
  nv1.volumes[1].cal_maxNeg = -0.1 * this.value;
  nv1.updateGLVolume();
};
var dropDrag = document.getElementById("dragMode");
dropDrag.onchange = function () {
  switch (document.getElementById("dragMode").value) {
    case "none":
      nv1.opts.dragMode = nv1.dragModes.none;
      break;
    case "contrast":
      nv1.opts.dragMode = nv1.dragModes.contrast;
      break;
    case "measurement":
      nv1.opts.dragMode = nv1.dragModes.measurement;
      break;
    case "pan":
      nv1.opts.dragMode = nv1.dragModes.pan;
      break;
  }
};
document.getElementById("about").addEventListener("click", doAbout);
function doAbout() {
  window.alert(
    "NiiVue allows asymmetric positive and negative statistical thresholds. \
	It can also make subthreshold values translucent \
	(only apply to unsmoothed images)"
  );
}
var volumeList1 = [
  { url: "../images/fslmean.nii.gz" },
  {
    url: "../images/fslt.nii.gz",
    colormap: "warm",
    colormapNegative: "winter",
    cal_min: 3,
    cal_max: 6,
  },
];
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
var nv1 = new niivue.Niivue({
  loadingText: "there are no images",
  backColor: [1, 1, 1, 1],
  show3Dcrosshair: true,
  onLocationChange: handleLocationChange,
});
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.setSliceMM(false);
nv1.opts.isColorbar = true;
await nv1.loadVolumes(volumeList1);
nv1.volumes[0].colorbarVisible = false; //hide colorbar for anatomical scan
nv1.volumes[1].alphaThreshold = true;
nv1.volumes[1].cal_minNeg = -6;
nv1.volumes[1].cal_maxNeg = -3.0;
nv1.opts.multiplanarForceRender = true;
nv1.setInterpolation(true);
nv1.updateGLVolume();

	
```
</td>
</tr>
</table>

# [Test images](https://niivue.github.io/niivue/features/test_images.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/ef511f63-8572-455c-954b-047d55eae2f7.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var volumeList1 = [
  // first item is background image
  {
    url: "../images/mni152.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
];
var nv1 = new niivue.Niivue({ backColor: [0.7, 0.7, 0.9, 1] });
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
nv1.opts.isColorbar = true;
nv1.setSliceType(nv1.sliceTypeRender);
nv1.setClipPlane([0.35, 270, 0]);
//nv1.setSliceType(nv1.sliceTypeMultiplanar)
let imgs = [
  "chris_MRA",
  "chris_PD",
  "chris_t1",
  "chris_t2",
  "CT_Abdo",
  "CT_AVM",
  "CT_Electrodes",
  "CT_Philips",
  "CT_pitch",
  "fmri_pitch",
  "Iguana",
  "mni152",
  "MR_Gd",
  "pcasl",
  "spm152",
  "spmMotor",
  "visiblehuman",
];
let imgEl = document.getElementById("images");
for (let i = 0; i < imgs.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = imgs[i];
  btn.onclick = function () {
    let root = "https://niivue.github.io/niivue-demo-images/";
    let img = root + imgs[i] + ".nii.gz";
    console.log("Loading: " + img);
    volumeList1[0].url = img;
    nv1.loadVolumes(volumeList1);
    nv1.updateGLVolume();
  };
  imgEl.appendChild(btn);
}
let cmaps = nv1.colormaps();
let cmapEl = document.getElementById("colormaps");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setColormap(nv1.volumes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>

# [Drag and drop](https://niivue.github.io/niivue/features/draganddrop.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/44893804-6898-4835-88f4-2f27fe56233d.png)


</td>
<td>

	
```javascript


import * as niivue from "../dist/index.js";
var nv1 = new niivue.Niivue();
nv1.attachTo("gl1");
nv1.setSliceType(nv1.sliceTypeRender);

	
```
</td>
</tr>
</table>

# [Select font](https://niivue.github.io/niivue/features/selectfont.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/79bdcf30-23fb-4cec-8175-998901d90c58.png)


</td>
<td>

	
```javascript

var dropFont = document.getElementById("fonts");
dropFont.onchange = function () {
  const fontName = document.getElementById("fonts").value;
  switch (fontName) {
    case "roboto":
      nv1.loadFont(
        "../fonts/Roboto-Regular.png",
        "../fonts/Roboto-Regular.json"
      );
      break;
    case "garamond":
      nv1.loadFont("../fonts/Garamond.png", "../fonts/Garamond.json");
      break;
    case "ubuntu":
      nv1.loadFont("../fonts/Ubuntu.png", "../fonts/Ubuntu.json");
      break;
    case "ubuntubold":
      nv1.loadFont("../fonts/UbuntuBold.png", "../fonts/UbuntuBold.json");
      break;
  }
};
import * as niivue from "../dist/index.js";
var nv1 = new niivue.Niivue();
nv1.attachTo("gl1");
nv1.setSliceType(nv1.sliceTypeMultiplanar);

	
```
</td>
</tr>
</table>

# [Connectome](https://niivue.github.io/niivue/features/connectome.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/e3fd7e69-5153-4552-9b4b-e5f5122904b6.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
invertCheck.onchange = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "colormapInvert", this.checked);
  nv1.updateGLVolume();
};
var sliderE = document.getElementById("edgeSlider");
var sliderN = document.getElementById("nodeSlider");
var sliderT = document.getElementById("threshSlider");
// Update the current slider value (each time you drag the slider handle)
sliderE.oninput = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "edgeScale", this.value * 0.1);
};
sliderN.oninput = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "nodeScale", this.value * 0.1);
};
sliderT.oninput = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "edgeMin", this.value * 0.1);
};
let connectome = {
  name: "simpleConnectome",
  nodeColormap: "warm",
  nodeColormapNegative: "winter",
  nodeMinColor: 2,
  nodeMaxColor: 4,
  nodeScale: 3, //scale factor for node, e.g. if 2 and a node has size 3, \
	/// a 6mm ball is drawn
  edgeColormap: "warm",
  edgeColormapNegative: "winter",
  edgeMin: 2,
  edgeMax: 6,
  edgeScale: 1,
  nodes: [
    {
      name: "RF",
      x: 40,
      y: 40,
      z: 30,
      colorValue: 2,
      sizeValue: 2,
    },
    {
      name: "LF",
      x: -40,
      y: 40,
      z: 20,
      colorValue: 2,
      sizeValue: 2,
    },
    {
      name: "RP",
      x: 40,
      y: -40,
      z: 50,
      colorValue: 3,
      sizeValue: 3,
    },
    {
      name: "LP",
      x: -40,
      y: -40,
      z: 50,
      colorValue: 4,
      sizeValue: 4,
    },
  ],
  edges: [
    {
      first: 0,
      second: 1,
      colorValue: 2,
    },
    {
      first: 0,
      second: 2,
      colorValue: -3,
    },
    {
      first: 0,
      second: 3,
      colorValue: 4,
    },
    {
      first: 1,
      second: 3,
      colorValue: 6,
    },
  ],
}; //connectome{}
var volumeList1 = [
  // first item is background image
  {
    url: "../images/mni152.nii.gz", //"./images/RAS.nii.gz",
	// "./images/spm152.nii.gz",
    colormap: "gray",
  },
];
let opts = {
  show3Dcrosshair: true,
  isColorbar: true,
  backColor: [0.8, 0.8, 1, 1],
  sliceType: niivue.SLICE_TYPE.RENDER,
};
var nv1 = new niivue.Niivue(opts);
nv1.attachTo("gl1");
await nv1.loadVolumes(volumeList1);
nv1.volumes[0].colorbarVisible = false;
await nv1.loadConnectome(connectome);
nv1.setClipPlane([-0.1, 270, 0]);
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function (e) {
    let id = nv1.meshes[0].id;
    if (e.shiftKey) id = nv1.meshes[1].id;
    nv1.setMeshShader(id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}
document.getElementById("reset").addEventListener("click", doReset);
function doReset() {
  nv1.setDefaults(opts, true);
  nv1.setClipPlane([-0.1, 270, 0]);
}

	
```
</td>
</tr>
</table>


# [Connectome API](https://niivue.github.io/niivue/features/connectome.api.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/4d80b48c-2226-4c24-8475-56f4952c3889.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var addNode = document.getElementById("addNode");
var deleteNode = document.getElementById("deleteNode");
var nodeName = document.getElementById("nodeName");
var nodeColor = document.getElementById("nodeColor");
nodeColor.value = 1;
var nodeSize = document.getElementById("nodeSize");
nodeSize.value = 1;
var addEdge = document.getElementById("addEdge");
var deleteEdge = document.getElementById("deleteEdge");
var firstIndex = document.getElementById("firstIndex");
var seceondIndex = document.getElementById("secondIndex");
var edgeColor = document.getElementById("edgeColor");

addNode.onclick = function () {
  var posMM = nv1.frac2mm(nv1.scene.crosshairPos);
  // nv1.meshes[0].addConnectomeNode({ 
  // name: nodeName.value, x: posMM[0], y: posMM[1], z: posMM[2], 
  // size: parseInt(nodeSize.value), color: parseInt(nodeColor.value) });

  nv1.meshes[0].addConnectomeNode({
    name: nodeName.value,
    x: posMM[0],
    y: posMM[1],
    z: posMM[2],
    colorValue: parseInt(nodeColor.value),
    sizeValue: parseInt(nodeSize.value),
  });
  nv1.meshes[0].updateMesh(nv1.gl);
  nv1.updateGLVolume();
};

deleteNode.onclick = function () {
  var posMM = nv1.frac2mm(nv1.scene.crosshairPos);
  var node = nv1.meshes[0].findClosestConnectomeNode(posMM, 15);
  if (node) {
    nv1.meshes[0].deleteConnectomeNode(node);
  }
  nv1.drawScene();
};

addEdge.onclick = function () {
  nv1.meshes[0].addConnectomeEdge(
    parseInt(firstIndex.value),
    parseInt(seceondIndex.value),
    parseInt(edgeColor.value)
  );
  nv1.drawScene();
};

deleteEdge.onclick = function () {
  nv1.meshes[0].deleteConnectomeEdge(
    parseInt(firstIndex.value),
    parseInt(seceondIndex.value)
  );
  nv1.drawScene();
};

let connectome = {
  name: "simpleConnectome",
  nodeColormap: "warm",
  nodeColormapNegative: "winter",
  nodeMinColor: 1,
  nodeMaxColor: 4,
  nodeScale: 3, //scale factor for node, e.g. if 2 and a node has size 3, \
  // a 6mm ball is drawn
  edgeColormap: "warm",
  edgeColormapNegative: "winter",
  edgeMin: 2,
  edgeMax: 6,
  edgeScale: 1,
  nodes: [
    {
      name: "RF",
      x: 40,
      y: 40,
      z: 30,
      colorValue: 2,
      sizeValue: 2,
    },
    {
      name: "LF",
      x: -40,
      y: 40,
      z: 20,
      colorValue: 2,
      sizeValue: 2,
    },
    {
      name: "RP",
      x: 40,
      y: -40,
      z: 50,
      colorValue: 3,
      sizeValue: 3,
    },
    {
      name: "LP",
      x: -40,
      y: -40,
      z: 50,
      colorValue: 4,
      sizeValue: 4,
    },
  ],
  edges: [
    {
      first: 0,
      second: 1,
      colorValue: 2,
    },
    {
      first: 0,
      second: 2,
      colorValue: -3,
    },
    {
      first: 0,
      second: 3,
      colorValue: 4,
    },
    {
      first: 1,
      second: 3,
      colorValue: 6,
    },
  ],
}; //connectome{}
var volumeList1 = [
  // first item is background image
  {
    url: "../images/mni152.nii.gz", //"./images/RAS.nii.gz",
    // "./images/spm152.nii.gz",
    colormap: "gray",
  },
];
let opts = {
  show3Dcrosshair: true,
  isColorbar: true,
  backColor: [0.8, 0.8, 1, 1],
  sliceType: niivue.SLICE_TYPE.RENDER,
};
var nv1 = new niivue.Niivue(opts);
nv1.attachTo("gl1");
await nv1.loadVolumes(volumeList1);
nv1.volumes[0].colorbarVisible = false;
await nv1.loadConnectome(connectome);
nv1.setClipPlane([-0.1, 270, 0]);
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function (e) {
    let id = nv1.meshes[0].id;
    if (e.shiftKey) id = nv1.meshes[1].id;
    nv1.setMeshShader(id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>


# [Minimal user interface with menus](https://niivue.github.io/niivue/features/ui.html) 

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/a0217c1d-1b74-4ddb-840c-5d0e09969b37.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

const isTouchDevice =
  "ontouchstart" in window ||
  navigator.maxTouchPoints > 0 ||
  navigator.msMaxTouchPoints > 0;
function handleIntensityChange(data) {
  document.getElementById("intensity").innerHTML = "&nbsp;&nbsp;" + data.string;
}
var nv1 = new niivue.Niivue({
  logging: true,
  dragAndDropEnabled: true,
  // backColor: [0, 0, 0, 1],
  show3Dcrosshair: true,
  onLocationChange: handleIntensityChange,
});
nv1.opts.isColorbar = true;
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
nv1.setClipPlane([0.3, 270, 0]);
nv1.setRenderAzimuthElevation(120, 10);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.setSliceMM(true);
nv1.opts.multiplanarForceRender = true;
nv1.graph.autoSizeMultiplanar = true;
nv1.graph.opacity = 1.0;
var volumeList1 = [{ url: "../images/mni152.nii.gz" }];
await nv1.loadVolumes(volumeList1);
function toggleGroup(id) {
  let buttons = document.getElementsByClassName("viewBtn");
  let char0 = id.charAt(0);
  for (let i = 0; i < buttons.length; i++) {
    if (buttons[i].id.charAt(0) !== char0) continue;
    buttons[i].classList.remove("dropdown-item-checked");
    if (buttons[i].id === id) buttons[i].classList.add("dropdown-item-checked");
  }
} // toggleGroup()
async function onButtonClick(event) {
  if (isTouchDevice) {
    console.log("Touch device: click menu to close menu");
    /*var el = this.parentNode
      el.style.display = "none"
      setTimeout(function() { //close menu
        //el.style.removeProperty("display")
        //el.style.display = "block"
      }, 500)*/
  }
  if (event.target.id === "SaveBitmap") {
    nv1.saveScene("ScreenShot.png");
    return;
  }
  if (event.target.id === "ShowHeader") {
    alert(nv1.volumes[0].hdr.toFormattedString());
    return;
  }
  if (event.target.id === "Colorbar") {
    nv1.opts.isColorbar = !nv1.opts.isColorbar;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
    return;
  }
  if (event.target.id === "Radiological") {
    nv1.opts.isRadiologicalConvention = !nv1.opts.isRadiologicalConvention;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
    return;
  }
  if (event.target.id === "Crosshair") {
    nv1.opts.show3Dcrosshair = !nv1.opts.show3Dcrosshair;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
  }
  if (event.target.id === "ClipPlane") {
    if (nv1.scene.clipPlaneDepthAziElev[0] > 1) nv1.setClipPlane([0.3, 270, 0]);
    else nv1.setClipPlane([2, 270, 0]);
    nv1.drawScene();
    return;
  }
  if (event.target.id.charAt(0) === "!") {
    // set color scheme
    //nv1.volumes[0].colormap = cmaps[i];
    nv1.volumes[0].colormap = event.target.id.substr(1);
    nv1.updateGLVolume();
    toggleGroup(event.target.id);
    return;
  }
  if (event.target.id.charAt(0) === "|") {
    //sliceType
    if (event.target.id === "|Axial") nv1.setSliceType(nv1.sliceTypeAxial);
    if (event.target.id === "|Coronal") nv1.setSliceType(nv1.sliceTypeCoronal);
    if (event.target.id === "|Sagittal")
      nv1.setSliceType(nv1.sliceTypeSagittal);
    if (event.target.id === "|Render") nv1.setSliceType(nv1.sliceTypeRender);
    if (event.target.id === "|MultiPlanar") {
      nv1.opts.multiplanarForceRender = false;
      nv1.setSliceType(nv1.sliceTypeMultiplanar);
    }
    if (event.target.id === "|MultiPlanarRender") {
      nv1.opts.multiplanarForceRender = true;
      nv1.setSliceType(nv1.sliceTypeMultiplanar);
    }
    toggleGroup(event.target.id);
  } //sliceType
  if (event.target.id === "BackColor") {
    if (nv1.opts.backColor[0] < 0.5) nv1.opts.backColor = [1, 1, 1, 1];
    else nv1.opts.backColor = [0, 0, 0, 1];
    nv1.drawScene();
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id.charAt(0) === "^") {
    //drag mode
    let s = event.target.id.substr(1);
    switch (s) {
      case "none":
        nv1.opts.dragMode = nv1.dragModes.none;
        break;
      case "contrast":
        nv1.opts.dragMode = nv1.dragModes.contrast;
        break;
      case "measurement":
        nv1.opts.dragMode = nv1.dragModes.measurement;
        break;
      case "pan":
        nv1.opts.dragMode = nv1.dragModes.pan;
        break;
    }
    toggleGroup(event.target.id);
  } //drag mode
  if (event.target.id === "_mesh") {
    volumeList1[0].url = "../images//mni152.nii.gz";
    await nv1.loadVolumes(volumeList1);
    nv1.loadMeshes([
      {
        url: "../images/BrainMesh_ICBM152.lh.mz3",
        rgba255: [200, 162, 255, 255],
      },
      { url: "../images/dpsv.trx", rgba255: [255, 255, 255, 255] },
    ]);
    toggleGroup(event.target.id);
  } else if (event.target.id.charAt(0) === "_") {
    //example image
    nv1.meshes = []; //close open meshes
    let root = "../images/";
    let s = event.target.id.substr(1);
    let img = root + s + ".nii.gz";
    console.log("Loading " + img);
    volumeList1[0].url = img;
    nv1.loadVolumes(volumeList1);
    toggleGroup(event.target.id);
    nv1.updateGLVolume();
  } //example image
} // onButtonClick()
var buttons = document.getElementsByClassName("viewBtn");
for (let i = 0; i < buttons.length; i++)
  buttons[i].addEventListener("click", onButtonClick, false);

	
```
</td>
</tr>
</table>


# [Meshes (GIfTI, FreeSurfer, MZ3, OBJ, STL, legacy VTK)](https://niivue.github.io/niivue/features/meshes.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/1cd480ec-ed78-4214-ade9-2e4e11da9f5c.png)



</td>
<td>

	
```javascript
import * as niivue from "../dist/index.js";
  
var slider = document.getElementById("meshSlider");
slider.oninput = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "rgba255", [
    this.value,
    164,
    164,
    255,
  ]);
};
document.getElementById("reverse").addEventListener("click", doReverse);
function doReverse() {
  nv1.reverseFaces(nv1.meshes[0].id);
}
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [0.9, 0.9, 1, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
await nv1.loadMeshes([
  {
    url: "../images/BrainMesh_ICBM152.lh.mz3",
    rgba255: [222, 164, 164, 255],
  },
  { url: "../images/CIT168.mz3", rgba255: [0, 0, 255, 255] },
]);
nv1.setMeshShader(nv1.meshes[0].id, "Outline");
nv1.setClipPlane([-0.1, 270, 0]);
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>

# [Mesh MatCaps](https://niivue.github.io/niivue/features/mesh.matcap.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/af34b233-1b19-43d0-a710-e41fa5064b2a.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
var slider = document.getElementById("meshSlider");
slider.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "cal_min", this.value * 0.1);
};
document.getElementById("matCaps").addEventListener("change", doMatCap);
function doMatCap() {
  nv1.setMeshShader(nv1.meshes[0].id, "Matcap");
  let matCapName = document.getElementById("matCaps").value;
  nv1.loadMatCapTexture("../matcaps/" + matCapName + ".jpg");
}
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [1, 1, 1, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
nv1.opts.isColorbar = true;
var meshLHLayersList1 = [
  {
    url: "../images/BrainMesh_ICBM152.lh.motor.mz3",
    cal_min: 2,
    cal_max: 5,
    useNegativeCmap: true,
    opacity: 0.7,
  },
];
await nv1.loadMeshes([
  { url: "../images/BrainMesh_ICBM152.lh.mz3", layers: meshLHLayersList1 },
]);
nv1.setMeshShader(nv1.meshes[0].id, "Matcap");
nv1.setClipPlane([-0.1, 270, 0]);

	
```
</td>
</tr>
</table>

# [Mesh Statistics](https://niivue.github.io/niivue/features/mesh.stats.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/2071f593-e149-44ee-a078-a53fc78045f2.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
curveSlider.onchange = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value * 0.1);
};
document
  .getElementById("threshSlider")
  .addEventListener("change", doThreshChange);
document
  .getElementById("rangeSlider")
  .addEventListener("change", doThreshChange);
function doThreshChange() {
  let mn = document.getElementById("threshSlider").value * 1.0;
  let mx = mn + document.getElementById("rangeSlider").value * 1.0;
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "cal_min", mn);
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "cal_max", mx);
}
shaderDrop.onchange = function () {
  const shaderName = this.value;
  nv1.setMeshShader(nv1.meshes[0].id, shaderName);
};
check1.onchange = function () {
  if (!check1.checked) {
    nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "colormap", "warm");
    nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "colormapNegative", "winter");
  } else {
    nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "colormap", "green2orange");
    nv1.setMeshLayerProperty(
      nv1.meshes[0].id,
      1,
      "colormapNegative",
      "green2cyan"
    );
  }
};
check2.onchange = function () {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    1,
    "alphaThreshold",
    check2.checked
  );
};
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [0, 0, 0, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
nv1.opts.isColorbar = true;
var meshLHLayersList1 = [
  {
    url: "../images/BrainMesh_ICBM152.lh.curv",
    colormap: "gray",
    cal_min: 0.3,
    cal_max: 0.5,
    opacity: 0.7,
  },
  {
    url: "../images/BrainMesh_ICBM152.lh.motor.mz3",
    cal_min: 2,
    cal_max: 5,
    colormap: "green2orange",
    colormapNegative: "green2cyan",
    useNegativeCmap: true,
    opacity: 0.7,
  },
];
await nv1.loadMeshes([
  { url: "../images/BrainMesh_ICBM152.lh.mz3", layers: meshLHLayersList1 },
]);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "colorbarVisible", false);
nv1.setClipPlane([-0.1, 270, 0]);
doThreshChange();
shaderDrop.onchange();

	
```
</td>
</tr>
</table>

# [Mesh layers (GIfTI, FreeSurfer, MZ3)](https://niivue.github.io/niivue/features/mesh.layers.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/09814eb7-6aa7-48ce-a13d-7d567c331286.png)



</td>
<td>

	
```javascript


import * as niivue from "../dist/index.js";
  
var checkbox1 = document.getElementById("meshCheckbox1");
checkbox1.onclick = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, 'visible', checkbox1.checked);
  console.log(`visible=${nv1.meshes[0].visible}`);
}
var slider2 = document.getElementById("meshSlider2");
slider2.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "cal_min", this.value * 0.1);
};
var slider3 = document.getElementById("meshSlider3");
slider3.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value * 0.1);
};
function handleLocationChange(data) {
  document.getElementById("location").innerHTML =
    "&nbsp;&nbsp;" + data.string;
}
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  onLocationChange: handleLocationChange,
  backColor: [1, 1, 1, 1],
  meshXRay: 0.3
});
nv1.attachTo("gl1");
nv1.opts.isColorbar = true;
var meshLHLayersList1 = [
  {
    url: "../images/BrainMesh_ICBM152.lh.motor.mz3",
    cal_min: 0.5,
    cal_max: 5.5,
    useNegativeCmap: true,
    opacity: 0.7,
  },
];
await nv1.loadMeshes([
  {
    url: "../images/BrainMesh_ICBM152.lh.mz3",
    rgba255: [255, 255, 255, 255],
    layers: meshLHLayersList1,
  },
  { url: "../images/CIT168.mz3", rgba255: [0, 0, 255, 255] },
]);
//n.b. one can also create asymmetric thresholds by explicitly 
// setting negative values:
// nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, 'cal_maxNeg', -5.0)
// nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, 'cal_minNeg', -0.5)
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>

# [Load Mesh Layers](https://niivue.github.io/niivue/features/mesh.loader.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/a21f371d-404c-4b7b-9730-04db6fdeae4d.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var checkbox1 = document.getElementById("meshCheckbox1");
checkbox1.onclick = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "visible", checkbox1.checked);
  console.log(`visible=${nv1.meshes[0].visible}`);
};
var slider2 = document.getElementById("meshSlider2");
slider2.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "cal_min", this.value * 0.1);
};
var slider3 = document.getElementById("meshSlider3");
slider3.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value * 0.1);
};

var button = document.getElementById("addMeshLayerButton");
button.onclick = async () => {
  const layer = {
    url: "../images/BrainMesh_ICBM152.lh.motor.mz3",
    cal_min: 0.5,
    cal_max: 5.5,
    useNegativeCmap: true,
    opacity: 0.7,
  };
  const response = await fetch(layer.url);
  if (!response.ok) {
    throw Error(response.statusText);
  }
  const buffer = await response.arrayBuffer();
  niivue.NVMeshLoaders.readLayer(
    layer.url,
    buffer,
    nv1.meshes[0],
    layer.opacity,
    "gray",
    undefined,
    layer.useNegativeCmap
  );
  nv1.meshes[0].updateMesh(nv1.gl);
  nv1.drawScene();
  console.log("mesh updated");
};

function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  onLocationChange: handleLocationChange,
  backColor: [1, 1, 1, 1],
  meshXRay: 0.3,
});
nv1.attachTo("gl1");
nv1.opts.isColorbar = true;

await nv1.loadMeshes([
  {
    url: "../images/BrainMesh_ICBM152.lh.mz3",
    rgba255: [255, 255, 255, 255],
  },
  { url: "../images/CIT168.mz3", rgba255: [0, 0, 255, 255] },
]);

let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>

# [4D mesh time series (GIfTI, FreeSurfer, MZ3)](https://niivue.github.io/niivue/features/mesh.4D.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/3ec12dd1-5f30-465d-b9fb-53f9e0d4db5b.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var slider = document.getElementById("meshSlider");
slider.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "frame4D", this.value);
};
var slider2 = document.getElementById("meshSlider2");
slider2.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value * 0.1);
};
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [0.9, 0.9, 1, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
var meshLHLayersList1 = [
  {
    url: "../images/Human.colin.R.FUNCTIONAL.71723.func.gii",
    colormap: "rocket",
    opacity: 0.7,
  },
];
nv1.loadMeshes([
  {
    url: "../images/Human.colin.Cerebral.R.VERY_INFLATED.71723.surf.gii",
    rgba255: [255, 255, 255, 255],
    layers: meshLHLayersList1,
  },
]);
nv1.setClipPlane([-0.1, 270, 0]);
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>

# [annot mesh atlases](https://niivue.github.io/niivue/features/mesh.atlas.html) 

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/61461b47-712b-4e16-a5fd-6fa31f801881.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var slider = document.getElementById("meshSlider");
slider.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "opacity", this.value / 255.0);
};
var slider2 = document.getElementById("meshSlider2");
slider2.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 2, "opacity", this.value / 255.0);
};
document.getElementById("check1").addEventListener("change", doCheck1Click);
function doCheck1Click() {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    1,
    "isOutlineBorder",
    this.checked
  );
}
document.getElementById("check2").addEventListener("change", doCheck2Click);
function doCheck2Click() {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    2,
    "isOutlineBorder",
    this.checked
  );
}
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [0.9, 0.9, 1, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
var meshLayersList1 = [
  {
    url: "../images/lh.curv",
    colormap: "gray",
    cal_min: 0.3,
    cal_max: 0.5,
    opacity: 1,
  },
  { url: "../images/boggle.lh.annot", colormap: "rocket", opacity: 0.5 },
  {
    url: "../images/pval.LH.nii.gz",
    cal_min: 25,
    cal_max: 35.0,
    opacity: 0.9,
  },
];
await nv1.loadMeshes([
  {
    url: "../images/lh.pial",
    rgba255: [255, 255, 255, 255],
    layers: meshLayersList1,
  },
  //{url: "../images/CIT168.mz3", rgba255 : [0, 0, 255, 255]},
]);
nv1.setClipPlane([-0.1, 270, 0]);
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}
document
  .getElementById("customShader")
  .addEventListener("click", doCustomShader);
function doCustomShader() {
  let idx = nv1.setCustomMeshShader(
    document.getElementById("customText").value
  );
  let id = nv1.meshes[0].id;
  nv1.setMeshShader(id, idx);
}

	
```
</td>
</tr>
</table>

# [GIFTI mesh atlases](https://niivue.github.io/niivue/features/mesh.atlas.gii.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/5db693b5-fda7-4dde-99d8-7ca1c10c2f62.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var slider = document.getElementById("meshSlider");
slider.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value / 255.0);
};
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [0.2, 0.2, 0.2, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
//you can convert between GIfTI and FreeSurfer annot files:
// mris_convert  --annot lh.Yeo2011_7Networks_N1000.annot lh.pial ./lh.Yeo2011.gii
var meshLayersList1 = [
  { url: "../images/lh.Yeo2011.gii", opacity: 0.5 }, //boggle.lh.annot lh.boggle.gii
];
await nv1.loadMeshes([
  {
    url: "../images/lh.pial",
    rgba255: [255, 255, 255, 255],
    layers: meshLayersList1,
  },
]);
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}
document
  .getElementById("customColormap")
  .addEventListener("click", doCustomColormap);
function doCustomColormap() {
  var val = document.getElementById("scriptText").value;
  val +=
    ';nv1.setMeshLayerProperty(nv1.meshes[0].id,0,"colormapLabel",cmap);nv1.updateGLVolume();';
  val && eval(val);
}

	
```
</td>
</tr>
</table>

# [MGH mesh atlases](https://niivue.github.io/niivue/features/mesh.atlas.mgh.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/e43788dc-1f75-4129-85fd-a355a5ece936.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var slider = document.getElementById("meshSlider");
slider.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value / 255.0);
};
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [0.4, 0.4, 0.4, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
//you can convert between GIfTI and FreeSurfer annot files:
// mris_convert  --annot lh.Yeo2011_7Networks_N1000.annot lh.pial ./lh.Yeo2011.gii
var meshLayersList1 = [
  { url: "../images/lh.Yeo2011.mgz", opacity: 0.5 }, //boggle.lh.annot lh.boggle.gii
];
await nv1.loadMeshes([
  {
    url: "../images/lh.pial",
    rgba255: [255, 255, 255, 255],
    layers: meshLayersList1,
  },
]);
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}
document
  .getElementById("customColormap")
  .addEventListener("click", doCustomColormap);
function doCustomColormap() {
  var val = document.getElementById("scriptText").value;
  val +=
    ';nv1.setMeshLayerProperty(nv1.meshes[0].id,0,"colormapLabel",cmap);nv1.updateGLVolume();';
  val && eval(val);
}

	
```
</td>
</tr>
</table>

# [GIfTI Meshes with NIfTI2 Curvature](https://niivue.github.io/niivue/features/mesh.curv.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/e12f93e7-939e-45d4-bea3-827c96b97e49.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
var slider0 = document.getElementById("meshSlider0");
slider0.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value / 255.0);
};
document.getElementById("check10").addEventListener("change", doCheck10Click);
function doCheck10Click() {
  nv1.setHighResolutionCapable(this.checked);
}
document.getElementById("matCaps").addEventListener("change", doMatCap);
function doMatCap() {
  nv1.setMeshShader(nv1.meshes[0].id, "Matcap");
  let matCapName = document.getElementById("matCaps").value;
  nv1.loadMatCapTexture("../matcaps/" + matCapName + ".jpg");
}
var nv1 = new niivue.Niivue({
  loadingText: "there are no images",
  backColor: [1, 1, 1, 1],
  show3Dcrosshair: true,
  logging: true,
});
var meshLayersList1 = [
  {
    url: "../images/fs_LR.32k.LR.curvature.dscalar.nii",
    colormap: "gray",
    cal_min: -0.15,
    cal_max: -0.001,
    opacity: 222 / 255,
  },
];
nv1.attachTo("gl1");
await nv1.loadMeshes([
  {
    url: "../images/fs_LR.32k.L.inflated.surf.gii",
    layers: meshLayersList1,
  },
]);
nv1.setMeshShader(nv1.meshes[0].id, "Matcap");
nv1.setMeshLayerProperty(
  nv1.meshes[0].id,
  0,
  "isTransparentBelowCalMin",
  false
);
document.getElementById("check10").checked = nv1.opts.isHighResolutionCapable;
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>

# Anti-Aliasing: Auto-select [Mesh](https://niivue.github.io/niivue/features/mesh.freesurfer.html)   

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/77c5441e-3f86-4245-aa87-4d02e10132d5.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
var slider0 = document.getElementById("meshSlider0");
slider0.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value / 255.0);
};
var slider1 = document.getElementById("meshSlider1");
slider1.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "opacity", this.value / 255.0);
};
var slider2 = document.getElementById("meshSlider2");
slider2.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 2, "opacity", this.value / 255.0);
};
var slider3 = document.getElementById("meshSlider3");
slider3.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 2, "cal_min", this.value);
};
document.getElementById("check1").addEventListener("change", doCheck1Click);
function doCheck1Click() {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    1,
    "isOutlineBorder",
    this.checked
  );
}
document.getElementById("check2").addEventListener("change", doCheck2Click);
function doCheck2Click() {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    2,
    "isOutlineBorder",
    this.checked
  );
}
document.getElementById("check10").addEventListener("change", doCheck10Click);
function doCheck10Click() {
  nv1.setHighResolutionCapable(this.checked);
}
document.getElementById("check11").addEventListener("change", doCheck11Click);
function doCheck11Click() {
  nv1.opts.meshXRay = Number(this.checked) * 0.02;
  nv1.drawScene();
}
document.getElementById("matCaps").addEventListener("change", doMatCap);
function doMatCap() {
  nv1.setMeshShader(nv1.meshes[0].id, "Matcap");
  let matCapName = document.getElementById("matCaps").value;
  nv1.loadMatCapTexture("../matcaps/" + matCapName + ".jpg");
}
var nv1 = new niivue.Niivue({
  loadingText: "there are no images",
  backColor: [1, 1, 1, 1],
  show3Dcrosshair: true,
  logging: true,
  isOrientCube: true,
});
var meshLayersList1 = [
  {
    url: "../images/lh.curv",
    colormap: "gray",
    cal_min: 0.3,
    cal_max: 0.5,
    opacity: 222 / 255,
  },
  { url: "../images/boggle.lh.annot", colormap: "rocket", opacity: 1 },
  {
    url: "../images/pval.LH.nii.gz",
    cal_min: 25,
    cal_max: 35.0,
    opacity: 1,
  },
];
nv1.attachTo("gl1");
await nv1.loadMeshes([{ url: "../images/lh.pial", layers: meshLayersList1 }]);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "isOutlineBorder", true);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "colorbarVisible", false);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "colorbarVisible", false);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 2, "colormapNegative", "");
document.getElementById("check10").checked = nv1.opts.isHighResolutionCapable;
nv1.opts.isColorbar = true;
nv1.setMeshShader(nv1.meshes[0].id, "Matcap");
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>

# Anti-Aliasing: Auto-Select [Voxel](https://niivue.github.io/niivue/features/vox.aaAUTO.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/ef94b849-2804-404d-b525-d64f035f9620.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var drop = document.getElementById("sliceType");
drop.onchange = function () {
  let st = parseInt(document.getElementById("sliceType").value);
  nv1.setSliceType(st);
};
document
  .getElementById("retinaCheck")
  .addEventListener("change", doRetinaCheck);
function doRetinaCheck() {
  nv1.setHighResolutionCapable(this.checked);
}
function handleIntensityChange(data) {
  document.getElementById("intensity").innerHTML = "&nbsp;&nbsp;" + data.string;
  console.log(data);
}
var volumeList1 = [
  { url: "../images/mni152.nii.gz" },
  {
    url: "../images/stats.nv_demo_mskd.nii.gz",
    colormap: "warm",
    colormapNegative: "winter",
    frame4D: 1,
    cal_min: 3.3641,
    cal_max: 6,
  },
];
var nv1 = new niivue.Niivue({
  logging: true,
  show3Dcrosshair: true,
  onLocationChange: handleIntensityChange,
});
nv1.attachTo("gl1");
nv1.opts.isColorbar = true;
nv1.opts.multiplanarForceRender = true;
await nv1.loadVolumes(volumeList1);
nv1.volumes[0].colorbarVisible = false; //hide colorbar for anatomical scan
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.updateGLVolume();

	
```
</td>
</tr>
</table>

# Anti-Aliasing: OFF (faster) [Mesh](https://niivue.github.io/niivue/features/mesh.freesurfer.aaOFF.html)  

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/66b1d1d1-cb30-40c4-9dd6-d42daa7a4ffd.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
var slider0 = document.getElementById("meshSlider0");
slider0.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value / 255.0);
};
var slider1 = document.getElementById("meshSlider1");
slider1.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "opacity", this.value / 255.0);
};
var slider2 = document.getElementById("meshSlider2");
slider2.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 2, "opacity", this.value / 255.0);
};
var slider3 = document.getElementById("meshSlider3");
slider3.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 2, "cal_min", this.value);
};
document.getElementById("check1").addEventListener("change", doCheck1Click);
function doCheck1Click() {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    1,
    "isOutlineBorder",
    this.checked
  );
}
document.getElementById("check2").addEventListener("change", doCheck2Click);
function doCheck2Click() {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    2,
    "isOutlineBorder",
    this.checked
  );
}
document.getElementById("check10").addEventListener("change", doCheck10Click);
function doCheck10Click() {
  nv1.setHighResolutionCapable(this.checked);
}
document.getElementById("check11").addEventListener("change", doCheck11Click);
function doCheck11Click() {
  nv1.opts.meshXRay = Number(this.checked) * 0.02;
  nv1.drawScene();
}
document.getElementById("matCaps").addEventListener("change", doMatCap);
function doMatCap() {
  nv1.setMeshShader(nv1.meshes[0].id, "Matcap");
  let matCapName = document.getElementById("matCaps").value;
  nv1.loadMatCapTexture("../matcaps/" + matCapName + ".jpg");
}
var nv1 = new niivue.Niivue({
  loadingText: "there are no images",
  backColor: [1, 1, 1, 1],
  show3Dcrosshair: true,
  logging: true,
  isOrientCube: true,
});
var meshLayersList1 = [
  {
    url: "../images/lh.curv",
    colormap: "gray",
    cal_min: 0.3,
    cal_max: 0.5,
    opacity: 222 / 255,
  },
  { url: "../images/boggle.lh.annot", colormap: "rocket", opacity: 1 },
  {
    url: "../images/pval.LH.nii.gz",
    cal_min: 25,
    cal_max: 35.0,
    opacity: 1,
  },
];
nv1.attachTo("gl1", false);
await nv1.loadMeshes([{ url: "../images/lh.pial", layers: meshLayersList1 }]);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "isOutlineBorder", true);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "colorbarVisible", false);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "colorbarVisible", false);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 2, "colormapNegative", "");
document.getElementById("check10").checked = nv1.opts.isHighResolutionCapable;
nv1.opts.isColorbar = true;
nv1.setMeshShader(nv1.meshes[0].id, "Matcap");
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>

# Anti-Aliasing: OFF (faster) [Voxel](https://niivue.github.io/niivue/features/vox.aaOFF.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/99ba37a7-9de7-445b-bb6b-a1de87f483b8.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var drop = document.getElementById("sliceType");
drop.onchange = function () {
  let st = parseInt(document.getElementById("sliceType").value);
  nv1.setSliceType(st);
};
document
  .getElementById("retinaCheck")
  .addEventListener("change", doRetinaCheck);
function doRetinaCheck() {
  nv1.setHighResolutionCapable(this.checked);
}
function handleIntensityChange(data) {
  document.getElementById("intensity").innerHTML = "&nbsp;&nbsp;" + data.string;
  console.log(data);
}
var volumeList1 = [
  { url: "../images/mni152.nii.gz" },
  {
    url: "../images/stats.nv_demo_mskd.nii.gz",
    colormap: "warm",
    colormapNegative: "winter",
    frame4D: 1,
    cal_min: 3.3641,
    cal_max: 6,
  },
];
var nv1 = new niivue.Niivue({
  logging: true,
  show3Dcrosshair: true,
  onLocationChange: handleIntensityChange,
});
nv1.attachTo("gl1", false);
nv1.opts.isColorbar = true;
nv1.opts.multiplanarForceRender = true;
await nv1.loadVolumes(volumeList1);
nv1.volumes[0].colorbarVisible = false; //hide colorbar for anatomical scan
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.updateGLVolume();

	
```
</td>
</tr>
</table>

# Anti-Aliasing: ON (better) [Mesh](https://niivue.github.io/niivue/features/mesh.freesurfer.aaON.html)   

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/fc2cab80-e103-46c6-94c5-cfce76aec086.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
var slider0 = document.getElementById("meshSlider0");
slider0.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value / 255.0);
};
var slider1 = document.getElementById("meshSlider1");
slider1.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "opacity", this.value / 255.0);
};
var slider2 = document.getElementById("meshSlider2");
slider2.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 2, "opacity", this.value / 255.0);
};
var slider3 = document.getElementById("meshSlider3");
slider3.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 2, "cal_min", this.value);
};
document.getElementById("check1").addEventListener("change", doCheck1Click);
function doCheck1Click() {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    1,
    "isOutlineBorder",
    this.checked
  );
}
document.getElementById("check2").addEventListener("change", doCheck2Click);
function doCheck2Click() {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    2,
    "isOutlineBorder",
    this.checked
  );
}
document.getElementById("check10").addEventListener("change", doCheck10Click);
function doCheck10Click() {
  nv1.setHighResolutionCapable(this.checked);
}
document.getElementById("check11").addEventListener("change", doCheck11Click);
function doCheck11Click() {
  nv1.opts.meshXRay = Number(this.checked) * 0.02;
  nv1.drawScene();
}
document.getElementById("matCaps").addEventListener("change", doMatCap);
function doMatCap() {
  nv1.setMeshShader(nv1.meshes[0].id, "Matcap");
  let matCapName = document.getElementById("matCaps").value;
  nv1.loadMatCapTexture("../matcaps/" + matCapName + ".jpg");
}
var nv1 = new niivue.Niivue({
  loadingText: "there are no images",
  backColor: [1, 1, 1, 1],
  show3Dcrosshair: true,
  logging: true,
  isOrientCube: true,
});
var meshLayersList1 = [
  {
    url: "../images/lh.curv",
    colormap: "gray",
    cal_min: 0.3,
    cal_max: 0.5,
    opacity: 222 / 255,
  },
  { url: "../images/boggle.lh.annot", colormap: "rocket", opacity: 1 },
  {
    url: "../images/pval.LH.nii.gz",
    cal_min: 25,
    cal_max: 35.0,
    opacity: 1,
  },
];
nv1.attachTo("gl1", true);
await nv1.loadMeshes([{ url: "../images/lh.pial", layers: meshLayersList1 }]);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "isOutlineBorder", true);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "colorbarVisible", false);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "colorbarVisible", false);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 2, "colormapNegative", "");
document.getElementById("check10").checked = nv1.opts.isHighResolutionCapable;
nv1.opts.isColorbar = true;
nv1.setMeshShader(nv1.meshes[0].id, "Matcap");
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>

# Anti-Aliasing: ON (better) [Voxel](https://niivue.github.io/niivue/features/vox.aaON.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/548adef0-535f-44c5-8ad3-56aea8caaa3e.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var drop = document.getElementById("sliceType");
drop.onchange = function () {
  let st = parseInt(document.getElementById("sliceType").value);
  nv1.setSliceType(st);
};
document
  .getElementById("retinaCheck")
  .addEventListener("change", doRetinaCheck);
function doRetinaCheck() {
  nv1.setHighResolutionCapable(this.checked);
}
function handleIntensityChange(data) {
  document.getElementById("intensity").innerHTML = "&nbsp;&nbsp;" + data.string;
  console.log(data);
}
var volumeList1 = [
  { url: "../images/mni152.nii.gz" },
  {
    url: "../images/stats.nv_demo_mskd.nii.gz",
    colormap: "warm",
    colormapNegative: "winter",
    frame4D: 1,
    cal_min: 3.3641,
    cal_max: 6,
  },
];
var nv1 = new niivue.Niivue({
  logging: true,
  show3Dcrosshair: true,
  onLocationChange: handleIntensityChange,
});
nv1.attachTo("gl1", true);
nv1.opts.isColorbar = true;
nv1.opts.multiplanarForceRender = true;
await nv1.loadVolumes(volumeList1);
nv1.volumes[0].colorbarVisible = false; //hide colorbar for anatomical scan
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.updateGLVolume();

	
```
</td>
</tr>
</table>

# [FreeSurfer mask editing](https://niivue.github.io/niivue/features/freesurfer.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/35902df6-1f55-4072-950d-941659eddb03.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

const isTouchDevice =
  "ontouchstart" in window ||
  navigator.maxTouchPoints > 0 ||
  navigator.msMaxTouchPoints > 0;
var isFilled = true;
function handleIntensityChange(data) {
  document.getElementById("intensity").innerHTML = "&nbsp;&nbsp;" + data.string;
}
var nv1 = new niivue.Niivue({
  logging: true,
  dragAndDropEnabled: true,
  backColor: [0, 0, 0, 1],
  show3Dcrosshair: true,
  onLocationChange: handleIntensityChange,
});
nv1.opts.isColorbar = false;
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
nv1.setClipPlane([0.3, 270, 0]);
nv1.setRenderAzimuthElevation(120, 10);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.setSliceMM(true);
nv1.drawOpacity = 0.5;
nv1.opts.isColorbar = false;
var volumeList1 = [{ url: "../images/fs/brainmask.mgz" }];
await nv1.loadVolumes(volumeList1);
await nv1.loadDrawingFromUrl("../images/fs/wm.mgz", true);
nv1.setMeshThicknessOn2D(0.35);
await nv1.loadMeshes([
  { url: "../images/fs/rh.pial", rgba255: [222, 22, 22, 255] },
  { url: "../images/fs/lh.pial", rgba255: [222, 22, 22, 255] },
  { url: "../images/fs/rh.white", rgba255: [222, 164, 0, 255] },
  { url: "../images/fs/lh.white", rgba255: [222, 164, 0, 255] },
]);
nv1.setInterpolation(true);
nv1.opts.dragMode = nv1.dragModes.slicer3D;
let cmap = {
  R: [0, 255, 0],
  G: [0, 20, 0],
  B: [0, 20, 80],
  A: [0, 255, 255],
  labels: ["", "white-matter", "delete T1"],
};
nv1.setDrawColormap(cmap);
function toggleGroup(id) {
  let buttons = document.getElementsByClassName("viewBtn");
  let char0 = id.charAt(0);
  for (let i = 0; i < buttons.length; i++) {
    if (buttons[i].id.charAt(0) !== char0) continue;
    buttons[i].classList.remove("dropdown-item-checked");
    if (buttons[i].id === id) buttons[i].classList.add("dropdown-item-checked");
  }
} // toggleGroup()
async function onButtonClick(event) {
  if (event.target.id === "SaveDraw") {
    nv1.saveImage({ filename: "draw.nii", isSaveDrawing: true });
    return;
  }
  if (event.target.id === "SaveBitmap") {
    nv1.saveScene("ScreenShot.png");
    return;
  }
  if (event.target.id === "ShowHeader") {
    alert(nv1.volumes[0].hdr.toFormattedString());
    return;
  }
  if (event.target.id === "Colorbar") {
    nv1.opts.isColorbar = !nv1.opts.isColorbar;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
    return;
  }
  if (event.target.id === "Radiological") {
    nv1.opts.isRadiologicalConvention = !nv1.opts.isRadiologicalConvention;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
    return;
  }
  if (event.target.id === "Crosshair") {
    nv1.opts.show3Dcrosshair = !nv1.opts.show3Dcrosshair;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
  }
  if (event.target.id === "ClipPlane") {
    if (nv1.scene.clipPlaneDepthAziElev[0] > 1) nv1.setClipPlane([0.3, 270, 0]);
    else nv1.setClipPlane([2, 270, 0]);
    nv1.drawScene();
    return;
  }
  if (event.target.id === "Undo") {
    nv1.drawUndo();
  }
  if (event.target.id.charAt(0) === "@") {
    //sliceType
    if (event.target.id === "@Off") nv1.setDrawingEnabled(false);
    else nv1.setDrawingEnabled(true);
    if (event.target.id === "@Erase") nv1.setPenValue(0, isFilled);
    if (event.target.id === "@Red") nv1.setPenValue(1, isFilled);
    if (event.target.id === "@Blue") nv1.setPenValue(2, isFilled);
    if (event.target.id === "@Cluster") nv1.setPenValue(-0, isFilled);
    if (event.target.id === "@GrowCluster") nv1.setPenValue(NaN, isFilled);
    if (event.target.id === "@GrowClusterBright")
      nv1.setPenValue(Number.POSITIVE_INFINITY, isFilled);
    if (event.target.id === "@GrowClusterDark")
      nv1.setPenValue(Number.NEGATIVE_INFINITY, isFilled);
    toggleGroup(event.target.id);
  } //Draw Color
  if (event.target.id === "Growcut") nv1.drawGrowCut();
  if (event.target.id === "Translucent") {
    if (nv1.drawOpacity > 0.75) nv1.drawOpacity = 0.5;
    else nv1.drawOpacity = 1.0;
    nv1.drawScene();
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "DrawOtsu") {
    let levels = parseInt(prompt("Segmentation classes (2..4)", "3"));
    nv1.drawOtsu(levels);
  }
  if (event.target.id === "RemoveHaze") {
    let level = parseInt(prompt("Remove Haze (1..5)", "5"));
    nv1.removeHaze(level);
  }
  if (event.target.id === "DrawFilled") {
    isFilled = !isFilled;
    nv1.setPenValue(nv1.opts.penValue, isFilled);
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "DrawOverwrite") {
    nv1.drawFillOverwrites = !nv1.drawFillOverwrites;
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id.charAt(0) === "|") {
    //sliceType
    if (event.target.id === "|Axial") nv1.setSliceType(nv1.sliceTypeAxial);
    if (event.target.id === "|Coronal") nv1.setSliceType(nv1.sliceTypeCoronal);
    if (event.target.id === "|Sagittal")
      nv1.setSliceType(nv1.sliceTypeSagittal);
    if (event.target.id === "|Render") nv1.setSliceType(nv1.sliceTypeRender);
    if (event.target.id === "|MultiPlanar") {
      nv1.opts.multiplanarForceRender = false;
      nv1.setSliceType(nv1.sliceTypeMultiplanar);
    }
    if (event.target.id === "|MultiPlanarRender") {
      nv1.opts.multiplanarForceRender = true;
      nv1.setSliceType(nv1.sliceTypeMultiplanar);
    }
    toggleGroup(event.target.id);
  } //sliceType
  if (event.target.id === "WorldSpace") {
    nv1.setSliceMM(!nv1.opts.isSliceMM);
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "Interpolate") {
    nv1.setInterpolation(!nv1.opts.isNearestInterpolation);
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "Left") nv1.moveCrosshairInVox(-1, 0, 0);
  if (event.target.id === "Right") nv1.moveCrosshairInVox(1, 0, 0);
  if (event.target.id === "Posterior") nv1.moveCrosshairInVox(0, -1, 0);
  if (event.target.id === "Anterior") nv1.moveCrosshairInVox(0, 1, 0);
  if (event.target.id === "Inferior") nv1.moveCrosshairInVox(0, 0, -1);
  if (event.target.id === "Superior") nv1.moveCrosshairInVox(0, 0, 1);
  if (event.target.id === "BackColor") {
    if (nv1.opts.backColor[0] < 0.5) nv1.opts.backColor = [1, 1, 1, 1];
    else nv1.opts.backColor = [0, 0, 0, 1];
    nv1.drawScene();
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id.charAt(0) === "^") {
    //drag mode
    let s = event.target.id.substr(1);
    switch (s) {
      case "none":
        nv1.opts.dragMode = nv1.dragModes.none;
        break;
      case "contrast":
        nv1.opts.dragMode = nv1.dragModes.contrast;
        break;
      case "measurement":
        nv1.opts.dragMode = nv1.dragModes.measurement;
        break;
      case "pan":
        nv1.opts.dragMode = nv1.dragModes.pan;
        break;
      case "slicer3D":
        nv1.opts.dragMode = nv1.dragModes.slicer3D;
        break;
    }
    toggleGroup(event.target.id);
  } //drag mode
} // onButtonClick()
var buttons = document.getElementsByClassName("viewBtn");
for (let i = 0; i < buttons.length; i++)
  buttons[i].addEventListener("click", onButtonClick, false);

	
```
</td>
</tr>
</table>

# [FreeSurfer point sets](https://niivue.github.io/niivue/features/pointset.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/f2568211-54df-40e7-ae02-95addda06a5d.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
import { esm } from "../dist/index.min.js";

save.onclick = function () {
  nv1.saveHTML("page.html", "gl1", decodeURIComponent(esm));
};
about.onclick = function () {
  window.alert(
    "The demo loads FreeSurfer Control Points. When `Edit` is checked, \
	you can click and right-click to add and remove nodes."
  );
};
nodeSlider.onchange = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "nodeScale", this.value);
};
xRaySlider.onchange = function () {
  nv1.opts.meshXRay = this.value / 10;
  nv1.drawScene();
};
pointID.onchange = function () {
  let num = this.value;
  let nodes = nv1.meshes[0].nodes;
  let name = nodes[num].name;
  let XYZ = [nodes[num].x, nodes[num].y, nodes[num].z];
  console.log("Selected point name: " + name);
  //nb prefilled property unique to FreeSurfer: does not exist for jcon format
  // therefore, check to ensure this property exists
  if (nodes.prefilled)
    console.log("Selected point prefilled: " + nodes.prefilled[num]);
  nv1.scene.crosshairPos = nv1.mm2frac(XYZ);
  nv1.updateGLVolume();
  nv1.drawScene();
};
colorMode.onchange = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "nodeColormap", this.value);
  nv1.meshes[0].updateLabels();
  nv1.drawScene();
};
dragMode.onchange = function () {
  nv1.onDragRelease = () => {};
  switch (document.getElementById("dragMode").value) {
    case "none":
      nv1.opts.dragMode = nv1.dragModes.none;
      break;
    case "contrast":
      nv1.opts.dragMode = nv1.dragModes.contrast;
      break;
    case "measurement":
      nv1.opts.dragMode = nv1.dragModes.measurement;
      break;
    case "pan":
      nv1.opts.dragMode = nv1.dragModes.pan;
      break;
    case "slicer3D":
      nv1.opts.dragMode = nv1.dragModes.slicer3D;
      break;
    case "custom":
      nv1.opts.dragMode = nv1.dragModes.callbackOnly;
      nv1.onDragRelease = doDragRelease;
      break;
  }
};
var volumeList1 = [{ url: "../images/mni152.nii.gz", limitFrames4D: 3 }];
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
/*function doDragRelease({fracStart, fracEnd}) {
  console.log("DragRelease", fracStart, fracEnd);
}*/
function deleteNode(XYZmm) {
  console.log("delete node called");
  let nodes = nv1.meshes[0].nodes;
  if (nodes.length < 1) return;
  console.log("Deleting ", XYZmm);
  let minDx = Number.POSITIVE_INFINITY;
  let minIdx = 0;
  //check distance of each node from clicked location
  for (let i = 0; i < nodes.length; i++) {
    let dx = Math.sqrt(
      Math.pow(XYZmm[0] - nodes[i].x, 2) +
        Math.pow(XYZmm[1] - nodes[i].y, 2) +
        Math.pow(XYZmm[2] - nodes[i].z, 2)
    );
    if (dx < minDx) {
      minDx = dx;
      minIdx = i;
    }
  }
  console.log("Node " + minIdx + " is " + minDx + "mm from the click");
  const tolerance = 15.0; //e.g. only 15mm from clicked location
  if (minDx > tolerance) return;
  // nodes.names.splice(minIdx, 1);
  // nodes.prefilled.splice(minIdx, 1);
  // nodes.X.splice(minIdx, 1);
  // nodes.Y.splice(minIdx, 1);
  // nodes.Z.splice(minIdx, 1);
  // nodes.Color.splice(minIdx, 1);
  // nodes.Size.splice(minIdx, 1);
  // nodes.splice(minIdx, 1);
  nv1.meshes[0].deleteConnectomeNode(nv1.meshes[0].nodes[minIdx]);
  nv1.meshes[0].updateMesh(nv1.gl);
  nv1.updateGLVolume();
}
function addNode(XYZmm) {
  let nodes = nv1.meshes[0].nodes;
  console.log("Adding ", XYZmm);
  // nodes.names.push("");
  // nodes.prefilled.push("");
  // nodes.X.push(XYZmm[0]);
  // nodes.Y.push(XYZmm[1]);
  // nodes.Z.push(XYZmm[2]);
  // nodes.Color.push(1);
  // nodes.Size.push(1);
  nv1.meshes[0].addConnectomeNode({
    name: "node",
    x: XYZmm[0],
    y: XYZmm[1],
    z: XYZmm[2],
    colorValue: 1,
    sizeValue: 1,
  });
  nv1.meshes[0].updateMesh(nv1.gl);
  nv1.updateGLVolume();
}

function doMouseUp(uiData) {
  if (!document.getElementById("checkEdit").checked) return;
  if (uiData.fracPos[0] < 0) return; //not on volume
  if (uiData.mouseButtonCenterDown) return;
  let XYZmmVec = this.frac2mm(uiData.fracPos);
  let XYZmm = [XYZmmVec[0], XYZmmVec[1], XYZmmVec[2]];
  if (uiData.mouseButtonRightDown) deleteNode(XYZmm);
  else addNode(XYZmm);
}
checkEdit.onchange = function () {
  if (this.checked) {
    dragMode.value = "none";
    document.getElementById("dragMode").dispatchEvent(new Event("change"));
  }
};
let defaults = {
  loadingText: "there are no images",
  backColor: [1, 1, 1, 1],
  show3Dcrosshair: true,
  onLocationChange: handleLocationChange,
};
var nv1 = new niivue.Niivue(defaults);
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.opts.multiplanarForceRender = true;
nv1.graph.opacity = 1.0;
nv1.opts.meshXRay = 0.2;
nv1.setClipPlane([0.09, 180, 20]);
await nv1.loadVolumes(volumeList1);
await nv1.loadFreeSurferConnectomeFromUrl(
  "../images/FreeSurferControlPoints.json"
);
document.getElementById("pointID").dispatchEvent(new Event("change"));
document.getElementById("dragMode").dispatchEvent(new Event("change"));
nv1.onMouseUp = doMouseUp;

	
```
</td>
</tr>
</table>

# [4D mesh time series (CIFTI-2)](https://niivue.github.io/niivue/features/cifti.4D.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/61054a7b-d5b5-4e80-975e-9ecf436de3cd.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var slider = document.getElementById("meshSlider");
slider.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "frame4D", this.value);
};
var slider2 = document.getElementById("meshSlider2");
slider2.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value * 0.1);
};
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [0.9, 0.9, 1, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
var meshLHLayersList1 = [
  {
    url: "../images/Conte69.MyelinAndCorrThickness.32k_fs_LR.dtseries.nii",
    cal_min: 0.01,
    cal_max: 3.5,
    colormap: "magma",
    colormap: "rocket",
    opacity: 0.7,
  },
];
nv1.loadMeshes([
  {
    url: "../images/Conte69.L.inflated.32k_fs_LR.surf.gii",
    rgba255: [255, 255, 255, 255],
    layers: meshLHLayersList1,
  },
]);
nv1.setClipPlane([-0.1, 270, 0]);
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>

# [Tractography (TCK, TRK, TRX, VTK)](https://niivue.github.io/niivue/features/tracts.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/b6d2a037-210f-4ca6-acb2-6fe06d42f3b1.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
fiberRadius.oninput = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "fiberRadius", this.value * 0.1);
  nv1.updateGLVolume();
};
var slider = document.getElementById("fiberLengthSlider");
slider.oninput = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "fiberLength", this.value);
};
var slider2 = document.getElementById("fiberDitherSlider");
slider2.oninput = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "fiberDither", this.value * 0.1);
};
var drop = document.getElementById("fiberColor");
drop.onchange = function () {
  const colorName = document.getElementById("fiberColor").value;
  nv1.setMeshProperty(nv1.meshes[0].id, "fiberColor", colorName);
};
var dropD = document.getElementById("fiberDecimation");
dropD.onchange = function () {
  const stride = document.getElementById("fiberDecimation").value;
  nv1.setMeshProperty(nv1.meshes[0].id, "fiberDecimationStride", stride);
};
var volumeList1 = [{ url: "../images/mni152.nii.gz" }];
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [0.8, 0.8, 1, 1],
});
nv1.opts.isColorbar = true;
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
await nv1.loadVolumes(volumeList1);
await nv1.loadMeshes([
  { url: "../images/dpsv.trx", rgba255: [0, 142, 0, 255] },
]);
nv1.setMeshProperty(nv1.meshes[0].id, "colormap", "blue"); //colormap for DPV and DPS
nv1.setMeshProperty(nv1.meshes[0].id, "rgba255", [0, 255, 255, 255]); //color for fixed
nv1.setClipPlane([-0.1, 270, 0]);

	
```
</td>
</tr>
</table>

# [Tractography groups (TRX)](https://niivue.github.io/niivue/features/tracts.group.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/79f53755-d9f6-42db-a42a-ed1857b35e89.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
fiberRadius.oninput = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "fiberRadius", this.value * 0.1);
  nv1.updateGLVolume();
};
fiberDitherSlider.oninput = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "fiberDither", this.value * 0.1);
};
fiberColor.onchange = function () {
  const colorName = document.getElementById("fiberColor").value;
  if (colorName === "DPG0") {
    let cmap = {
      R: [0],
      G: [255],
      B: [0],
      I: [0],
    };
    nv1.setMeshProperty(nv1.meshes[0].id, "fiberGroupColormap", cmap);
  } else if (colorName === "DPG1") {
    let cmap = {
      R: [0],
      G: [255],
      B: [0],
      I: [1],
    };
    nv1.setMeshProperty(nv1.meshes[0].id, "fiberGroupColormap", cmap);
  } else if (colorName === "DPG01") {
    let cmap = {
      R: [0, 255],
      G: [255, 0],
      B: [0, 0],
      I: [0, 1],
    };
    nv1.setMeshProperty(nv1.meshes[0].id, "fiberGroupColormap", cmap);
  } else {
    nv1.setMeshProperty(nv1.meshes[0].id, "fiberGroupColormap", null);
    nv1.setMeshProperty(nv1.meshes[0].id, "fiberColor", colorName);
  }
};
custom.onclick = function () {
  var val = document.getElementById("scriptText").value;
  val += '; nv1.setMeshProperty(nv1.meshes[0].id, "fiberGroupColormap", cmap);';
  val && eval(val);
};
fiberDecimation.onchange = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "fiberDecimationStride", this.value);
};
var volumeList1 = [{ url: "../images/sub-01_ses-01_dwi_desc-b0_dwi.nii.gz" }];
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [0.7, 0.7, 0.7, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
await nv1.loadVolumes(volumeList1);
await nv1.loadMeshes([
  {
    url: "../images/sub-01_ses-01_dwi_space-RASMM_model-probCSD_algo-AFQ_tractography.trx",
    rgba255: [0, 142, 0, 255],
  },
]);
nv1.setClipPlane([-0.1, 180, 0]);

	
```
</td>
</tr>
</table>

# [Advanced tractography (TCK, TRK, TRX, VTK)](https://niivue.github.io/niivue/features/tracts2.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/23c6eee4-3066-4a57-b8d1-f2eca3539eee.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

zoomSlider.onchange = function () {
  nv1.scene.volScaleMultiplier = zoomSlider.value * 0.1;
  nv1.drawScene();
};
xRaySlider.onchange = function () {
  nv1.opts.meshXRay = this.value * 0.01;
  nv1.drawScene();
};
shaderDrop.onchange = function () {
  const shaderName = this.value;
  nv1.setMeshShader(nv1.meshes[3].id, shaderName);
};
colorDrop.onchange = function () {
  const colorName = this.value;
  nv1.setMeshProperty(nv1.meshes[0].id, "fiberColor", colorName);
  nv1.setMeshProperty(nv1.meshes[1].id, "fiberColor", colorName);
  nv1.setMeshProperty(nv1.meshes[2].id, "fiberColor", colorName);
};
var volumeList1 = [{ url: "../images/mni152.nii.gz" }];
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [0, 0, 0, 1],
});
nv1.opts.isOrientCube = true;
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
await nv1.loadVolumes(volumeList1);
await nv1.loadMeshes([
  { url: "../images/tract.FAT_R.vtk", rgba255: [180, 180, 0, 255] },
  { url: "../images/tract.IFOF_R.trk", rgba255: [0, 255, 0, 255] },
  { url: "../images/tract.SLF1_R.tck", rgba255: [0, 0, 255, 255] },
  {
    url: "../images/BrainMesh_ICBM152.lh.mz3",
    rgba255: [242, 174, 177, 255],
    opacity: 0.2,
  },
]);
nv1.setClipPlane([-0.1, 0, 90]);
nv1.setRenderAzimuthElevation(135, 15);
document.getElementById("colorDrop").dispatchEvent(new Event("change"));
document.getElementById("xRaySlider").dispatchEvent(new Event("change"));
document.getElementById("shaderDrop").dispatchEvent(new Event("change"));

	
```
</td>
</tr>
</table>

# [4D Time series data (fMRI, DTI, ASL, etc) using thumbnail for rapid loading](https://niivue.github.io/niivue/features/timeseries.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/1590e168-69d4-4c31-aff9-0572c6a82d84.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var volumeList1 = [
  // first item is background image
  {
    url: "../images/pcasl.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
    frame4D: 2,
  },
];
var nv1 = new niivue.Niivue({
  onLocationChange: handleLocationChange,
  thumbnail: "../images/pcasl.png",
});
nv1.attachTo("gl1");
nv1.setRadiologicalConvention(false);
nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.graph.autoSizeMultiplanar = true;
nv1.opts.multiplanarForceRender = true;
nv1.graph.normalizeValues = false;
nv1.graph.opacity = 1.0;
check1.onchange = function () {
  nv1.graph.normalizeValues = this.checked;
  nv1.updateGLVolume();
};
let currentVol = 0;
prevVolume.onclick = function () {
  currentVol = Math.max(currentVol - 1, 0);
  nv1.setFrame4D(nv1.volumes[0].id, currentVol);
};
nextVolume.onclick = function () {
  currentVol++;
  currentVol = Math.min(currentVol, nv1.getFrame4D(nv1.volumes[0].id) - 1);
  nv1.setFrame4D(nv1.volumes[0].id, currentVol);
};
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
var animationTimer = null;
function doAnimate() {
  currentVol++;
  if (currentVol >= nv1.getFrame4D(nv1.volumes[0].id)) currentVol = 0;
  nv1.setFrame4D(nv1.volumes[0].id, currentVol);
}
animate.onclick = function () {
  if (animationTimer == null) animationTimer = setInterval(doAnimate, 100);
  else {
    clearInterval(animationTimer);
    animationTimer = null;
  }
};
document.getElementById("gl1").addEventListener("dblclick", toggleThumbnail);
function toggleThumbnail() {
  nv1.thumbnailVisible = !nv1.thumbnailVisible;
  nv1.drawScene();
}
thumbnail.onclick = function () {
  toggleThumbnail();
};

	
```
</td>
</tr>
</table>



# [4D Time series data (fMRI, DTI, ASL, etc) initially showing only the first volumes for rapid loading](https://niivue.github.io/niivue/features/timeseries2.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/b18f204c-cdb5-4d18-b5ff-130123fa5451.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var volumeList1 = [
  {
    url: "../images/pcasl.nii.gz",
    limitFrames4D: 5,
  },
];
var nv1 = new niivue.Niivue({
  onLocationChange: handleLocationChange,
});
nv1.attachTo("gl1");
nv1.setRadiologicalConvention(false);
nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.graph.autoSizeMultiplanar = true;
nv1.opts.multiplanarForceRender = true;
nv1.graph.normalizeValues = false;
nv1.graph.opacity = 1.0;
check1.onchange = function () {
  nv1.graph.normalizeValues = this.checked;
  nv1.updateGLVolume();
};
let currentVol = 0;
prevVolume.onclick = function () {
  currentVol = Math.max(currentVol - 1, 0);
  nv1.setFrame4D(nv1.volumes[0].id, currentVol);
};
nextVolume.onclick = function () {
  currentVol++;
  currentVol = Math.min(currentVol, nv1.getFrame4D(nv1.volumes[0].id) - 1);
  nv1.setFrame4D(nv1.volumes[0].id, currentVol);
};
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
var animationTimer = null;
function doAnimate() {
  currentVol++;
  if (currentVol >= nv1.getFrame4D(nv1.volumes[0].id)) currentVol = 0;
  nv1.setFrame4D(nv1.volumes[0].id, currentVol);
}
animate.onclick = function () {
  if (animationTimer == null) animationTimer = setInterval(doAnimate, 100);
  else {
    clearInterval(animationTimer);
    animationTimer = null;
  }
};
about.onclick = function () {
  alert(
    "4D images can be slow to load. Click the `...` \
	icon below the graph to see the entire dataset. \
	Currently displaying " +
      nv1.volumes[0].nFrame4D +
      " of " +
      nv1.volumes[0].nTotalFrame4D +
      " frames."
  );
};

	
```

</td>
</tr>
</table>

# [AFNI volumes](https://niivue.github.io/niivue/features/afni.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/d4e6d1d0-10f6-46c2-9e9e-0b1014202135.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var volumeList1 = [
  // for AFNI head/brik files we need to explicitly specify BOTH
  {
    url: "../images/example4d+orig.HEAD", //"./images/RAS.nii.gz", "./images/spm152.nii.gz",
    urlImgData: "../images/example4d+orig.BRIK.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
];
var nv1 = new niivue.Niivue({
  onFrameChange: updateFrameValue,
});
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.graph.autoSizeMultiplanar = true;
nv1.opts.multiplanarForceRender = true;
nv1.graph.normalizeValues = false;
nv1.graph.opacity = 1.0;
check1.onchange = function () {
  nv1.graph.normalizeValues = this.checked;
  nv1.updateGLVolume();
};
let currentVol = 0;
prevVolume.onclick = function () {
  currentVol = Math.max(currentVol - 1, 0);
  nv1.setFrame4D(nv1.volumes[0].id, currentVol);
  document.getElementById("volume").innerHTML = "volume " + currentVol;
};
function updateFrameValue(volume, index) {
  document.getElementById("volume").innerHTML = "volume " + index;
  currentVol = index;
}
nextVolume.onclick = function () {
  currentVol++;
  currentVol = Math.min(currentVol, nv1.getFrame4D(nv1.volumes[0].id) - 1);
  nv1.setFrame4D(nv1.volumes[0].id, currentVol);
  document.getElementById("volume").innerHTML = "volume " + currentVol;
};
var animationTimer = null;
function doAnimate() {
  currentVol++;
  if (currentVol >= nv1.getFrame4D(nv1.volumes[0].id)) currentVol = 0;
  nv1.setFrame4D(nv1.volumes[0].id, currentVol);
}
animate.onclick = function () {
  if (animationTimer == null) animationTimer = setInterval(doAnimate, 100);
  else {
    clearInterval(animationTimer);
    animationTimer = null;
  }
};

	
```
</td>
</tr>
</table>

# [BrainVoyager meshes](https://niivue.github.io/niivue/features/brainvoyager.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/ad4be17e-46c8-413d-927f-9e1ac111831f.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var slider = document.getElementById("meshSlider");
slider.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "frame4D", this.value);
};
var slider2 = document.getElementById("meshSlider2");
slider2.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value * 0.1);
};
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [0, 0, 0, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
var meshLHLayersList1 = [
  //{url: "../images/sub-test02_left_hemisphere_4_curvature_maps.smp", cal_min: 0.0, cal_max: 1.0, useNegativeCmap: true, opacity: 0.7},
  {
    url: "../images/sub-test02_left_hemisphere_4_curvature_maps.smp.gz",
    colormap: "rocket",
    cal_min: 0.0,
    cal_max: 0.5,
    opacity: 0.7,
  },
];
nv1.loadMeshes([
  {
    url: "../images/sub-test02_left_hemisphere.srf.gz",
    rgba255: [255, 255, 255, 255],
    layers: meshLHLayersList1,
  },
]);
nv1.setClipPlane([-0.1, 270, 0]);
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>

# [x3d meshes](https://niivue.github.io/niivue/features/x3d.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/16a5cfee-0422-47e7-b53d-63c515f8b8b3.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

document.getElementById("check10").addEventListener("change", doCheck10Click);
function doCheck10Click() {
  nv1.setHighResolutionCapable(this.checked);
}
document.getElementById("check11").addEventListener("change", doCheck11Click);
function doCheck11Click() {
  nv1.opts.meshXRay = Number(this.checked) * 0.02;
  nv1.drawScene();
}
var nv1 = new niivue.Niivue({
  backColor: [0.9, 0.9, 0.9, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
nv1.loadMeshes([
  {
    url: "../images/MolView-sticks-color_38.x3d",
    rgba255: [222, 164, 164, 255],
  },
]);
nv1.setClipPlane([-0.1, 270, 0]);
document.getElementById("check10").checked = nv1.opts.isHighResolutionCapable;
document.getElementById("check11").checked = nv1.opts.isMeshXRay;
let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>

# [Clip planes](https://niivue.github.io/niivue/features/clipplanes.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/abe6dff2-ab8d-4667-927d-2f0f207ff75d.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
var volumeList1 = [
  {
    url: "../images/mni152.nii.gz", //"./RAS.nii.gz", "./spm152.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
];
var nv1 = new niivue.Niivue({
  show3Dcrosshair: false,
  backColor: [1, 1, 1, 1],
});
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeRender);
nv1.setClipPlane([0, 180, 40]);
nv1.setRenderAzimuthElevation(260, 20);
nv1.loadMeshes([
  {
    url: "../images/BrainMesh_ICBM152.lh.mz3",
    rgba255: [222, 164, 164, 255],
  },
  { url: "../images/connectome.jcon" },
]);
var check = document.getElementById("check1");
check.onclick = function () {
  let clr = nv1.opts.clipPlaneColor;
  console.log(clr);
  clr[3] = Math.abs(clr[3]);
  if (this.checked) clr[3] = -clr[3];
  nv1.setClipPlaneColor(clr);
};
var slider = document.getElementById("alphaSlider");
slider.oninput = function () {
  let clr = nv1.opts.clipPlaneColor;
  let rev = clr[3] < 0;
  clr[3] = this.value / 255;
  if (rev) clr[3] = -clr[3];
  nv1.setClipPlaneColor(clr);
};
var cslider = document.getElementById("colorSlider");
cslider.oninput = function () {
  let clr = nv1.opts.clipPlaneColor;
  clr[1] = this.value / 255;
  nv1.setClipPlaneColor(clr);
};
var xslider = document.getElementById("xRaySlider");
xslider.oninput = function () {
  nv1.opts.meshXRay = this.value * 0.01;
  nv1.drawScene();
};

	
```
</td>
</tr>
</table>

# [Drawing](https://niivue.github.io/niivue/features/draw2.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/a0b13e8c-3183-406d-9954-b587392585a5.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

document
  .getElementById("drawOpacity")
  .addEventListener("change", doDrawOpacity);
function doDrawOpacity() {
  nv1.setDrawOpacity(this.value * 0.01);
}
document.getElementById("drawPen").addEventListener("change", doDrawPen);
function doDrawPen() {
  const mode = parseInt(document.getElementById("drawPen").value);
  nv1.setDrawingEnabled(mode >= 0);
  if (mode >= 0) nv1.setPenValue(mode & 7, mode > 7);
  if (mode === 12)
    //erase selected cluster
    nv1.setPenValue(-0);
}
document.getElementById("left").addEventListener("click", doLeft);
function doLeft() {
  nv1.moveCrosshairInVox(-1, 0, 0);
}
document.getElementById("right").addEventListener("click", doRight);
function doRight() {
  nv1.moveCrosshairInVox(1, 0, 0);
}
document.getElementById("posterior").addEventListener("click", doPosterior);
function doPosterior() {
  nv1.moveCrosshairInVox(0, -1, 0);
}
document.getElementById("anterior").addEventListener("click", doAnterior);
function doAnterior() {
  nv1.moveCrosshairInVox(0, 1, 0);
}
document.getElementById("inferior").addEventListener("click", doInferior);
function doInferior() {
  nv1.moveCrosshairInVox(0, 0, -1);
}
document.getElementById("info").addEventListener("click", doInfo);
function doInfo() {
  let obj = nv1.getDescriptives(0, [], true);
  let str = JSON.stringify(obj, null, 2);
  alert(str);
}
document.getElementById("superior").addEventListener("click", doSuperior);
function doSuperior() {
  nv1.moveCrosshairInVox(0, 0, 1);
}
document.getElementById("undo").addEventListener("click", doUndo);
function doUndo() {
  nv1.drawUndo();
}
document.getElementById("growcut").addEventListener("click", doGrowCut);
function doGrowCut() {
  nv1.drawGrowCut();
}
document.getElementById("save").addEventListener("click", doSave);
function doSave() {
  nv1.saveImage({ filename: "test.nii", isSaveDrawing: true });
}
document.getElementById("check1").addEventListener("change", doCheckClick);
function doCheckClick() {
  nv1.drawFillOverwrites = this.checked;
}
document.getElementById("check2").addEventListener("change", doCheck2Click);
function doCheck2Click() {
  nv1.setRadiologicalConvention(this.checked);
}
document.getElementById("check3").addEventListener("change", doCheck3Click);
function doCheck3Click() {
  nv1.setSliceMM(this.checked);
}
document.getElementById("check9").addEventListener("change", doCheck9Click);
function doCheck9Click() {
  nv1.setInterpolation(!this.checked);
}
document.getElementById("check10").addEventListener("change", doCheck10Click);
function doCheck10Click() {
  nv1.setHighResolutionCapable(this.checked);
}
var btn = document.getElementById("custom");
btn.onclick = function (event) {
  var val = document.getElementById("scriptText").value;
  val += ";nv1.setDrawColormap(cmap);";
  val && eval(val);
};
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
var volumeList1 = [{ url: "../images/FLAIR.nii.gz" }];
var nv1 = new niivue.Niivue({
  backColor: [1, 1, 1, 1],
  onLocationChange: handleLocationChange,
});
nv1.setRadiologicalConvention(false);
nv1.opts.multiplanarForceRender = true;
nv1.attachTo("gl1");
await nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
await nv1.loadDrawingFromUrl("../images/lesion.nii.gz");

	
```
</td>
</tr>
</table>

# [Drawing user interface](https://niivue.github.io/niivue/features/draw.ui.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/2e493aa9-af11-48ea-9eb3-2c32d4938632.png)


</td>
<td>

	
```javascript
import * as niivue from "../dist/index.js";

const isTouchDevice =
  "ontouchstart" in window ||
  navigator.maxTouchPoints > 0 ||
  navigator.msMaxTouchPoints > 0;
var isFilled = true;
function handleIntensityChange(data) {
  document.getElementById("intensity").innerHTML = "&nbsp;&nbsp;" + data.string;
}
var nv1 = new niivue.Niivue({
  logging: true,
  dragAndDropEnabled: true,
  backColor: [0, 0, 0, 1],
  show3Dcrosshair: true,
  onLocationChange: handleIntensityChange,
});
nv1.opts.isColorbar = false;
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
nv1.setClipPlane([0.3, 270, 0]);
nv1.setRenderAzimuthElevation(120, 10);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.setSliceMM(true);
nv1.opts.multiplanarForceRender = false;
nv1.graph.autoSizeMultiplanar = true;
nv1.graph.opacity = 1.0;
nv1.drawOpacity = 0.5;
nv1.opts.isColorbar = false;
var volumeList1 = [{ url: "../images/FLAIR.nii.gz" }];
await nv1.loadVolumes(volumeList1);
await nv1.loadDrawingFromUrl("../images/lesion.nii.gz");
function toggleGroup(id) {
  let buttons = document.getElementsByClassName("viewBtn");
  let char0 = id.charAt(0);
  for (let i = 0; i < buttons.length; i++) {
    if (buttons[i].id.charAt(0) !== char0) continue;
    buttons[i].classList.remove("dropdown-item-checked");
    if (buttons[i].id === id) buttons[i].classList.add("dropdown-item-checked");
  }
} // toggleGroup()
async function onButtonClick(event) {
  if (isTouchDevice) {
    console.log("Touch device: click menu to close menu");
    /*var el = this.parentNode
      el.style.display = "none"
      setTimeout(function() { //close menu
        //el.style.removeProperty("display")
        //el.style.display = "block"
      }, 500)*/
  }
  if (event.target.id === "SaveDraw") {
    nv1.saveImage({ filename: "draw.nii", isSaveDrawing: true });
    return;
  }
  if (event.target.id === "CloseDraw") {
    nv1.closeDrawing();
    return;
  }
  if (event.target.id === "SaveBitmap") {
    nv1.saveScene("ScreenShot.png");
    return;
  }
  if (event.target.id === "ShowHeader") {
    alert(nv1.volumes[0].hdr.toFormattedString());
    return;
  }
  if (event.target.id === "Colorbar") {
    nv1.opts.isColorbar = !nv1.opts.isColorbar;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
    return;
  }
  if (event.target.id === "Radiological") {
    nv1.opts.isRadiologicalConvention = !nv1.opts.isRadiologicalConvention;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
    return;
  }
  if (event.target.id === "Crosshair") {
    nv1.opts.show3Dcrosshair = !nv1.opts.show3Dcrosshair;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
  }
  if (event.target.id === "ClipPlane") {
    if (nv1.scene.clipPlaneDepthAziElev[0] > 1) nv1.setClipPlane([0.3, 270, 0]);
    else nv1.setClipPlane([2, 270, 0]);
    nv1.drawScene();
    return;
  }
  if (event.target.id.charAt(0) === "!") {
    // set color scheme
    nv1.volumes[0].colormap = event.target.id.substr(1);
    nv1.updateGLVolume();
    toggleGroup(event.target.id);
    return;
  }
  if (event.target.id.charAt(0) === "{") {
    // change color labels https://github.com/niivue/niivue/issues/575
    if (event.target.id === "{$Custom") {
      let cmap = {
        R: [0, 255, 22, 127],
        G: [0, 20, 192, 187],
        B: [0, 152, 80, 255],
        A: [0, 255, 255, 255],
        labels: ["", "pink", "lime", "sky"],
      };
      nv1.setDrawColormap(cmap);
    } else nv1.setDrawColormap(event.target.id.substr(1));
    toggleGroup(event.target.id);
    return;
  }
  if (event.target.id === "Undo") {
    nv1.drawUndo();
  }
  if (event.target.id.charAt(0) === "@") {
    //sliceType
    if (event.target.id === "@Off") nv1.setDrawingEnabled(false);
    else nv1.setDrawingEnabled(true);
    if (event.target.id === "@Erase") nv1.setPenValue(0, isFilled);
    if (event.target.id === "@Red") nv1.setPenValue(1, isFilled);
    if (event.target.id === "@Green") nv1.setPenValue(2, isFilled);
    if (event.target.id === "@Blue") nv1.setPenValue(3, isFilled);
    if (event.target.id === "@Yellow") nv1.setPenValue(4, isFilled);
    if (event.target.id === "@Cyan") nv1.setPenValue(5, isFilled);
    if (event.target.id === "@Purple") nv1.setPenValue(6, isFilled);
    if (event.target.id === "@Cluster") nv1.setPenValue(-0, isFilled);
    if (event.target.id === "@GrowCluster") nv1.setPenValue(NaN, isFilled);
    if (event.target.id === "@GrowClusterBright")
      nv1.setPenValue(Number.POSITIVE_INFINITY, isFilled);
    if (event.target.id === "@GrowClusterDark")
      nv1.setPenValue(Number.NEGATIVE_INFINITY, isFilled);
    toggleGroup(event.target.id);
  } //Draw Color
  if (event.target.id === "Growcut") nv1.drawGrowCut();
  if (event.target.id === "Translucent") {
    if (nv1.drawOpacity > 0.75) nv1.drawOpacity = 0.5;
    else nv1.drawOpacity = 1.0;
    nv1.drawScene();
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "DrawOtsu") {
    let levels = parseInt(prompt("Segmentation classes (2..4)", "3"));
    nv1.drawOtsu(levels);
  }
  if (event.target.id === "RemoveHaze") {
    let level = parseInt(prompt("Remove Haze (1..5)", "5"));
    nv1.removeHaze(level);
  }
  if (event.target.id === "DrawFilled") {
    isFilled = !isFilled;
    nv1.setPenValue(nv1.opts.penValue, isFilled);
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "DrawOverwrite") {
    nv1.drawFillOverwrites = !nv1.drawFillOverwrites;
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id.charAt(0) === "|") {
    //sliceType
    if (event.target.id === "|Axial") nv1.setSliceType(nv1.sliceTypeAxial);
    if (event.target.id === "|Coronal") nv1.setSliceType(nv1.sliceTypeCoronal);
    if (event.target.id === "|Sagittal")
      nv1.setSliceType(nv1.sliceTypeSagittal);
    if (event.target.id === "|Render") nv1.setSliceType(nv1.sliceTypeRender);
    if (event.target.id === "|MultiPlanar") {
      nv1.opts.multiplanarForceRender = false;
      nv1.setSliceType(nv1.sliceTypeMultiplanar);
    }
    if (event.target.id === "|MultiPlanarRender") {
      nv1.opts.multiplanarForceRender = true;
      nv1.setSliceType(nv1.sliceTypeMultiplanar);
    }
    toggleGroup(event.target.id);
  } //sliceType
  if (event.target.id === "WorldSpace") {
    nv1.setSliceMM(!nv1.opts.isSliceMM);
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "Interpolate") {
    nv1.setInterpolation(!nv1.opts.isNearestInterpolation);
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "Left") nv1.moveCrosshairInVox(-1, 0, 0);
  if (event.target.id === "Right") nv1.moveCrosshairInVox(1, 0, 0);
  if (event.target.id === "Posterior") nv1.moveCrosshairInVox(0, -1, 0);
  if (event.target.id === "Anterior") nv1.moveCrosshairInVox(0, 1, 0);
  if (event.target.id === "Inferior") nv1.moveCrosshairInVox(0, 0, -1);
  if (event.target.id === "Superior") nv1.moveCrosshairInVox(0, 0, 1);
  if (event.target.id === "BackColor") {
    if (nv1.opts.backColor[0] < 0.5) nv1.opts.backColor = [1, 1, 1, 1];
    else nv1.opts.backColor = [0, 0, 0, 1];
    nv1.drawScene();
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id.charAt(0) === "^") {
    //drag mode
    let s = event.target.id.substr(1);
    switch (s) {
      case "none":
        nv1.opts.dragMode = nv1.dragModes.none;
        break;
      case "contrast":
        nv1.opts.dragMode = nv1.dragModes.contrast;
        break;
      case "measurement":
        nv1.opts.dragMode = nv1.dragModes.measurement;
        break;
      case "pan":
        nv1.opts.dragMode = nv1.dragModes.pan;
        break;
    }
    toggleGroup(event.target.id);
  } //drag mode
  if (event.target.id === "_mesh") {
    volumeList1[0].url = "../images/mni152.nii.gz";
    await nv1.loadVolumes(volumeList1);
    nv1.loadMeshes([
      {
        url: "../images/BrainMesh_ICBM152.lh.mz3",
        rgba255: [200, 162, 255, 255],
      },
      { url: "../images/dpsv.trx", rgba255: [255, 255, 255, 255] },
    ]);
    toggleGroup(event.target.id);
  } else if (event.target.id.charAt(0) === "_") {
    //example image
    nv1.meshes = []; //close open meshes
    let root = "../images/";
    let s = event.target.id.substr(1);
    let img = root + s + ".nii.gz";
    console.log("Loading " + img);
    volumeList1[0].url = img;
    nv1.loadVolumes(volumeList1);
    toggleGroup(event.target.id);
    nv1.updateGLVolume();
  } //example image
} // onButtonClick()
var buttons = document.getElementsByClassName("viewBtn");
for (let i = 0; i < buttons.length; i++)
  buttons[i].addEventListener("click", onButtonClick, false);

	
```
</td>
</tr>
</table>

# [Torso regions](https://niivue.github.io/niivue/features/torso.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/f7bd9505-94de-46ae-b6ed-2fd301b6fe6c.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var slider = document.getElementById("alphaSlider");
slider.oninput = function () {
  nv1.setDrawOpacity(this.value / 255);
};
var slider2 = document.getElementById("ambientSlider");
slider2.oninput = function () {
  nv1.setRenderDrawAmbientOcclusion(this.value / 255);
};
var check1 = document.getElementById("check1");
check1.onclick = function (event) {
  nv1.volumes[0].opacity = this.checked;
  nv1.updateGLVolume();
};
var check2 = document.getElementById("check2");
check2.onclick = function (event) {
  nv1.isAlphaClipDark = this.checked;
  nv1.updateGLVolume();
};
var check3 = document.getElementById("check3");
check3.onclick = function (event) {
  nv1.setInterpolation(!this.checked);
};
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
let defaults = {
  logging: true,
  dragAndDropEnabled: true,
  backColor: [0.3, 0.3, 0.3, 1],
  show3Dcrosshair: true,
  onLocationChange: handleLocationChange,
};
var nv1 = new niivue.Niivue(defaults);
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
var volumeList1 = [
  {
    url: "../images/torso.nii.gz",
    cal_min: 0,
    cal_max: 200,
    opacity: 1.0,
  },
];
await nv1.loadVolumes(volumeList1);
nv1.opts.multiplanarForceRender = true;
nv1.graph.autoSizeMultiplanar = true;
nv1.setClipPlane([-0.1, 270, 0]);
let cmap = {
  R: [0, 0, 185, 185, 252, 0, 103, 216, 127, 127, 0, 222],
  G: [0, 20, 102, 102, 0, 255, 76, 132, 0, 127, 255, 154],
  B: [0, 152, 83, 83, 0, 0, 71, 105, 127, 0, 255, 132],
  A: [0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
  labels: [
    "background",
    "1spleen",
    "2kidneyR",
    "3kidneyL",
    "4gallbladder",
    "5esophagus",
    "6Liver",
    "7stomach",
    "8aorta",
    "9inferiorvenacava",
    "10pancreas",
    "11bladder",
  ],
};
nv1.setDrawColormap(cmap);
nv1.setRadiologicalConvention(true);

await nv1.loadDrawingFromUrl("../images/torsoLabel.nii.gz");
	
```
</td>
</tr>
</table>

# [Carotid Artery-Computed Tomographic Angiography Scoring](https://niivue.github.io/niivue/features/cactus.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/d1adfde6-086f-485c-947e-421b2543a6ea.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
var isFilled = true;
var isCustomDraw = true;
var lastPos = null;
document.getElementById("gl1").ondblclick = async function () {
  if (!isCustomDraw) return;
  if (!lastPos) return;
  if (!lastPos.values) return;
  if (!nv1.drawBitmap) nv1.createEmptyDrawing();
  if (!isFinite(lastPos.axCorSag)) return;
  if (lastPos.axCorSag < 0 || lastPos.axCorSag > 2) return;
  let penValue = 2; //green
  let threshold_tolerance = 450;
  let intensity = lastPos.values[0].value;
  let mn = intensity - threshold_tolerance;
  let mx = intensity + threshold_tolerance;
  let min_threshold_tolerance = 300;
  if (mn < min_threshold_tolerance) {
    console.log("Hounsfield Intensity too dark to be plaque");
    if (mx < min_threshold_tolerance) return;
    mn = Math.max(mn, min_threshold_tolerance);
  }
  nv1.drawPt(...lastPos.vox, penValue);
  await nv1.drawFloodFill(lastPos.vox, 0, 1, mn, mx);
  nv1.refreshDrawing(true);
};
function handleIntensityChange(data) {
  document.getElementById("intensity").innerHTML = "&nbsp;&nbsp;" + data.string;
  lastPos = data;
}
var nv1 = new niivue.Niivue({
  logging: true,
  dragAndDropEnabled: true,
  backColor: [0, 0, 0, 1],
  show3Dcrosshair: true,
  onLocationChange: handleIntensityChange,
});
nv1.opts.isColorbar = false;
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
nv1.setRenderAzimuthElevation(120, 10);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.setSliceMM(true);
nv1.opts.multiplanarForceRender = false;
nv1.graph.autoSizeMultiplanar = true;
nv1.graph.opacity = 1.0;
nv1.drawOpacity = 0.5;
nv1.opts.isColorbar = false;
nv1.opts.multiplanarForceRender = true;
var volumeList1 = [{ url: "../images/cactus.nii.gz" }];
await nv1.loadVolumes(volumeList1);
//image specific settings
nv1.volumes[0].colormap = "ct_kidneys";
nv1.volumes[0].cal_min = 80;
nv1.volumes[0].cal_max = 480;
nv1.opts.dragMode = nv1.dragModes.slicer3D;
nv1.setRenderAzimuthElevation(220, -20);
nv1.scene.crosshairPos = [0.68, 0.275, 0.086];
nv1.updateGLVolume();
//handle menus
function toggleGroup(id) {
  let buttons = document.getElementsByClassName("viewBtn");
  let char0 = id.charAt(0);
  for (let i = 0; i < buttons.length; i++) {
    if (buttons[i].id.charAt(0) !== char0) continue;
    buttons[i].classList.remove("dropdown-item-checked");
    if (buttons[i].id === id) buttons[i].classList.add("dropdown-item-checked");
  }
} // toggleGroup()
async function onButtonClick(event) {
  if (event.target.id === "SaveDraw") {
    nv1.saveImage({ filename: "draw.nii", isSaveDrawing: true });
    return;
  }
  if (event.target.id === "SaveBitmap") {
    nv1.saveScene("ScreenShot.png");
    return;
  }
  if (event.target.id === "ShowHeader") {
    alert(nv1.volumes[0].hdr.toFormattedString());
    return;
  }
  if (event.target.id === "Colorbar") {
    nv1.opts.isColorbar = !nv1.opts.isColorbar;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
    return;
  }
  if (event.target.id === "Radiological") {
    nv1.opts.isRadiologicalConvention = !nv1.opts.isRadiologicalConvention;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
    return;
  }
  if (event.target.id === "Crosshair") {
    nv1.opts.show3Dcrosshair = !nv1.opts.show3Dcrosshair;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
  }
  if (event.target.id === "ClipPlane") {
    if (nv1.scene.clipPlaneDepthAziElev[0] > 1) nv1.setClipPlane([0.3, 270, 0]);
    else nv1.setClipPlane([2, 270, 0]);
    nv1.drawScene();
    return;
  }
  if (event.target.id.charAt(0) === "!") {
    // set color scheme
    nv1.volumes[0].colormap = event.target.id.substr(1);
    nv1.updateGLVolume();
    toggleGroup(event.target.id);
    return;
  }
  if (event.target.id === "Undo") {
    nv1.drawUndo();
  }
  if (event.target.id.charAt(0) === "@") {
    //sliceType
    isCustomDraw = false;
    if (event.target.id === "@Off") nv1.setDrawingEnabled(false);
    else nv1.setDrawingEnabled(true);
    if (event.target.id === "@Erase") nv1.setPenValue(0, isFilled);
    if (event.target.id === "@Red") nv1.setPenValue(1, isFilled);
    if (event.target.id === "@Green") nv1.setPenValue(2, isFilled);
    if (event.target.id === "@Blue") nv1.setPenValue(3, isFilled);
    if (event.target.id === "@Yellow") nv1.setPenValue(4, isFilled);
    if (event.target.id === "@Cyan") nv1.setPenValue(5, isFilled);
    if (event.target.id === "@Purple") nv1.setPenValue(6, isFilled);
    if (event.target.id === "@Cluster") nv1.setPenValue(-0, isFilled);
    if (event.target.id === "@SelectCluster") {
      //custom
      nv1.setDrawingEnabled(false);
      isCustomDraw = true;
    }
    toggleGroup(event.target.id);
  } //Draw Color
  if (event.target.id === "Growcut") nv1.drawGrowCut();
  if (event.target.id === "Translucent") {
    if (nv1.drawOpacity > 0.75) nv1.drawOpacity = 0.5;
    else nv1.drawOpacity = 1.0;
    nv1.drawScene();
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "DrawOtsu") {
    let levels = parseInt(prompt("Segmentation classes (2..4)", "3"));
    nv1.drawOtsu(levels);
  }
  if (event.target.id === "RemoveHaze") {
    let level = parseInt(prompt("Remove Haze (1..5)", "5"));
    nv1.removeHaze(level);
  }
  if (event.target.id === "DrawFilled") {
    isFilled = !isFilled;
    nv1.setPenValue(nv1.opts.penValue, isFilled);
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "DrawOverwrite") {
    nv1.drawFillOverwrites = !nv1.drawFillOverwrites;
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id.charAt(0) === "|") {
    //sliceType
    if (event.target.id === "|Axial") nv1.setSliceType(nv1.sliceTypeAxial);
    if (event.target.id === "|Coronal") nv1.setSliceType(nv1.sliceTypeCoronal);
    if (event.target.id === "|Sagittal")
      nv1.setSliceType(nv1.sliceTypeSagittal);
    if (event.target.id === "|Render") nv1.setSliceType(nv1.sliceTypeRender);
    if (event.target.id === "|MultiPlanar") {
      nv1.opts.multiplanarForceRender = false;
      nv1.setSliceType(nv1.sliceTypeMultiplanar);
    }
    if (event.target.id === "|MultiPlanarRender") {
      nv1.opts.multiplanarForceRender = true;
      nv1.setSliceType(nv1.sliceTypeMultiplanar);
    }
    toggleGroup(event.target.id);
  } //sliceType
  if (event.target.id === "WorldSpace") {
    nv1.setSliceMM(!nv1.opts.isSliceMM);
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "Interpolate") {
    nv1.setInterpolation(!nv1.opts.isNearestInterpolation);
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "Left") nv1.moveCrosshairInVox(-1, 0, 0);
  if (event.target.id === "Right") nv1.moveCrosshairInVox(1, 0, 0);
  if (event.target.id === "Posterior") nv1.moveCrosshairInVox(0, -1, 0);
  if (event.target.id === "Anterior") nv1.moveCrosshairInVox(0, 1, 0);
  if (event.target.id === "Inferior") nv1.moveCrosshairInVox(0, 0, -1);
  if (event.target.id === "Superior") nv1.moveCrosshairInVox(0, 0, 1);
  if (event.target.id === "BackColor") {
    if (nv1.opts.backColor[0] < 0.5) nv1.opts.backColor = [1, 1, 1, 1];
    else nv1.opts.backColor = [0, 0, 0, 1];
    nv1.drawScene();
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id.charAt(0) === "^") {
    //drag mode
    let s = event.target.id.substr(1);
    switch (s) {
      case "none":
        nv1.opts.dragMode = nv1.dragModes.none;
        break;
      case "contrast":
        nv1.opts.dragMode = nv1.dragModes.contrast;
        break;
      case "measurement":
        nv1.opts.dragMode = nv1.dragModes.measurement;
        break;
      case "pan":
        nv1.opts.dragMode = nv1.dragModes.pan;
        break;
      case "slicer":
        nv1.opts.dragMode = nv1.dragModes.slicer3D;
        break;
    }
    toggleGroup(event.target.id);
  } //drag mode
} // onButtonClick()
var buttons = document.getElementsByClassName("viewBtn");
for (let i = 0; i < buttons.length; i++)
  buttons[i].addEventListener("click", onButtonClick, false);

	
```
</td>
</tr>
</table>

# [Voxel atlas](https://niivue.github.io/niivue/features/atlas.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/6830c047-b389-462c-917d-16eefc898803.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
var volumeList1 = [
  { url: "../images/mni152.nii.gz" },
  { url: "../images/aal.nii.gz" },
];
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = data.string;
}
var nv1 = new niivue.Niivue({
  backColor: [0.5, 0.5, 0.5, 1],
  onLocationChange: handleLocationChange,
});
nv1.attachTo("gl1");
await nv1.loadVolumes(volumeList1);
async function fetchJSON(fnm) {
  const response = await fetch(fnm);
  const js = await response.json();
  return js;
}
let cmap = await fetchJSON("../images/aal.json");
nv1.volumes[1].setColormapLabel(cmap);
nv1.updateGLVolume();
nv1.setMultiplanarPadPixels(5);
document.getElementById("check1").addEventListener("change", doCheckClick);
function doCheckClick() {
  nv1.setAtlasOutline(this.checked);
}
check2.onchange = function () {
  if (this.checked) nv1.opts.backColor = [0.5, 0.5, 0.5, 1];
  else nv1.opts.backColor = [1, 1, 1, 1];
  nv1.drawScene();
};
alphaSlider.oninput = function () {
  nv1.setOpacity(1, this.value / 255);
};
padSlider.oninput = function () {
  nv1.setMultiplanarPadPixels(this.value);
};

	
```
</td>
</tr>
</table>

# [Sparse voxel atlas](https://niivue.github.io/niivue/features/atlas.sparse.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/2d81b7a9-1b25-4417-aa3d-29230efd4ec6.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
var volumeList1 = [
  { url: "../images/inia19-t1-brain.nii.gz" },
  { url: "../images/inia19-NeuroMaps.nii.gz", opacity: 0.5 },
];
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = data.string;
}
var nv1 = new niivue.Niivue({ onLocationChange: handleLocationChange });
nv1.attachTo("gl1");
await nv1.loadVolumes(volumeList1);
/*async function fetchJSON(fnm) {
  const response = await fetch(fnm);
  const js = await response.json();
  return js;
}
let cmap = await fetchJSON("../demos/images/inia19-NeuroMaps.json");
nv1.volumes[1].setColormapLabel(cmap);*/
await nv1.volumes[1].setColormapLabelFromUrl("../images/inia19-NeuroMaps.json");
nv1.updateGLVolume();
document.getElementById("check1").addEventListener("change", doCheckClick);
function doCheckClick() {
  nv1.setAtlasOutline(this.checked);
}
var slider = document.getElementById("alphaSlider");
slider.oninput = function () {
  nv1.setOpacity(1, this.value / 255);
};
document.getElementById("about").addEventListener("click", doAbout);
function doAbout() {
  window.alert(
    "This demo demonstrates sparse labeling. \
	The inia19 atlas has 1004 labels in the range 0..1606 ."
  );
}

	
```
</td>
</tr>
</table>

# [Modulation](https://niivue.github.io/niivue/features/modulate.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/2fb7e334-21fb-41db-8f9d-c34dcef2b5ec.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
about.onclick = function () {
  window.alert(
    "Experimental diffusion tensor V1 validation (to do: assumptions regarding \
	neurological convention, slice orientation, world space)"
  );
};
function minMax() {
  let mn = 0.01 * slide.value;
  let mx = 0.01 * slideX.value;
  nv1.volumes[0].cal_min = Math.min(mn, mx);
  nv1.volumes[0].cal_max = Math.max(mn, mx);
  nv1.updateGLVolume();
}
slide.oninput = function () {
  minMax();
};
slideX.oninput = function () {
  minMax();
};
check.onchange = function () {
  nv1.isAlphaClipDark = this.checked;
  nv1.updateGLVolume();
};
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
var volumeList1 = [
  {
    url: "../images/FA.nii.gz",
    opacity: 1,
    visible: false,
  },
  {
    url: "../images/V1.nii.gz",
    opacity: 0.0,
    visible: false,
  },
];
var nv1 = new niivue.Niivue({
  backColor: [0.0, 0.0, 0.2, 1],
  show3Dcrosshair: true,
  onLocationChange: handleLocationChange,
});
nv1.opts.dragMode = nv1.dragModes.pan;
nv1.opts.yoke3Dto2DZoom = true;
nv1.setCrosshairWidth(0.1);
//v1 aided if all views show voxel centers
nv1.opts.isForceMouseClickToVoxelCenters = true;
nv1.attachTo("gl1");
//V1 lines REQUIRES nearest neighbor interpolation
nv1.setInterpolation(true);
await nv1.loadVolumes(volumeList1);
nv1.scene.crosshairPos = nv1.vox2frac([41, 46, 28]);
var drop = document.getElementById("mode");
drop.onchange = function () {
  let mode = document.getElementById("mode").selectedIndex;
  if (mode === 0) {
    nv1.setOpacity(0, 1.0); //show FA
    nv1.setOpacity(1, 0.0); //hide V1
  } else if (mode > 2) {
    nv1.setOpacity(0, 1.0); //show FA
    nv1.setOpacity(1, 1.0); //show V1
  } else {
    nv1.setOpacity(0, 0.0); //hide FA
    nv1.setOpacity(1, 1.0); //show V1
  }
  if (mode === 4 || mode === 2) {
    nv1.setModulationImage(nv1.volumes[1].id, nv1.volumes[0].id);
  } else nv1.setModulationImage(nv1.volumes[1].id, null);
  nv1.opts.isV1SliceShader = mode > 2;
  nv1.updateGLVolume();
};
drop.onchange();
check.onchange();

	
```
</td>
</tr>
</table>

# [Multiplanar Layout (Auto, Column, Grid, Row)](https://niivue.github.io/niivue/features/layout.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/4dd0b1db-8941-485c-8ab0-e244eef26775.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
padSlider.oninput = function () {
  nv1.setMultiplanarPadPixels(this.value);
};
renderCheck.onchange = function () {
  nv1.opts.multiplanarForceRender = this.checked;
  nv1.drawScene();
};
timelineCheck.onchange = function () {
  nv1.graph.autoSizeMultiplanar = this.checked;
  nv1.drawScene();
};
layout.onchange = function () {
  nv1.setMultiplanarLayout(Number(this.value));
};
var volumeList1 = [{ url: "../images/pcasl.nii.gz" }];
let opts = {
  show3Dcrosshair: true,
  backColor: [0.64, 0.76, 0.68, 1],
};
var nv1 = new niivue.Niivue(opts);
nv1.attachTo("gl1");
nv1.setMultiplanarPadPixels(5);
nv1.graph.opacity = 1.0;
await nv1.loadVolumes(volumeList1);

	
```
</td>
</tr>
</table>

# [Modulation of scalar volumes](https://niivue.github.io/niivue/features/modulateScalar.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/24c352b1-89f8-46bd-bb5c-c9d65db51a05.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var sliderT = document.getElementById("slideT");
sliderT.oninput = function () {
  nv1.volumes[2].cal_max = 0.1 * this.value;
  nv1.updateGLVolume();
};
var sliderC = document.getElementById("slideC");
sliderC.oninput = function () {
  nv1.volumes[1].cal_max = this.value;
  nv1.updateGLVolume();
};
var slider2 = document.getElementById("slide2");
slider2.oninput = function () {
  nv1.overlayOutlineWidth = 0.25 * this.value;
  nv1.updateGLVolume();
};
document.getElementById("check").addEventListener("change", doCheckClick);
function doCheckClick() {
  nv1.isAlphaClipDark = this.checked;
  nv1.updateGLVolume();
}
document.getElementById("check2").addEventListener("change", doCheck2Click);
function doCheck2Click() {
  drop.onchange();
}
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
var volumeList1 = [
  {
    url: "../images/mean_func.nii.gz",
    opacity: 1,
    colormap: "gray",
  },
  {
    url: "../images/cope1.nii.gz",
    colormap: "winter",
    opacity: 0,
    cal_min: 0.0,
    cal_max: 100,
  },
  {
    url: "../images/tstat1.nii.gz",
    opacity: 1,
    colormap: "warm",
    cal_min: 0,
    cal_max: 4.5,
  },
];
var nv1 = new niivue.Niivue({
  backColor: [0.2, 0.2, 0.3, 1],
  onLocationChange: handleLocationChange,
});
nv1.attachTo("gl1");
nv1.overlayOutlineWidth = 0.25;
await nv1.loadVolumes(volumeList1);
nv1.opts.isColorbar = true;
nv1.setInterpolation(true);
nv1.scene.crosshairPos = [0.55, 0.5, 0.8];
nv1.setSliceType(nv1.sliceTypeMultiplanar);
var drop = document.getElementById("mode");
drop.onchange = function () {
  let mode = document.getElementById("mode").selectedIndex;
  nv1.setOpacity(0, 1.0); //background opaque
  nv1.setOpacity(1, 0.0); //hide tstat
  nv1.setOpacity(2, 0.0); //hide cope
  nv1.setOpacity(Math.min(2, mode), 1.0);
  if (mode == 3) {
    nv1.setOpacity(1, 1.0); //show cope
    nv1.setOpacity(2, 0.0); //hide tstat
    let modulateAlpha = document.getElementById("check2").checked;
    nv1.setModulationImage(nv1.volumes[1].id, nv1.volumes[2].id, modulateAlpha);
  } else nv1.setModulationImage(nv1.volumes[1].id, null);
};
drop.onchange();

	
```
</td>
</tr>
</table>

# [Modulation of AFNI statistics](https://niivue.github.io/niivue/features/modulateAfni.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/ff641edb-3d42-4a25-aff2-14650e71bc80.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

opacitySlider.onchange = function () {
  drop.onchange();
};
document.getElementById("ExtButton").addEventListener("click", doExtButton);
function doExtButton() {
  let str = "Volume does not have an extension";
  if (nv1.volumes[1].hdr.extensions.length > 0) {
    let buf = nv1.volumes[1].hdr.extensions[0].edata;
    str = String.fromCharCode.apply(null, new Uint8Array(buf));
  }
  alert(str);
}
document
  .getElementById("outlineCheck")
  .addEventListener("change", doCheckClick);
function doCheckClick() {
  if (this.checked) nv1.overlayOutlineWidth = 1.0;
  else nv1.overlayOutlineWidth = 0.0;
  nv1.drawScene();
}
document
  .getElementById("smoothCheck")
  .addEventListener("change", doCheck4Click);
function doCheck4Click() {
  nv1.setInterpolation(!this.checked);
  nv1.drawScene();
}
document
  .getElementById("modulateSlider")
  .addEventListener("change", modulateChange);
function modulateChange() {
  drop.onchange();
}
var volumeList1 = [
  { url: "../images/mni152.nii.gz" },
  {
    url: "../images/stats.nv_demo_mskd.nii.gz",
    colormap: "blue2magenta",
    colormapNegative: "blue2cyan",
    frame4D: 1,
    cal_min: 0.01,
    cal_max: 3.3641,
  },
  {
    url: "../images/stats.nv_demo_mskd.nii.gz",
    colormap: "afni_reds_inv",
    colormapNegative: "afni_blues_inv",
    frame4D: 0,
    cal_max: 3.09735,
    cal_min: 0,
  },
];
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
let defaults = {
  loadingText: "there are no images",
  backColor: [1, 1, 1, 1],
  show3Dcrosshair: true,
  logging: true,
  onLocationChange: handleLocationChange,
};
var nv1 = new niivue.Niivue(defaults);
nv1.setInterpolation(true);
nv1.opts.multiplanarForceRender = true;
nv1.attachTo("gl1");
nv1.setSliceType(nv1.sliceTypeMultiplanar);
await nv1.loadVolumes(volumeList1);
var drop = document.getElementById("mode");
drop.onchange = function () {
  let mode = document.getElementById("mode").selectedIndex;
  nv1.setOpacity(0, 1.0); //background opaque
  nv1.setOpacity(1, 0.0); //hide tstat
  nv1.setOpacity(2, 0.0); //hide cope
  let visibleOverlay = Math.min(mode, 2);
  let opacity = opacitySlider.value / 255;
  nv1.overlayOutlineAlpha = opacity;
  nv1.setOpacity(visibleOverlay, opacity);
  nv1.overlayAlphaShader = 1.0;
  if (mode === 3) {
    nv1.overlayAlphaShader = opacity;
    let modulateAlpha = modulateSlider.value;
    nv1.setModulationImage(nv1.volumes[2].id, nv1.volumes[1].id, modulateAlpha);
  } else nv1.setModulationImage(nv1.volumes[2].id, null);
};
nv1.overlayOutlineWidth = 1;
nv1.volumes[0].colorbarVisible = false; //hide colorbar for anatomical scan
nv1.volumes[1].colorbarVisible = false; //hide colorbar for anatomical scan
nv1.opts.isColorbar = true;
drop.onchange();
nv1.createOnLocationChange();

	
```
</td>
</tr>
</table>

# [Fixed canvas size](https://niivue.github.io/niivue/features/fixedsize.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/a62414bc-3649-4b5f-a67d-c55f7aefdc83.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var volumeList1 = [{ url: "../images/FLAIR.nii.gz" }];
var nv1 = new niivue.Niivue({
  isResizeCanvas: false,
});
nv1.attachTo("gl");
await nv1.loadVolumes(volumeList1);

	
```
</td>
</tr>
</table>

# [Segmented image with named labels](https://niivue.github.io/niivue/features/segment.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/e3d4681d-f2f3-45c8-b468-7dad6580063d.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var slider = document.getElementById("alphaSlider");
slider.oninput = function () {
  nv1.setOpacity(1, this.value / 255);
};
var check1 = document.getElementById("check1");
check1.onclick = function (event) {
  nv1.volumes[0].opacity = this.checked;
  nv1.updateGLVolume();
};
var check2 = document.getElementById("check2");
check2.onclick = function (event) {
  nv1.isAlphaClipDark = this.checked;
  nv1.updateGLVolume();
};
var check3 = document.getElementById("check3");
check3.onclick = function (event) {
  nv1.setInterpolation(!this.checked);
};
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
var btn = document.getElementById("custom");
btn.onclick = function (event) {
  var val = document.getElementById("scriptText").value;
  val += ";nv1.volumes[1].setColormapLabel(cmap);nv1.updateGLVolume();";
  val && eval(val);
};
let defaults = {
  logging: false,
  dragAndDropEnabled: true,
  backColor: [0.3, 0.3, 0.3, 1],
  show3Dcrosshair: true,
  onLocationChange: handleLocationChange,
};
var nv1 = new niivue.Niivue(defaults);
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
var volumeList1 = [
  {
    url: "../images/mni152.nii.gz",
  },
  {
    url: "../images/mni152_pveseg.nii.gz",
    opacity: 0.5,
  },
];
await nv1.loadVolumes(volumeList1);
nv1.opts.multiplanarForceRender = true;
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.graph.autoSizeMultiplanar = true;
nv1.updateGLVolume(); //apply labeled colormap
btn.click();

	
```
</td>
</tr>
</table>

# [Mosaics](https://niivue.github.io/niivue/features/mosaics.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/4f98484a-df9e-47bc-a964-6a9e6b9459d2.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
var volumeList1 = [
  {
    url: "../images/mni152.nii.gz",
  },
];
var nv1 = new niivue.Niivue();
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
var txt = document.getElementById("str");
nv1.setSliceType(nv1.sliceTypeAxial);
nv1.setSliceMosaicString(txt.value);
document.getElementById("str").addEventListener("keyup", doStr);
function doStr() {
  nv1.setSliceMosaicString(txt.value);
}
document.getElementById("about").addEventListener("click", doAbout);
function doAbout() {
  window.alert(
    "Choose axial (A), coronal (C) or sagittal (S) slices. \ 
	Modify with cross slices (X) and renderings (R)."
  );
}

	
```
</td>
</tr>
</table>

# [Advanced mosaics](https://niivue.github.io/niivue/features/mosaics2.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/a5c9871e-6c40-432e-94b9-565b5088118e.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
var dropDrag = document.getElementById("dragMode");
dropDrag.onchange = function () {
  switch (document.getElementById("dragMode").value) {
    case "none":
      nv1.opts.dragMode = nv1.dragModes.none;
      break;
    case "contrast":
      nv1.opts.dragMode = nv1.dragModes.contrast;
      break;
    case "measurement":
      nv1.opts.dragMode = nv1.dragModes.measurement;
      break;
    case "pan":
      nv1.opts.dragMode = nv1.dragModes.pan;
      break;
  }
};
var slider = document.getElementById("gamma");
slider.oninput = function () {
  nv1.setGamma(0.1 * this.value);
};
document.getElementById("check1").addEventListener("change", doCheckClick);
function doCheckClick() {
  nv1.setRadiologicalConvention(this.checked);
}
document.getElementById("check3").addEventListener("change", doCheck3Click);
function doCheck3Click() {
  nv1.setSliceMM(this.checked);
}
document.getElementById("check5").addEventListener("change", doCheck5Click);
function doCheck5Click() {
  nv1.opts.isRuler = this.checked;
  nv1.drawScene();
}
document.getElementById("check6").addEventListener("change", doCheck6Click);
function doCheck6Click() {
  nv1.opts.sagittalNoseLeft = this.checked;
  nv1.drawScene();
}
document.getElementById("check7").addEventListener("change", doCheck7Click);
function doCheck7Click() {
  nv1.opts.isColorbar = this.checked;
  nv1.drawScene();
}
document.getElementById("check8").addEventListener("change", doCheck8Click);
function doCheck8Click() {
  if (this.checked) nv1.setColormapNegative(nv1.volumes[1].id, "winter");
  else nv1.setColormapNegative(nv1.volumes[1].id, "");
  nv1.drawScene();
}
document.getElementById("check9").addEventListener("change", doCheck9Click);
function doCheck9Click() {
  nv1.opts.isOrientCube = this.checked;
  nv1.drawScene();
}
document.getElementById("check10").addEventListener("change", doCheck10Click);
function doCheck10Click() {
  nv1.setHighResolutionCapable(this.checked);
}
var volumeList1 = [
  {
    url: "../images/fslmean.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
  {
    url: "../images/fslt.nii.gz",
    colormap: "warm",
    colormapNegative: "winter",
    opacity: 1,
    cal_min: 1,
    cal_max: 6,
    visible: true,
  },
];
var nv1 = new niivue.Niivue({ backColor: [1, 1, 1, 1] });
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
var txt = document.getElementById("str");
nv1.setSliceType(nv1.sliceTypeAxial);
nv1.opts.isColorbar = true;
nv1.setSliceMosaicString(txt.value);
document.getElementById("str").addEventListener("keyup", doStr);
function doStr() {
  nv1.setSliceMosaicString(txt.value);
}
document.getElementById("about").addEventListener("click", doAbout);
function doAbout() {
  window.alert(
    "Choose axial (A), coronal (C) or sagittal (S) slices. \
	Modify with cross slices (X) and renderings (R)."
  );
}

	
```
</td>
</tr>
</table>

# [World space](https://niivue.github.io/niivue/features/worldspace.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/3dbd0e3d-0c8f-424f-8a67-1ab019214ad8.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var dropDrag = document.getElementById("dragMode");
dropDrag.onchange = function () {
  switch (document.getElementById("dragMode").value) {
    case "none":
      nv1.opts.dragMode = nv1.dragModes.none;
      break;
    case "contrast":
      nv1.opts.dragMode = nv1.dragModes.contrast;
      break;
    case "measurement":
      nv1.opts.dragMode = nv1.dragModes.measurement;
      break;
    case "pan":
      nv1.opts.dragMode = nv1.dragModes.pan;
      break;
  }
};
document.getElementById("check1").addEventListener("change", doCheckClick);
function doCheckClick() {
  nv1.setRadiologicalConvention(this.checked);
}
document.getElementById("check2").addEventListener("change", doCheck2Click);
function doCheck2Click() {
  nv1.opts.sagittalNoseLeft = this.checked;
  nv1.drawScene();
}
document.getElementById("check3").addEventListener("change", doCheck3Click);
function doCheck3Click() {
  nv1.setSliceMM(this.checked);
}
var volumeList1 = [
  {
    url: "../images/FLAIR.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
];
var nv1 = new niivue.Niivue({
  dragAndDropEnabled: true,
  backColor: [1, 1, 1, 1],
  show3Dcrosshair: true,
});
nv1.setSliceMM(true);
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
	
```
</td>
</tr>
</table>

# [Advanced world space](https://niivue.github.io/niivue/features/worldspace2.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/038c6daf-cead-416a-9730-cdbf70a436d5.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var dropDrag = document.getElementById("dragMode");
dropDrag.onchange = function () {
  switch (document.getElementById("dragMode").value) {
    case "none":
      nv1.opts.dragMode = nv1.dragModes.none;
      break;
    case "contrast":
      nv1.opts.dragMode = nv1.dragModes.contrast;
      break;
    case "measurement":
      nv1.opts.dragMode = nv1.dragModes.measurement;
      break;
    case "pan":
      nv1.opts.dragMode = nv1.dragModes.pan;
      break;
  }
};
document.getElementById("check1").addEventListener("change", doCheckClick);
function doCheckClick() {
  nv1.setRadiologicalConvention(this.checked);
}
document.getElementById("check2").addEventListener("change", doCheck2Click);
function doCheck2Click() {
  nv1.setCornerOrientationText(this.checked);
}
document.getElementById("check3").addEventListener("change", doCheck3Click);
function doCheck3Click() {
  nv1.setSliceMM(this.checked);
}
var dxslider = document.getElementById("dxSlider");
dxslider.oninput = function () {
  let dx = parseFloat(this.value);
  if (dx > 10) dx = Infinity;
  nv1.setMeshThicknessOn2D(dx);
};
document.getElementById("check7").addEventListener("change", doCheck7Click);
function doCheck7Click() {
  nv1.opts.isColorbar = this.checked;
  nv1.drawScene();
}
document.getElementById("check8").addEventListener("change", doCheck8Click);
function doCheck8Click() {
  nv1.opts.isOrientCube = this.checked;
  nv1.drawScene();
}
document.getElementById("check9").addEventListener("change", doCheck9Click);
function doCheck9Click() {
  let pad = 0;
  if (this.checked) pad = 5;
  nv1.opts.multiplanarPadPixels = pad;
  nv1.drawScene();
}
document.getElementById("check10").addEventListener("change", doCheck10Click);
function doCheck10Click() {
  nv1.setHighResolutionCapable(this.checked);
}
document.getElementById("check11").addEventListener("change", doCheck11Click);
function doCheck11Click() {
  nv1.opts.multiplanarForceRender = this.checked;
  nv1.drawScene();
}

var volumeList1 = [
  {
    url: "../images/mni152.nii.gz", //"./images/RAS.nii.gz", 
	 // "./images/spm152.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
];
var nv1 = new niivue.Niivue({
  dragAndDropEnabled: true,
  backColor: [0.3, 0.2, 0.4, 1],
  show3Dcrosshair: true,
});
nv1.setSliceMM(true);
nv1.attachTo("gl1");
nv1.setClipPlane([-0.1, 270, 0]);
nv1.setRenderAzimuthElevation(120, 10);
nv1.setHighResolutionCapable(true);
await nv1.loadVolumes(volumeList1);
await nv1.loadMeshes([
  {
    url: "../images/BrainMesh_ICBM152.lh.mz3",
    rgba255: [200, 162, 255, 255],
  },
  { url: "../images/dpsv.trx", rgba255: [255, 255, 255, 255] },
]);
nv1.setSliceType(nv1.sliceTypeMultiplanar);

	
```
</td>
</tr>
</table>

# [Images with shear](https://niivue.github.io/niivue/features/shear.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/8c5570b8-bfb1-463e-bf88-61728c4f0b24.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
document.getElementById("check3").addEventListener("change", doCheck3Click);
function doCheck3Click() {
  nv1.setSliceMM(this.checked);
}
document.getElementById("smooth").addEventListener("change", doSmooth);
function doSmooth() {
  nv1.setInterpolation(!this.checked);
}
var volumeList1 = [
  // first item is background image
  {
    url: "../images/shear.nii.gz", //"./images/RAS.nii.gz", "./images/spm152.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
];
var nv1 = new niivue.Niivue({
  dragAndDropEnabled: true,
  backColor: [1, 1, 1, 1],
  show3Dcrosshair: true,
});
nv1.setSliceMM(true);
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
await nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.opts.multiplanarForceRender = true;
document.getElementById("about").addEventListener("click", doAbout);
function doAbout() {
  window.alert(
    "CT scans often have include gantry tilt to reduce artifacts from teeth \
	fillings and radiation dose to the eyeballs. This creates rhomboidal voxels.\
	Viewing 2D slices in world space reveals this shear. Note that 3D renderings\
	are always in world space (so meshes and other objects align nicely)."
  );
}
let connectome = {
  name: "shearConnectome",
  nodeColormap: "viridis",
  nodeColormapNegative: "viridis",
  nodeMinColor: 2,
  nodeMaxColor: 4,
  nodeScale: 3, //scale factor for node, e.g. if 2 and a node has size 3,\
	// a 6mm ball is drawn
  edgeColormap: "warm",
  edgeColormapNegative: "winter",
  edgeMin: 2,
  edgeMax: 4,
  edgeScale: 1,
  nodes: {
    names: ["Sphere", "Pyramid", "Box", "CylinderLow"], //currently unused
    X: [0, -41, -37, -21], //Xmm for each node
    Y: [0, -59, -6, -21], //Ymm for each node
    Z: [0, 3, 16, -22], //Zmm for each node
    Color: [2, 2, 3, 4], //Used to interpolate color
    Size: [2, 2, 3, 4], //Size of node
  },
  edges: [1, 4, -3, 4, 0, 1, 0, 6, 0, 0, 1, 0, 0, 0, 0, 1],
}; //connectome{}
await nv1.loadConnectome(connectome);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.opts.multiplanarForceRender = true;

	
```
</td>
</tr>
</table>

# [Multiuser basic 3D](https://niivue.github.io/niivue/features/multiuser.3d.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/deebdcf8-7713-49fc-9e5c-fbe56b216f1e.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

function toggleHippo() {
  let buttonElem = document.getElementById("toggleHippoButton");
  if (isHippoShowing) {
    nv1.removeVolumeByUrl(url);
    buttonElem.innerText = "Add Hippocampus";
    isHippoShowing = false;
  } else {
    nv1.addVolumeFromUrl({ url });
    buttonElem.innerText = "Remove Hippocampus";
    isHippoShowing = true;
  }
}

const url = "../images/hippo.nii.gz";
var isHippoShowing = false;
var volumeList1 = [
  // first item is background image
  {
    url: "../images/mni152.nii.gz", //"./images/RAS.nii.gz", "./images/spm152.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
];
var nv1 = new niivue.Niivue();
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeRender);
var controller = new niivue.NVController(nv1);
controller.connectToSession("niivue-3d");

	
```
</td>
</tr>
</table>

# [Multiuser Time Series](https://niivue.github.io/niivue/features/multiuser.timeseries.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/c7fd20ea-04dc-4d85-abe7-df700e26cdd6.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var volumeList1 = [
  // first item is background image
  {
    url: "../images/pcasl.nii.gz", //"./images/RAS.nii.gz", "./images/spm152.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
];
var nv1 = new niivue.Niivue();
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.graph.autoSizeMultiplanar = true;
nv1.graph.normalizeValues = false;
nv1.graph.opacity = 1.0;

var controller = new niivue.NVController(nv1);
controller.onFrameChange = updateFrameValue;
controller.connectToSession("timeseries");

function checkClick(cb) {
  nv1.graph.normalizeValues = cb.checked;
  nv1.updateGLVolume();
}
let currentVol = 0;
function prevVolume() {
  currentVol = Math.max(currentVol - 1, 0);
  nv1.setFrame4D(nv1.volumes[0].id, currentVol);
  document.getElementById("volume").innerHTML = "volume " + currentVol;
}
function nextVolume() {
  currentVol++;
  currentVol = Math.min(currentVol, nv1.getFrame4D(nv1.volumes[0].id) - 1);
  nv1.setFrame4D(nv1.volumes[0].id, currentVol);
  document.getElementById("volume").innerHTML = "volume " + currentVol;
}
function updateFrameValue(volume, index) {
  document.getElementById("volume").innerHTML = "volume " + index;
  currentVol = index;
}
var animationTimer = null;
function doAnimate() {
  currentVol++;
  if (currentVol >= nv1.getFrame4D(nv1.volumes[0].id)) currentVol = 0;
  nv1.setFrame4D(nv1.volumes[0].id, currentVol);
}
function animateVolume() {
  if (animationTimer == null) animationTimer = setInterval(doAnimate, 100);
  else {
    clearInterval(animationTimer);
    animationTimer = null;
  }
}

	
```
</td>
</tr>
</table>

# [Multiuser color maps](https://niivue.github.io/niivue/features/multiuser.imageoptions.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/f51f295a-8ae0-45fb-b211-c00bf85a5097.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

var opacitySlider = document.getElementById("opacitySlider");

opacitySlider.oninput = function () {
  nv1.volumes[0].opacity = this.value;
  nv1.updateGLVolume();
};
var volumeList1 = [
  // first item is background image
  {
    url: "../images/mni152.nii.gz", //"./images/RAS.nii.gz", "./images/spm152.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
];
var nv1 = new niivue.Niivue();
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1).then(() => {
  nv1.setSliceType(nv1.sliceTypeMultiplanar);
  var controller = new niivue.NVController(nv1);
  controller.connectToSession("imageoptions");
});

cmaps = nv1.colormaps();
cmapEl = document.getElementById("colormaps");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function () {
    nv1.volumes[0].colormap = cmaps[i];
    nv1.updateGLVolume();
  };
  cmapEl.appendChild(btn);
}

	
```
</td>
</tr>
</table>

# [Multiuser meshes](https://niivue.github.io/niivue/features/multiuser.meshes.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/a0cf6e81-bf9e-4274-b93e-65403704f970.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

const meshOptions = {
  url: "../images/CIT168.mz3",
  rgba255: [0, 0, 255, 255],
};
let isMeshShowing = false;

var slider = document.getElementById("meshSlider");
// Update the current slider value (each time you drag the slider handle)
slider.oninput = function () {
  nv1.setMeshProperty(nv1.meshes[0].id, "rgba255", [this.value, 164, 164, 255]);
};

var volumeList1 = [
  // first item is background image
  {
    url: "../images/mni152.nii.gz", //"./images/RAS.nii.gz", "./images/spm152.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
];
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [1, 1, 1, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
await nv1.loadMeshes([
  {
    url: "../images/BrainMesh_ICBM152.lh.mz3",
    rgba255: [222, 164, 164, 255],
  },
]);
nv1.setClipPlane([-0.1, 270, 0]);
nv1.setMeshShader(nv1.meshes[0].id, "Outline");

let controller = new niivue.NVController(nv1);
controller.connectToSession("mesh");

let cmaps = nv1.meshShaderNames();
let cmapEl = document.getElementById("shaders");
for (let i = 0; i < cmaps.length; i++) {
  let btn = document.createElement("button");
  btn.innerHTML = cmaps[i];
  btn.onclick = function (e) {
    let id = nv1.meshes[0].id;
    if (e.shiftKey) id = nv1.meshes[1].id;
    nv1.setMeshShader(id, cmaps[i]);
  };
  cmapEl.appendChild(btn);
}
document
  .getElementById("customShader")
  .addEventListener("click", doCustomShader);
function doCustomShader() {
  let idx = nv1.setCustomMeshShader(
    document.getElementById("customText").value
  );
  let id = nv1.meshes[0].id;
  nv1.setMeshShader(id, idx);
}
document
  .getElementById("toggleMeshButton")
  .addEventListener("click", toggleMesh);
function toggleMesh() {
  let buttonElem = document.getElementById("toggleMeshButton");
  if (isMeshShowing) {
    var mesh = nv1.getMediaByUrl(meshOptions.url);
    if (mesh) {
      nv1.removeMesh(mesh);
      buttonElem.innerText = "Add CIT168.mz3";
      isMeshShowing = false;
    }
  } else {
    nv1.addMeshFromUrl(meshOptions);
    buttonElem.innerText = "Remove CIT168.mz3";
    isMeshShowing = true;
  }
}

	
```
</td>
</tr>
</table>

# [User scripting](https://niivue.github.io/niivue/features/scripts.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/f564dad9-1ab2-49ee-9f26-9aa76d88db5d.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
document.getElementById("scriptButton").addEventListener("click", doScript);
function doScript() {
  var val = document.getElementById("scriptText");
  val && eval(val.value);
}
var volumeList1 = [
  {
    url: "../images/mni152.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
];
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [1, 0.5, 1, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
nv1.loadMeshes([
  {
    url: "../images/BrainMesh_ICBM152.lh.mz3",
    rgba255: [222, 164, 164, 255],
  },
  { url: "../images/motor_4t95mesh.rh.mz3", rgba255: [0, 0, 255, 255] },
]);
nv1.setClipPlane([0.1, 0, 145]);
nv1.setRenderAzimuthElevation(100, 25);

	
```
</td>
</tr>
</table>

# [Shiny volume rendering](https://niivue.github.io/niivue/features/shiny.volumes.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/9d170d79-4bc4-482d-b262-0f1967e1e3cb.png)


</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
checkXRay.onchange = function () {
  nv1.opts.meshXRay = this.checked * 0.05;
  nv1.drawScene();
};
dragMode.onchange = function () {
  switch (document.getElementById("dragMode").value) {
    case "none":
      nv1.opts.dragMode = nv1.dragModes.none;
      break;
    case "contrast":
      nv1.opts.dragMode = nv1.dragModes.contrast;
      break;
    case "measurement":
      nv1.opts.dragMode = nv1.dragModes.measurement;
      break;
    case "pan":
      nv1.opts.dragMode = nv1.dragModes.pan;
      break;
    case "slicer3D":
      nv1.opts.dragMode = nv1.dragModes.slicer3D;
      break;
  }
};
zoomSlider.oninput = function () {
  nv1.setScale(this.value / 100);
};
renderMode.onchange = function () {
  nv1.setVolumeRenderIllumination(this.value);
};
matCaps.onchange = function () {
  let matCapName = document.getElementById("matCaps").value;
  nv1.loadMatCapTexture("../matcaps/" + matCapName + ".jpg");
};
var volumeList1 = [
  { url: "../images/mni152.nii.gz", cal_min: 30, cal_max: 80 },
  {
    url: "../images/spmMotor.nii.gz",
    cal_min: 3,
    cal_max: 8,
    colormap: "warm",
  },
];
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
let defaults = {
  loadingText: "there are no images",
  backColor: [1, 1, 1, 1],
  show3Dcrosshair: true,
  limitFrames4D: 3,
  onLocationChange: handleLocationChange,
};
var nv1 = new niivue.Niivue(defaults);
nv1.attachTo("gl1");
nv1.setSliceType(nv1.sliceTypeRender);
nv1.opts.multiplanarForceRender = true;
nv1.setVolumeRenderIllumination(1.0);
nv1.setClipPlane([0.3, 180, 20]);
await nv1.loadVolumes(volumeList1);
await nv1.loadMeshes([
  { url: "../images/connectome.jcon" },
  { url: "../images/dpsv.trx", rgba255: [0, 142, 0, 255] },
]);
matCaps.dispatchEvent(new Event("change"));
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.graph.autoSizeMultiplanar = true;
nv1.opts.multiplanarForceRender = true;

	
```
</td>
</tr>
</table>

# [Dragging callbacks](https://niivue.github.io/niivue/features/dragCallback.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/483428eb-8571-46ac-a067-db03bdf5db18.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
checkXRay.onchange = function () {
  nv1.opts.meshXRay = this.checked * 0.05;
  nv1.drawScene();
};
dragMode.onchange = function () {
  switch (document.getElementById("dragMode").value) {
    case "none":
      nv1.opts.dragMode = nv1.dragModes.none;
      break;
    case "contrast":
      nv1.opts.dragMode = nv1.dragModes.contrast;
      break;
    case "measurement":
      nv1.opts.dragMode = nv1.dragModes.measurement;
      break;
    case "pan":
      nv1.opts.dragMode = nv1.dragModes.pan;
      break;
    case "slicer3D":
      nv1.opts.dragMode = nv1.dragModes.slicer3D;
      break;
  }
};
zoomSlider.oninput = function () {
  nv1.setScale(this.value / 100);
};
renderMode.onchange = function () {
  nv1.setVolumeRenderIllumination(this.value);
};
matCaps.onchange = function () {
  let matCapName = document.getElementById("matCaps").value;
  nv1.loadMatCapTexture("../matcaps/" + matCapName + ".jpg");
};
var volumeList1 = [
  { url: "../images/mni152.nii.gz", cal_min: 30, cal_max: 80 },
  {
    url: "../images/spmMotor.nii.gz",
    cal_min: 3,
    cal_max: 8,
    colormap: "warm",
  },
];
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
let defaults = {
  loadingText: "there are no images",
  backColor: [1, 1, 1, 1],
  show3Dcrosshair: true,
  limitFrames4D: 3,
  onLocationChange: handleLocationChange,
};
var nv1 = new niivue.Niivue(defaults);
nv1.attachTo("gl1");
nv1.setSliceType(nv1.sliceTypeRender);
nv1.opts.multiplanarForceRender = true;
nv1.setVolumeRenderIllumination(1.0);
nv1.setClipPlane([0.3, 180, 20]);
await nv1.loadVolumes(volumeList1);
await nv1.loadMeshes([
  { url: "../images/connectome.jcon" },
  { url: "../images/dpsv.trx", rgba255: [0, 142, 0, 255] },
]);
matCaps.dispatchEvent(new Event("change"));
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.graph.autoSizeMultiplanar = true;
nv1.opts.multiplanarForceRender = true;

	
```
</td>
</tr>
</table>

# [Voxels with complex numbers](https://niivue.github.io/niivue/features/complex.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/8552536a-da1c-4176-94b9-cfb2c4e517fc.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
sliceType.onchange = function () {
  nv1.setSliceType(parseInt(this.value));
};
function handleIntensityChange(data) {
  document.getElementById("intensity").innerHTML = data.string;
}
var volumeList1 = [{ url: "../images/complex.nii.gz" }];
var nv1 = new niivue.Niivue({
  onLocationChange: handleIntensityChange,
});
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);

	
```
</td>
</tr>
</table>

# Additive [voxels](https://niivue.github.io/niivue/features/additive.voxels.html) and

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/430ad282-3259-494e-b02a-c36bcccc759d.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
document.getElementById("checkAlpha").onchange = function () {
  nv1.volumes[1].alphaThreshold = this.checked;
  nv1.volumes[2].alphaThreshold = this.checked;
  nv1.updateGLVolume();
};
document.getElementById("checkAdditive").onchange = function () {
  nv1.setAdditiveBlend(this.checked);
};
document.getElementById("slideRed").oninput = function () {
  nv1.volumes[1].cal_min = 0.1 * this.value;
  nv1.updateGLVolume();
};
document.getElementById("slideGreen").oninput = function () {
  nv1.volumes[2].cal_min = 0.1 * this.value;
  nv1.updateGLVolume();
};
document.getElementById("about").addEventListener("click", doAbout);
function doAbout() {
  window.alert(
    "In the emissive additive color mode, red and green combine to form yellow. Otherwise, higher overlays overwrite color of lower layers."
  );
}
var volumeList1 = [
  { url: "../images/mni152.nii.gz" },
  {
    url: "../images/narps-4965_9U7M-hypo1_unthresh.nii.gz",
    colormap: "red",
    cal_min: 2,
    cal_max: 4,
  },
  {
    url: "../images/narps-4735_50GV-hypo1_unthresh.nii.gz",
    colormap: "green",
    cal_min: 2,
    cal_max: 4,
  },
];
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}

var nv1 = new niivue.Niivue({
  loadingText: "there are no images",
  backColor: [1, 1, 1, 1],
  show3Dcrosshair: true,
  onLocationChange: handleLocationChange,
});
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.setSliceMM(false);
nv1.opts.isColorbar = true;
nv1.setAdditiveBlend(true);
await nv1.loadVolumes(volumeList1);
nv1.volumes[0].colorbarVisible = false; //hide colorbar for anatomical scan
nv1.opts.multiplanarForceRender = true;
nv1.setInterpolation(true);
nv1.updateGLVolume();
checkAlpha.onchange();

	
```
</td>
</tr>
</table>

# Additive [mesh](https://niivue.github.io/niivue/features/additive.mesh.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/f554ae0b-566a-4cf8-9c25-01b439b1b927.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
additiveCheck.onchange = function () {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    1,
    "isAdditiveBlend",
    this.checked
  );
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    2,
    "isAdditiveBlend",
    this.checked
  );
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    3,
    "isAdditiveBlend",
    this.checked
  );
};
opacitySlider.onchange = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "opacity", this.value * 0.1);
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 2, "opacity", this.value * 0.1);
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 3, "opacity", this.value * 0.1);
};
redSlider.onchange = function () {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    1,
    "cal_min",
    parseInt(this.value) + 0.5
  );
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    1,
    "cal_max",
    parseInt(this.value) + 2.5
  );
};
greenSlider.onchange = function () {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    2,
    "cal_min",
    parseInt(this.value) + 0.5
  );
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    2,
    "cal_max",
    parseInt(this.value) + 2.5
  );
};
blueSlider.onchange = function () {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    3,
    "cal_min",
    parseInt(this.value) + 0.5
  );
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    3,
    "cal_max",
    parseInt(this.value) + 2.5
  );
};
shaderDrop.onchange = function () {
  const shaderName = this.value;
  nv1.setMeshShader(nv1.meshes[0].id, shaderName);
};
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [0.7, 0.7, 0.7, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
nv1.opts.isColorbar = true;
var meshLHLayersList1 = [
  {
    url: "../images/BrainMesh_ICBM152.lh.curv",
    colormap: "gray",
    colormapNegative: "",
    cal_min: 0.3,
    cal_max: 0.5,
    opacity: 0.7,
  },
  {
    url: "../images/xd.mz3",
    cal_min: 2.5,
    cal_max: 4.5,
    colormap: "red",
    colormapNegative: "",
  },
  {
    url: "../images/yd.mz3",
    cal_min: 1.5,
    cal_max: 3.5,
    colormap: "green",
    colormapNegative: "",
  },
  {
    url: "../images/zd.mz3",
    cal_min: 1.5,
    cal_max: 3.5,
    colormap: "blue",
    colormapNegative: "",
  },
];
await nv1.loadMeshes([
  {
    url: "../images/BrainMesh_ICBM152.lh.mz3",
    layers: meshLHLayersList1,
  },
]);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "colorbarVisible", false);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "alphaThreshold", true);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 2, "alphaThreshold", true);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 3, "alphaThreshold", true);
nv1.setClipPlane([-0.1, 270, 0]);
shaderDrop.onchange();
additiveCheck.onchange();
opacitySlider.onchange();

	
```
</td>
</tr>
</table>

# [negative colormaps](https://niivue.github.io/niivue/features/additive.mesh.negative.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/214c6649-9a43-4f68-abad-cc80309a7596.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
additiveCheck.onchange = function () {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    1,
    "isAdditiveBlend",
    this.checked
  );
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    2,
    "isAdditiveBlend",
    this.checked
  );
};
opacitySlider.onchange = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 1, "opacity", this.value * 0.1);
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 2, "opacity", this.value * 0.1);
};
redSlider.onchange = function () {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    1,
    "cal_min",
    parseInt(this.value) + 0.5
  );
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    1,
    "cal_max",
    parseInt(this.value) + 2.5
  );
};
greenSlider.onchange = function () {
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    2,
    "cal_min",
    parseInt(this.value) + 0.5
  );
  nv1.setMeshLayerProperty(
    nv1.meshes[0].id,
    2,
    "cal_max",
    parseInt(this.value) + 2.5
  );
};
shaderDrop.onchange = function () {
  const shaderName = this.value;
  nv1.setMeshShader(nv1.meshes[0].id, shaderName);
};
var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
  backColor: [0.5, 0.5, 1, 1],
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
nv1.opts.isColorbar = true;
var meshLHLayersList1 = [
  {
    url: "../images/BrainMesh_ICBM152.lh.curv",
    colormap: "gray",
    colormapNegative: "",
    cal_min: 0.3,
    cal_max: 0.5,
    opacity: 0.7,
  },
  {
    url: "../images/yd.mz3",
    cal_min: 1.5,
    cal_max: 3.5,
    colormap: "red",
    colormapNegative: "blue",
    useNegativeCmap: true,
  },
  {
    url: "../images/zd.mz3",
    cal_min: 1.5,
    cal_max: 3.5,
    colormap: "green",
    colormapNegative: "blue",
    useNegativeCmap: true,
  },
];
await nv1.loadMeshes([
  {
    url: "../images/BrainMesh_ICBM152.lh.mz3",
    layers: meshLHLayersList1,
  },
]);
nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "colorbarVisible", false);
let v = 1;
nv1.setMeshLayerProperty(nv1.meshes[0].id, v + 0, "alphaThreshold", true);
nv1.setMeshLayerProperty(nv1.meshes[0].id, v + 1, "alphaThreshold", true);
nv1.setClipPlane([-0.1, 270, 0]);
shaderDrop.onchange();
additiveCheck.onchange();
opacitySlider.onchange();

	
```
</td>
</tr>
</table>

# [DICOM Manifest](https://niivue.github.io/niivue/features/dicom.manifest.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/b5771290-e8b0-4b40-b471-e39d30830760.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
var volumeList1 = [
  // first item is background image
  {
    url: "https://raw.githubusercontent.com/niivue/niivue-demo-images/main/dicom/niivue-manifest.txt",
    colormap: "gray",
    opacity: 1,
    visible: true,
    isManifest: true,
  },
];
var nv1 = new niivue.Niivue();
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeMultiplanar);

	
```
</td>
</tr>
</table>

# [Load a document](https://niivue.github.io/niivue/features/document.load.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/58f0e3ad-8a8b-476d-8127-fcdca520b2c6.png)



</td>
<td>

	
```javascript

CODE HERE
	
```
</td>
</tr>
</table>

# [Download a document with 3D render](https://niivue.github.io/niivue/features/document.3d.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/88a57f60-7447-48fc-94f7-7e346fac55fa.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

function toggleHippo() {
  let buttonElem = document.getElementById("toggleHippoButton");
  if (isHippoShowing) {
    nv1.removeVolumeByUrl(url);
    buttonElem.innerText = "Add Hippocampus";
    isHippoShowing = false;
  } else {
    nv1.addVolumeFromUrl({ url, colormap: "bluegrn" });
    buttonElem.innerText = "Remove Hippocampus";
    isHippoShowing = true;
  }
}

async function onButtonClick(event) {
  switch (event.target.id) {
    case "SaveDocument":
      nv1.saveDocument("niivue.basic.nvd");
      break;
    case "ToggleHippocampus":
      toggleHippo();
      break;
  }
}

const url = "../images/hippo.nii.gz";
var isHippoShowing = false;
var volumeList1 = [
  // first item is background image
  {
    url: "../images/mni152.nii.gz", //"./images/RAS.nii.gz", "./images/spm152.nii.gz",
    colormap: "gray",
    opacity: 1,
    visible: true,
  },
];
var nv1 = new niivue.Niivue();
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeRender);

var buttons = document.getElementsByClassName("viewBtn");
for (let i = 0; i < buttons.length; i++)
  buttons[i].addEventListener("click", onButtonClick, false);

	
```
</td>
</tr>
</table>

# [Download a document with drawing](https://niivue.github.io/niivue/features/document.drawing.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/55b55aad-a4a2-40dd-8b97-a1b57fa2c949.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

const isTouchDevice =
  "ontouchstart" in window ||
  navigator.maxTouchPoints > 0 ||
  navigator.msMaxTouchPoints > 0;
var isFilled = true;
function handleIntensityChange(data) {
  document.getElementById("intensity").innerHTML = "&nbsp;&nbsp;" + data.string;
}
var nv1 = new niivue.Niivue({
  logging: true,
  dragAndDropEnabled: true,
  backColor: [0, 0, 0, 1],
  show3Dcrosshair: true,
  onLocationChange: handleIntensityChange,
});
nv1.opts.isColorbar = false;
nv1.setRadiologicalConvention(false);
nv1.attachTo("gl1");
nv1.setClipPlane([0.3, 270, 0]);
nv1.setRenderAzimuthElevation(120, 10);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
nv1.setSliceMM(true);
nv1.opts.multiplanarForceRender = false;
nv1.graph.autoSizeMultiplanar = true;
nv1.graph.opacity = 1.0;
nv1.drawOpacity = 0.5;
nv1.opts.isColorbar = false;
var volumeList1 = [{ url: "../images/FLAIR.nii.gz" }];
await nv1.loadVolumes(volumeList1);
await nv1.loadDrawingFromUrl("../images/lesion.nii.gz");
function toggleGroup(id) {
  let buttons = document.getElementsByClassName("viewBtn");
  let char0 = id.charAt(0);
  for (let i = 0; i < buttons.length; i++) {
    if (buttons[i].id.charAt(0) !== char0) continue;
    buttons[i].classList.remove("dropdown-item-checked");
    if (buttons[i].id === id) buttons[i].classList.add("dropdown-item-checked");
  }
} // toggleGroup()
async function onButtonClick(event) {
  if (event.target.id === "SaveDocument") {
    nv1.saveDocument("niivue.drawing.nvd");
    return;
  }
  if (event.target.id === "SaveBitmap") {
    nv1.saveScene("ScreenShot.png");
    return;
  }
  if (event.target.id === "ShowHeader") {
    alert(nv1.volumes[0].hdr.toFormattedString());
    return;
  }
  if (event.target.id === "Colorbar") {
    nv1.opts.isColorbar = !nv1.opts.isColorbar;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
    return;
  }
  if (event.target.id === "Radiological") {
    nv1.opts.isRadiologicalConvention = !nv1.opts.isRadiologicalConvention;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
    return;
  }
  if (event.target.id === "Crosshair") {
    nv1.opts.show3Dcrosshair = !nv1.opts.show3Dcrosshair;
    event.srcElement.classList.toggle("dropdown-item-checked");
    nv1.drawScene();
  }
  if (event.target.id === "ClipPlane") {
    if (nv1.scene.clipPlaneDepthAziElev[0] > 1) nv1.setClipPlane([0.3, 270, 0]);
    else nv1.setClipPlane([2, 270, 0]);
    nv1.drawScene();
    return;
  }
  if (event.target.id.charAt(0) === "!") {
    // set color scheme
    nv1.volumes[0].colormap = event.target.id.substr(1);
    nv1.updateGLVolume();
    toggleGroup(event.target.id);
    return;
  }
  if (event.target.id === "Undo") {
    nv1.drawUndo();
  }
  if (event.target.id.charAt(0) === "@") {
    //sliceType
    if (event.target.id === "@Off") nv1.setDrawingEnabled(false);
    else nv1.setDrawingEnabled(true);
    if (event.target.id === "@Erase") nv1.setPenValue(0, isFilled);
    if (event.target.id === "@Red") nv1.setPenValue(1, isFilled);
    if (event.target.id === "@Green") nv1.setPenValue(2, isFilled);
    if (event.target.id === "@Blue") nv1.setPenValue(3, isFilled);
    if (event.target.id === "@Cluster") nv1.setPenValue(-0, isFilled);
    toggleGroup(event.target.id);
  } //Draw Color
  if (event.target.id === "Growcut") nv1.drawGrowCut();
  if (event.target.id === "Translucent") {
    if (nv1.drawOpacity > 0.75) nv1.drawOpacity = 0.5;
    else nv1.drawOpacity = 1.0;
    nv1.drawScene();
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "DrawOtsu") {
    let levels = parseInt(prompt("Segmentation classes (2..4)", "3"));
    nv1.drawOtsu(levels);
  }
  if (event.target.id === "RemoveHaze") {
    let level = parseInt(prompt("Remove Haze (1..5)", "5"));
    nv1.removeHaze(level);
  }
  if (event.target.id === "DrawFilled") {
    isFilled = !isFilled;
    nv1.setPenValue(nv1.opts.penValue, isFilled);
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "DrawOverwrite") {
    nv1.drawFillOverwrites = !nv1.drawFillOverwrites;
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id.charAt(0) === "|") {
    //sliceType
    if (event.target.id === "|Axial") nv1.setSliceType(nv1.sliceTypeAxial);
    if (event.target.id === "|Coronal") nv1.setSliceType(nv1.sliceTypeCoronal);
    if (event.target.id === "|Sagittal")
      nv1.setSliceType(nv1.sliceTypeSagittal);
    if (event.target.id === "|Render") nv1.setSliceType(nv1.sliceTypeRender);
    if (event.target.id === "|MultiPlanar") {
      nv1.opts.multiplanarForceRender = false;
      nv1.setSliceType(nv1.sliceTypeMultiplanar);
    }
    if (event.target.id === "|MultiPlanarRender") {
      nv1.opts.multiplanarForceRender = true;
      nv1.setSliceType(nv1.sliceTypeMultiplanar);
    }
    toggleGroup(event.target.id);
  } //sliceType
  if (event.target.id === "WorldSpace") {
    nv1.setSliceMM(!nv1.opts.isSliceMM);
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "Interpolate") {
    nv1.setInterpolation(!nv1.opts.isNearestInterpolation);
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id === "Left") nv1.moveCrosshairInVox(-1, 0, 0);
  if (event.target.id === "Right") nv1.moveCrosshairInVox(1, 0, 0);
  if (event.target.id === "Posterior") nv1.moveCrosshairInVox(0, -1, 0);
  if (event.target.id === "Anterior") nv1.moveCrosshairInVox(0, 1, 0);
  if (event.target.id === "Inferior") nv1.moveCrosshairInVox(0, 0, -1);
  if (event.target.id === "Superior") nv1.moveCrosshairInVox(0, 0, 1);
  if (event.target.id === "BackColor") {
    if (nv1.opts.backColor[0] < 0.5) nv1.opts.backColor = [1, 1, 1, 1];
    else nv1.opts.backColor = [0, 0, 0, 1];
    nv1.drawScene();
    event.srcElement.classList.toggle("dropdown-item-checked");
    return;
  }
  if (event.target.id.charAt(0) === "^") {
    //drag mode
    let s = event.target.id.substr(1);
    switch (s) {
      case "none":
        nv1.opts.dragMode = nv1.dragModes.none;
        break;
      case "contrast":
        nv1.opts.dragMode = nv1.dragModes.contrast;
        break;
      case "measurement":
        nv1.opts.dragMode = nv1.dragModes.measurement;
        break;
      case "pan":
        nv1.opts.dragMode = nv1.dragModes.pan;
        break;
    }
    toggleGroup(event.target.id);
  } //drag mode
  if (event.target.id === "_mesh") {
    volumeList1[0].url = "../images/mni152.nii.gz";
    await nv1.loadVolumes(volumeList1);
    nv1.loadMeshes([
      {
        url: "../images/BrainMesh_ICBM152.lh.mz3",
        rgba255: [200, 162, 255, 255],
      },
      { url: "../images/dpsv.trx", rgba255: [255, 255, 255, 255] },
    ]);
    toggleGroup(event.target.id);
  } else if (event.target.id.charAt(0) === "_") {
    //example image
    nv1.meshes = []; //close open meshes
    let root = "../images/";
    let s = event.target.id.substr(1);
    let img = root + s + ".nii.gz";
    console.log("Loading " + img);
    volumeList1[0].url = img;
    nv1.loadVolumes(volumeList1);
    toggleGroup(event.target.id);
    nv1.updateGLVolume();
  } //example image
} // onButtonClick()
var buttons = document.getElementsByClassName("viewBtn");
for (let i = 0; i < buttons.length; i++)
  buttons[i].addEventListener("click", onButtonClick, false);

	
```
</td>
</tr>
</table>

# [Download a document with meshes](https://niivue.github.io/niivue/features/document.meshes.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/7504c8e0-a431-4b19-818f-711965993d13.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";

function toggleMesh() {
  if (nv1.meshes.length === 0 && mesh) {
    nv1.addMesh(mesh);
  } else {
    mesh = nv1.meshes[0];
    nv1.removeMesh(mesh);
  }
}

async function onButtonClick(event) {
  switch (event.target.id) {
    case "SaveDocument":
      nv1.saveDocument("niivue.mesh.nvd");
      break;
    case "ToggleMesh":
      toggleMesh();
      break;
  }
}

function checkShader(id) {
  let cmapEl = document.getElementById("shadersDropDownContent");
  for (const child of cmapEl.children) {
    if (id === child.id) {
      child.classList.add("dropdown-item-checked");
    } else {
      child.classList.remove("dropdown-item-checked");
    }
  }
}

function initShaders() {
  let cmaps = nv1.meshShaderNames();
  let cmapEl = document.getElementById("shadersDropDownContent");
  for (let i = 0; i < cmaps.length; i++) {
    let buttonLink = document.createElement("a");
    buttonLink.className = "viewBtn";
    buttonLink.innerHTML = cmaps[i];
    buttonLink.id = "shader-" + i;
    buttonLink.onclick = function (event) {
      checkShader(event.srcElement.id);
      nv1.setMeshShader(nv1.meshes[0].id, cmaps[i]);
    };
    cmapEl.appendChild(buttonLink);
  }

  checkShader("shader-0");
}

var slider = document.getElementById("meshSlider");
slider.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "cal_min", this.value * 0.5);
};
var slider2 = document.getElementById("meshSlider2");
slider2.oninput = function () {
  nv1.setMeshLayerProperty(nv1.meshes[0].id, 0, "opacity", this.value * 0.1);
};

var nv1 = new niivue.Niivue({
  show3Dcrosshair: true,
});
nv1.setSliceType(nv1.sliceTypeRender);
nv1.attachTo("gl1");
var meshLHLayersList1 = [
  {
    url: "../images/BrainMesh_ICBM152.lh.motor.mz3",
    cal_min: 0.5,
    cal_max: 5.5,
    useNegativeCmap: true,
    opacity: 0.7,
  },
];
nv1.loadMeshes([
  {
    url: "../images/BrainMesh_ICBM152.lh.mz3",
    rgba255: [255, 255, 255, 255],
    layers: meshLHLayersList1,
  },
]);
nv1.setClipPlane([-0.1, 270, 0]);

var buttons = document.getElementsByClassName("viewBtn");
for (let i = 0; i < buttons.length; i++)
  buttons[i].addEventListener("click", onButtonClick, false);

initShaders();
var mesh = nv1.meshes[0];

	
```
</td>
</tr>
</table>



# [Save a scene as HTML](https://niivue.github.io/niivue/features/save.html.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 
	
![](https://pad.gwdg.de/uploads/70d8d9c5-9868-449b-bf03-553853771ce4.png)



</td>
<td>

	
```javascript

import { Niivue } from "../dist/index.js";
import { esm } from "../dist/index.min.js";

function saveAsHtml() {
  nv1.saveHTML("page.html", "gl1", decodeURIComponent(esm));
}
var volumeList1 = [
  { 
    url: "../images/mni152.nii.gz",
    colormap: "gray",
    visible: true,
    opacity: 1,
  },
  {
    url: "../images/hippo.nii.gz",
    colormap: "red",
    visible: true,
    opacity: 1,
  },
];

// assign our event handler
var button = document.getElementById("save");
button.onclick = saveAsHtml;
var nv1 = new Niivue();
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeRender);

	
```
</td>
</tr>
</table>


# [Save a scene with custom HTML](https://niivue.github.io/niivue/features/save.custom.html.html)

<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/c5c28bf8-9b25-41ae-839f-5c690d7323e8.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
import { esm } from "../dist/index.min.js";

document
  .getElementById("drawOpacity")
  .addEventListener("change", doDrawOpacity);
function doDrawOpacity() {
  nv1.setDrawOpacity(this.value * 0.01);
}
document.getElementById("drawPen").addEventListener("change", doDrawPen);
function doDrawPen() {
  const mode = parseInt(document.getElementById("drawPen").value);
  nv1.setDrawingEnabled(mode >= 0);
  if (mode >= 0) nv1.setPenValue(mode & 7, mode > 7);
  if (mode === 12)
    //erase selected cluster
    nv1.setPenValue(-0);
}
document.getElementById("left").addEventListener("click", doLeft);
function doLeft() {
  nv1.moveCrosshairInVox(-1, 0, 0);
}
document.getElementById("right").addEventListener("click", doRight);
function doRight() {
  nv1.moveCrosshairInVox(1, 0, 0);
}
document.getElementById("posterior").addEventListener("click", doPosterior);
function doPosterior() {
  nv1.moveCrosshairInVox(0, -1, 0);
}
document.getElementById("anterior").addEventListener("click", doAnterior);
function doAnterior() {
  nv1.moveCrosshairInVox(0, 1, 0);
}
document.getElementById("inferior").addEventListener("click", doInferior);
function doInferior() {
  nv1.moveCrosshairInVox(0, 0, -1);
}
document.getElementById("info").addEventListener("click", doInfo);
function doInfo() {
  let obj = nv1.getDescriptives(0, [], true);
  let str = JSON.stringify(obj, null, 2);
  alert(str);
}
document.getElementById("superior").addEventListener("click", doSuperior);
function doSuperior() {
  nv1.moveCrosshairInVox(0, 0, 1);
}
document.getElementById("undo").addEventListener("click", doUndo);
function doUndo() {
  nv1.drawUndo();
}
document.getElementById("growcut").addEventListener("click", doGrowCut);
function doGrowCut() {
  nv1.drawGrowCut();
}
document.getElementById("check1").addEventListener("change", doCheckClick);
function doCheckClick() {
  nv1.drawFillOverwrites = this.checked;
}
document.getElementById("check2").addEventListener("change", doCheck2Click);
function doCheck2Click() {
  nv1.setRadiologicalConvention(this.checked);
}
document.getElementById("check3").addEventListener("change", doCheck3Click);
function doCheck3Click() {
  nv1.setSliceMM(this.checked);
}
document.getElementById("check9").addEventListener("change", doCheck9Click);
function doCheck9Click() {
  nv1.setInterpolation(!this.checked);
}
document.getElementById("check10").addEventListener("change", doCheck10Click);
function doCheck10Click() {
  nv1.setHighResolutionCapable(this.checked);
}
var btn = document.getElementById("custom");
btn.onclick = function (event) {
  var val = document.getElementById("scriptText").value;
  val += ";nv1.setDrawColormap(cmap);";
  val && eval(val);
};
function handleLocationChange(data) {
  document.getElementById("location").innerHTML = "&nbsp;&nbsp;" + data.string;
}
function saveAsHtml() {
  const javascript = nv1.generateLoadDocumentJavaScript(
    "gl1",
    decodeURIComponent(esm)
  );
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width,initial-scale=1.0" />
  <title>Drawing</title>
  <style>
    html {
height: auto;
min-height: 100%;
margin: 0;
}
body {
display: flex;
flex-direction: column;
margin: 0;
min-height: 100%;
width: 100%;
position: absolute;
font-family: system-ui, Arial, Helvetica, sans-serif;
user-select: none; /* Standard syntax */
color: white;
background: #202020;
}
header {
margin: 10px;
}
main {
flex: 1;
background: #000000;
position: relative;
}
footer {
margin: 10px;
}
canvas {
position: absolute;
cursor: crosshair;
}
canvas:focus {
outline: 0px;
}
div {
display: table-row;
background-color: blue;
}
.dropdown {
float: left;
overflow: hidden;
}
.dropdown .dropbtn {
font-size: 16px;
border: none;
outline: none;
color: white;
padding: 12px 12px;
background-color: #202020;
font-family: inherit;
margin: 0;
}
.dropdown:hover .dropbtn {
background-color: #9a9;
}
.dropdown-content {
display: none;
position: absolute;
background-color: #303030;
min-width: 160px;
border-radius: 5px;
box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
z-index: 1;
}
.dropdown-content a {
float: none;
color: white;
padding: 12px 16px;
text-decoration: none;
display: block;
text-align: left;
line-height: 6px;
}
.dropdown-content a:hover {
background-color: #aba;
}
.dropdown:hover .dropdown-content {
display: block;
}
.dropdown-item-checked::before {
position: absolute;
left: 0.2rem;  
font-weight: 600;
}
.divider {
border-top: 1px solid grey;
}
.vertical-divider {
border-left: 1px solid grey;
height: 40px;
}
.help-text {
margin: auto;
max-width: 150px;
padding: 0 10px;
}
.slidecontainer {
padding: 10px 10px;
white-space: normal;
word-break: break-word;
display: flex;
align-items: center;
flex: 0 0 auto;
}
</style>
</head>
<body>
  <noscript>
    <strong>niivue requires JavaScript.</strong>
  </noscript>
  <header>
    <button id="save">Save as HTML</button>
    <label for="drawPen">Draw color:</label>
    <select name="drawPen" id="drawPen">
      <option value="-1">Off</option>
      <option value="0">Erase</option>
      <option value="1">Red</option>
      <option value="2">Green</option>
      <option value="3">Blue</option>
      <option value="8">Filled Erase</option>
      <option value="9">Filled Red</option>
      <option value="10">Filled Green</option>
      <option value="11">Filled Blue</option>
      <option value="12">Erase Selected Cluster</option>
    </select>
    <button id="left">left</button>
    <button id="right">right</button>
    <button id="posterior">posterior</button>
    <button id="anterior">anterior</button>
    <button id="inferior">inferior</button>
    <button id="superior">superior</button>
    <button id="info">info</button>      
    <button id="undo">undo</button>
    <button id="growcut">grow cut</button>
    <label for="drawOpacity">drawing opacity</label>
    <input
      type="range"
      min="0"
      max="100"
      value="80"
      class="slider"
      id="drawOpacity"
    />
    <label for="check1">fill pen overwrites</label>
    <input type="checkbox" id="check1" name="check1" checked />
    <label for="check2">Radiological</label>
    <input type="checkbox" id="check2" name="check2" unchecked />
    <label for="check3">World space</label>
    <input type="checkbox" id="check3" name="check3" unchecked />
    <label for="check9">Linear Interpolation</label>
    <input type="checkbox" id="check9" name="check9" checked />
    <label for="check10">HighDPI</label>
    <input type="checkbox" id="check10" name="check10" checked />
  </header>
  <main id="container">
    <canvas id="gl1"></canvas>
  </main>
  <footer>&nbsp;
    <label id="location"></label>
    <p>
    <textarea id="scriptText" name="customText" rows="8" cols="60">let cmap = {&#10; R: [0, 255, 22, 127],&#10; G: [0, 20, 192, 187],&#10; B: [0, 152, 80, 255],&#10; labels: ["clear", "pink","lime","sky"],&#10;};</textarea>
    &nbsp;<button id="custom">Apply</button>&nbsp;
  </footer>
</body>
</html>
<script type="module" async>
${javascript}
document
  .getElementById("drawOpacity")
  .addEventListener("change", doDrawOpacity);
function doDrawOpacity() {
  nv1.setDrawOpacity(this.value * 0.01);
}
document.getElementById("drawPen").addEventListener("change", doDrawPen);
function saveAsHtml() {
  saveNiivueAsHtml("niivue.drawing.html");
}
function doDrawPen() {
  const mode = parseInt(document.getElementById("drawPen").value);
  nv1.setDrawingEnabled(mode >= 0);
  if (mode >= 0) nv1.setPenValue(mode & 7, mode > 7);
  if (mode === 12)
    //erase selected cluster
    nv1.setPenValue(-0);
}
document.getElementById("left").addEventListener("click", doLeft);
function doLeft() {
  nv1.moveCrosshairInVox(-1, 0, 0);
}
document.getElementById("right").addEventListener("click", doRight);
function doRight() {
  nv1.moveCrosshairInVox(1, 0, 0);
}
document.getElementById("posterior").addEventListener("click", doPosterior);
function doPosterior() {
  nv1.moveCrosshairInVox(0, -1, 0);
}
document.getElementById("anterior").addEventListener("click", doAnterior);
function doAnterior() {
  nv1.moveCrosshairInVox(0, 1, 0);
}
document.getElementById("inferior").addEventListener("click", doInferior);
function doInferior() {
  nv1.moveCrosshairInVox(0, 0, -1);
}
document.getElementById("info").addEventListener("click", doInfo);
function doInfo() {
  let obj = nv1.getDescriptives(0, [], true);
  let str = JSON.stringify(obj, null, 2)
  alert(str);
}
document.getElementById("superior").addEventListener("click", doSuperior);
function doSuperior() {
  nv1.moveCrosshairInVox(0, 0, 1);
}
document.getElementById("undo").addEventListener("click", doUndo);
function doUndo() {
  nv1.drawUndo();
}
document.getElementById("growcut").addEventListener("click", doGrowCut);
function doGrowCut() {
  nv1.drawGrowCut();
}

document.getElementById("check1").addEventListener("change", doCheckClick);
function doCheckClick() {
  nv1.drawFillOverwrites = this.checked;
}
document.getElementById("check2").addEventListener("change", doCheck2Click);
function doCheck2Click() {
  nv1.setRadiologicalConvention(this.checked);
}
document.getElementById("check3").addEventListener("change", doCheck3Click);
function doCheck3Click() {
  nv1.setSliceMM(this.checked);
}
document.getElementById("check9").addEventListener("change", doCheck9Click);
function doCheck9Click() {
  nv1.setInterpolation(!this.checked);
}
document.getElementById("check10").addEventListener("change", doCheck10Click);
function doCheck10Click() {
  nv1.setHighResolutionCapable(this.checked);
}
var btn = document.getElementById("custom");
btn.onclick = function (event) {
  var val = document.getElementById("scriptText").value;
  val += ';nv1.setDrawColormap(cmap);';
  val && eval(val);
}
function handleLocationChange(data) {
  document.getElementById("location").innerHTML =
    "&nbsp;&nbsp;" + data.string;
}
var button = document.getElementById("save");
  button.onclick = saveAsHtml;
nv1.setRadiologicalConvention(false);
nv1.opts.multiplanarForceRender = true;  
nv1.setSliceType(nv1.sliceTypeMultiplanar);
<\/script>`;
  niivue.NVUtilities.download(html, "niivue.drawing.html", "application/html");
}

var button = document.getElementById("save");
button.onclick = saveAsHtml;
var volumeList1 = [{ url: "../images/FLAIR.nii.gz" }];
var nv1 = new niivue.Niivue({
  backColor: [1, 1, 1, 1],
  onLocationChange: handleLocationChange,
});
nv1.setRadiologicalConvention(false);
nv1.opts.multiplanarForceRender = true;
nv1.attachTo("gl1");
await nv1.loadVolumes(volumeList1);
nv1.setSliceType(nv1.sliceTypeMultiplanar);
await nv1.loadDrawingFromUrl("../images/lesion.nii.gz");

	
```

</td>
</tr>
</table>


# [Show labels](https://niivue.github.io/niivue/features/labels.html)




<table><tr><td> Image </td> <td> Code </td></tr>
<tr>
<td style="width: 500px;"> 

![](https://pad.gwdg.de/uploads/de5efb84-8d39-4228-9b00-35abf44a7dca.png)



</td>
<td>

	
```javascript

import * as niivue from "../dist/index.js";
import { esm } from "../dist/index.min.js";

function saveAsHtml() {
  nv1.saveHTML("labels.html", "gl1", decodeURIComponent(esm));
}

function setSliceType() {
  let st = parseInt(document.getElementById("sliceType").value);
  nv1.setSliceType(st);
}

var volumeList1 = [
  {
    url: "../images/mni152.nii.gz",
    colormap: "gray",
    visible: true,
    opacity: 1,
  },
  {
    url: "../images/hippo.nii.gz",
    colormap: "red",
    visible: true,
    opacity: 1,
  },
];

// assign our event handler
var button = document.getElementById("save");
button.onclick = saveAsHtml;
var drop = document.getElementById("sliceType");
drop.onchange = setSliceType;

var nv1 = new niivue.Niivue();
nv1.opts.multiplanarForceRender = true;
nv1.attachTo("gl1");
nv1.loadVolumes(volumeList1);
nv1.addLabel(
  "Insula",
  { textScale: 2.0, textAlignment: niivue.LabelTextAlignment.CENTER },
  [0.0, 0.0, 0.0]
);
nv1.addLabel(
  "ventral anterior insula",
  {
    lineWidth: 3.0,
    textColor: [1.0, 1.0, 0.0, 1.0],
    lineColor: [1.0, 1.0, 0.0, 1.0],
  },
  [
    [-33, 13, -7],
    [32, 10, -6],
  ]
);
nv1.addLabel(
  "dorsal anterior insula",
  {
    textColor: [0.0, 1.0, 0.0, 1.0],
    lineWidth: 3.0,
    lineColor: [0.0, 1.0, 0.0, 1.0],
  },
  [
    [-38, 6, 2],
    [35, 7, 3],
  ]
);
nv1.addLabel(
  "posterior insula",
  {
    textColor: [0.0, 0.0, 1.0, 1.0],
    lineWidth: 3.0,
    lineColor: [0.0, 0.0, 1.0, 1.0],
  },
  [
    [-38, -6, 5],
    [35, -11, 6],
  ]
);
nv1.addLabel(
  "hippocampus",
  { textColor: [1, 0, 0, 1], lineWidth: 3.0, lineColor: [1, 0, 0, 1] },
  [-25, -15.0, -25.0]
);
nv1.addLabel(
  "right justified footnote",
  {
    textScale: 0.5,
    textAlignment: niivue.LabelTextAlignment.RIGHT,
    bulletColor: [1.0, 0.0, 1.0, 1.0],
    bulletScale: 0.5,
  },
  [0.0, 0.0, 0.0]
);

	
```
</td>
</tr>
</table>
