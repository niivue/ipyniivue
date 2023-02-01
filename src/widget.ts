// Copyright (c) NiiVue
// Distributed under the terms of the Modified BSD License.

//Much of the structure and many of the functions/classes in this file
//are from https://github.com/martinRenou/ipycanvas. NiivueModel is based off of  CanvasModel and NiivueView is based off of CanvasView.

import * as niivue from '@niivue/niivue';
import { arrayBufferToBase64 } from './utils';

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
  unpack_models
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

import "../css/styles.css"

const COMMANDS = [
  'saveScene', 
  'addVolumeFromUrl', 
  'removeVolumeByUrl', 
  'setCornerOrientationText', 
  'setRadiologicalConvention', 
  'setMeshThicknessOn2D', 
  'setSliceMosaicString', 
  'setSliceMM', 
  'setHighResolutionCapable', 
  'addVolume', 
  'addMesh', 
  'drawUndo', 
  'loadDrawingFromUrl', 
  'drawOtsu', 
  'removeHaze', 
  'saveImage', 
  'setMeshProperty', 
  'reverseFaces', 
  'setMeshLayerProperty', 
  'setPan2Dxyzmm', 
  'setRenderAzimuthElevation', 
  'setVolume', 
  'removeVolume', 
  'removeVolumeByIndex', 
  'removeMesh', 
  'removeMeshByUrl', 
  'moveVolumeToBottom', 
  'moveVolumeUp', 
  'moveVolumeDown', 
  'moveVolumeToTop', 
  'setClipPlane', 
  'setCrosshairColor', 
  'setCrosshairWidth', 
  'setDrawingEnabled', 
  'setPenValue', 
  'setDrawOpacity', 
  'setSelectionBoxColor', 
  'setSliceType', 
  'setOpacity', 
  'setScale', 
  'setClipPlaneColor', 
  'loadDocumentFromUrl', 
  'loadVolumes', 
  'addMeshFromUrl', 
  'loadMeshes', 
  'loadConnectome', 
  'createEmptyDrawing', 
  'drawGrowCut', 
  'setMeshShader', 
  'setCustomMeshShader', 
  'updateGLVolume', 
  'setColorMap', 
  'setColorMapNegative', 
  'setModulationImage', 
  'setFrame4D', 
  'setInterpolation', 
  'moveCrosshairInVox', 
  'drawMosaic',
  'addVolumeFromBase64'
];

function serializeImageData(array: Uint8ClampedArray) {
  return new DataView(array.buffer.slice(0));
}

function deserializeImageData(dataview: DataView | null) {
  if (dataview === null) {
    return null;
  }

  return new Uint8ClampedArray(dataview.buffer);
}

export class NiivueModel extends DOMWidgetModel {
  //for drawing things
  defaults() {
    return {
      ...super.defaults(),
      _model_name: NiivueModel.model_name,
      _model_module: NiivueModel.model_module,
      _model_module_version: NiivueModel.model_module_version,
      _view_name: NiivueModel.view_name,
      _view_module: NiivueModel.view_module,
      _view_module_version: NiivueModel.view_module_version,
      height: 480,
      width: 640
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    _canvas_manager: { deserialize: unpack_models as any },
    image_data: {
      serialize: serializeImageData,
      deserialize: deserializeImageData
    }
  };

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
  
    this.on('msg:custom', (command: any, buffers: any) => {
      this.currentProcessing = this.currentProcessing.then(async () => {
        await this.onCommand(command, buffers);
      });
    });
    
    this.createNV();
  }

  private async onCommand(command: any, buffers: DataView[]) {
    const name: string = COMMANDS[command[0]];
    const args: any[] = command[1];
    switch(name) {
      case 'saveScene':
        this.nv.saveScene(args[0]);
        break;
      case 'addVolumeFromUrl':
        this.nv.addVolumeFromUrl({url: args[0]});
        break;
      case 'removeVolumeByUrl':
        this.nv.removeVolumeByUrl(args[0]);
        break;
      case 'setCornerOrientationText':
        this.nv.setCornerOrientationText(args[0]);
        break;
      case 'setRadiologicalConvention':
        this.nv.setRadiologicalConvention(args[0]);
        break;
      case 'setMeshThicknessOn2D':
        this.nv.setMeshThicknessOn2D(args[0]);
        break;
      case 'setSliceMosaicString':
        this.nv.setSliceMosaicString(args[0]);
        break;
      case 'setSliceMM':
        this.nv.setSliceMM(args[0]);
        break;
      case 'setHighResolutionCapable':
        this.nv.setHighResolutionCapable(args[0]);
        break;
      case 'addVolume':
        this.nv.addVolume(args[0]);
        break;
      case 'addMesh':
        this.nv.addMesh(args[0]);
        break;
      case 'drawUndo':
        this.nv.drawUndo();
        break;
      case 'loadDrawingFromUrl':
        this.nv.loadDrawingFromUrl(args[0]);
        break;
      case 'drawOtsu':
        this.nv.drawOtsu(args[0]);
        break;
      case 'removeHaze':
        this.nv.removeHaze(args[0], args[1]);
        break;
      case 'saveImage':
        this.nv.saveImage(args[0], args[1]);
        break;
      case 'setMeshProperty':
        this.nv.setMeshProperty(args[0], args[1], args[2]);
        break;
      case 'reverseFaces':
        this.nv.reverseFaces(args[0]);
        break;
      case 'setMeshLayerProperty':
        this.nv.setMeshLayerProperty(args[0], args[1], args[2], args[3]);
        break;
      case 'setPan2Dxyzmm':
        this.nv.setPan2Dxyzmm(args[0]);
        break;
      case 'setRenderAzimuthElevation':
        this.nv.setRenderAzimuthElevation(args[0], args[1]);
        break;
      case 'setVolume':
        this.nv.setVolume(args[0], args[1]);
        break;
      case 'removeVolume':
        this.nv.removeVolume(args[0]);
        break;
      case 'removeVolumeByIndex':
        this.nv.removeVolumeByIndex(args[0]);
        break;
      case 'removeMesh':
        this.nv.removeMesh(args[0]);
        break;
      case 'removeMeshByUrl':
        this.nv.removeMeshByUrl(args[0]);
        break;
      case 'moveVolumeToBottom':
        this.nv.moveVolumeToBottom(args[0]);
        break;
      case 'moveVolumeUp':
        this.nv.moveVolumeUp(args[0]);
        break;
      case 'moveVolumeDown':
        this.nv.moveVolumeDown(args[0]);
        break;
      case 'moveVolumeToTop':
        this.nv.moveVolumeToTop(args[0]);
        break;
      case 'setClipPlane':
        this.nv.setClipPlane(args[0]);
        break;
      case 'setCrosshairColor':
        this.nv.setCrosshairColor(args[0]);
        break;
      case 'setCrosshairWidth':
        this.nv.setCrosshairWidth(args[0]);
        break;
      case 'setDrawingEnabled':
        this.nv.setDrawingEnabled(args[0]);
        break;
      case 'setPenValue':
        this.nv.setPenValue(args[0], args[1]);
        break;
      case 'setDrawOpacity':
        this.nv.setDrawOpacity(args[0]);
        break;
      case 'setSelectionBoxColor':
        this.nv.setSelectionBoxColor(args[0]);
        break;
      case 'setSliceType':
        this.nv.setSliceType(args[0]);
        break;
      case 'setOpacity':
        this.nv.setOpacity(args[0], args[1]);
        break;
      case 'setScale':
        this.nv.setScale(args[0]);
        break;
      case 'setClipPlaneColor':
        this.nv.setClipPlaneColor(args[0]);
        break;
      case 'loadDocumentFromUrl':
        this.nv.loadDocumentFromUrl(args[0]);
        break;
      case 'loadVolumes':
        this.nv.loadVolumes(args[0]);
        break;
      case 'addMeshFromUrl':
        this.nv.addMeshFromUrl(args[0]);
        break;
      case 'loadMeshes':
        this.nv.loadMeshes(args[0]);
        break;
      case 'loadConnectome':
        this.nv.loadConnectome(args[0]);
        break;
      case 'createEmptyDrawing':
        this.nv.createEmptyDrawing();
        break;
      case 'drawGrowCut':
        this.nv.drawGrowCut();
        break;
      case 'setMeshShader':
        this.nv.setMeshShader(args[0], args[1]);
        break;
      case 'setCustomMeshShader':
        this.nv.setCustomMeshShader(args[0], args[1]);
        break;
      case 'updateGLVolume':
        this.nv.updateGLVolume();
        break;
      case 'setColorMap':
        this.nv.setColorMap(args[0], args[1]);
        break;
      case 'setColorMapNegative':
        this.nv.setColorMapNegative(args[0], args[1]);
        break;
      case 'setModulationImage':
        this.nv.setModulationImage(args[0], args[1], args[2]);
        break;
      case 'setFrame4D':
        this.nv.setFrame4D(args[0], args[1]);
        break;
      case 'setInterpolation':
        this.nv.setInterpolation(args[0]);
        break;
      case 'moveCrosshairInVox':
        this.nv.moveCrosshairInVox(args[0], args[1], args[2]);
        break;
      case 'drawMosaic':
        this.nv.drawMosaic(args[0]);
        break;
      case 'addVolumeFromBase64':
        this.nv.addVolume(niivue.NVImage.loadFromBase64({name: args[0], base64: arrayBufferToBase64(buffers[0].buffer)}));
        break;
    }
  }

  private async createNV() {
    this.nv = new niivue.Niivue({ 
      isResizeCanvas: false, 
      logging: true,

      textHeight: this.get('text_height'),
      colorbarHeight: this.get('colorbar_height'),
      colorbarMargin: this.get('colorbar_margin'),
      crosshairWidth: this.get('crosshair_width'),
      rulerWidth: this.get('ruler_width'),
      backColor: this.get('back_color'),
      crosshairColor: this.get('crosshair_color'),
      fontColor: this.get('font_color'),
      selectionBoxColor: this.get('selection_box_color'),
      clipPlaneColor: this.get('clip_plane_color'),
      rulerColor: this.get('ruler_color'),
      show3Dcrosshair: this.get('show_3D_crosshair'),
      trustCalMinMax: this.get('trust_cal_min_max'),
      clipPlaneHotKey: this.get('clip_plane_hot_key'),
      viewModeHotKey: this.get('view_mode_hot_key'),
      keyDebounceTime: this.get('key_debounce_time'),
      doubleTouchTimeout: this.get('double_touch_timeout'),
      longTouchTimeout: this.get('long_touch_timeout'),
      isRadiologicalConvention: this.get('is_radiological_convention'),
      loadingText: this.get('loading_text'),
      dragAndDropEnabled: this.get('drag_and_drop_enabled'),
      isNearestInterpolation: this.get('is_nearest_interpolation'),
      isAtlasOutline: this.get('is_atlas_outline'),
      isRuler: this.get('is_ruler'),
      isColorbar: this.get('is_colorbar'),
      isOrientCube: this.get('is_orient_cube'),
      multiplanarPadPixels: this.get('multiplanar_pad_pixels'),
      multiplanarForceRender: this.get('multiplanar_force_render'),
      meshThicknessOn2D: this.get('mesh_thickness_on_2D') == 1.7976931348623157e+308 ? undefined : this.get('mesh_thickness_on_2D'),
      dragMode: this.get('drag_mode'),
      isDepthPickMesh: this.get('is_depth_pick_mesh'),
      isCornerOrientationText: this.get('is_corner_orientation_text'),
      sagittalNoseLeft: this.get('sagittal_nose_left'),
      isSliceMM: this.get('is_slice_MM'),
      isHighResolutionCapable: this.get('is_high_resolution_capable'),
      drawingEnabled: this.get('drawing_enabled'),
      penValue: this.get('pen_value') == 1.7976931348623157e+308 ? undefined : this.get('pen_value'),
      isFilledPen: this.get('is_filled_pen'),
      maxDrawUndoBitmaps: this.get('max_draw_undo_bitmaps'),
      thumbnail: this.get('thumbnail')
    });
  }

  static model_name = 'NiivueModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'NiivueView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;

  private currentProcessing: Promise<void> = Promise.resolve();
  nv: any;
}

export class NiivueView extends DOMWidgetView {
  //for changing things / listening to callbacks
  render() {
    //reason for canvas creation being in here is 2-fold
    //1) NiivueVIEW
    //2) https://ipywidgets.readthedocs.io/en/7.7.0/examples/Widget%20Low%20Level.html#Models-and-Views
    //   "Multiple WidgetViews can be linked to a single WidgetModel. This is how you can redisplay the same Widget multiple times and it still works."    
    this.canvas = document.createElement('canvas');
    this.canvas.classList.add('niivue-widget');

    this.resize();
    this.updateCanvas();
    //this.value_changed();

    this.model.on_some_change(['width', 'height'], this.resize, this);
    //this.model.on('change:value', this.value_changed, this);
  }

  protected resize() {
    //resize div
    this.el.setAttribute('width', this.model.get('width'));
    this.el.setAttribute('height', this.model.get('height'));
    this.el.setAttribute('style', `width: ${this.model.get('width')}px; height: ${this.model.get('height')}px;`);
    //resize canvas
    this.canvas.setAttribute('width', this.model.get('width'));
    this.canvas.setAttribute('height', this.model.get('height'));
    this.canvas.setAttribute('style', `width: ${this.model.get('width')}px; height: ${this.model.get('height')};`);
    //redraw
    this.model.nv.drawScene();
  }

  updateCanvas() {
    this.el.appendChild(this.canvas);
    this.model.nv.attachToCanvas(this.canvas);
    this.el.style.backgroundColor = 'transparent';
  }

  //proof of concept - can have updates from variable changes
  value_changed() {
    this.model.nv.loadVolumes([{url: this.model.get("value")}]);
  }

  //this makes this.el become a custom tag (div in this case). Technically this is not necessary.
  preinitialize() {
    this.tagName = 'div';
  }

  el: HTMLDivElement;
  canvas: HTMLCanvasElement;
  model: NiivueModel;
}
