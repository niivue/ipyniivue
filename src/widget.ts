// Copyright (c) NiiVue
// Distributed under the terms of the Modified BSD License.

//Much of the structure and many of the functions/classes in this file
//are from https://github.com/martinRenou/ipycanvas. NiivueModel is based off of  CanvasModel and NiivueView is based off of CanvasView.

import { Buffer } from 'buffer';

import {
  WidgetModel,
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
  unpack_models
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

import {
  getTypedArray
} from './utils';

import "../css/styles.css";

import * as niivue from '@niivue/niivue';

const COMMANDS = [
  'setNiivue',
  'setClipPlane'
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

export class CanvasManagerModel extends WidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: CanvasManagerModel.model_name,
      _model_module: CanvasManagerModel.model_module,
      _model_module_version: CanvasManagerModel.model_module_version
    };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);

    this.on('msg:custom', (command: any, buffers: any) => {
      this.currentProcessing = this.currentProcessing.then(async () => {
        await this.onCommand(command, buffers);
      });
    });
  }

  private async onCommand(command: any, buffers: any) {
    const cmd = JSON.parse(
      Buffer.from(getTypedArray(buffers[0], command)).toString('utf-8')
    );
    console.log('onCommand CanvasManagerModel', cmd);
    await this.processCommand(cmd, buffers.slice(1, buffers.length));
  }

  private async processCommand(command: any, buffers: any) {
    const name: string = COMMANDS[command[0]];
    const args: any[] = command[1];
    switch(name) {
      case "setNiivue":
        console.log('await this.setNiivue(', args, ')');
      case "setClipPlane":
        console.log('this.currentNiivue.nv.setClipPlane(', args, ')');
    }
  }

  /*
  private async setNiivue(serializedNiivue: any) {
    this.currentNiivue = await unpack_models(
      serializedNiivue,
      this.widget_manager
    );
  }
  */

  //private currentNiivue: NiivueModel;
  private currentProcessing: Promise<void> = Promise.resolve();

  static model_name = 'CanvasManagerModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
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
    
    this.createNV();
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

    this.resize();
    this.updateCanvas();
    this.value_changed();

    this.model.on_some_change(['width', 'height'], this.resize, this);
    this.model.on('change:value', this.value_changed, this);
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
  }

  value_changed() {
    this.model.nv.loadVolumes([{url: this.model.get("value")}]);
  }

  //this makes this.el become a custom tag (div in this case)
  preinitialize() {
    this.tagName = 'div';
  }

  el: HTMLDivElement;
  canvas: HTMLCanvasElement;
  model: NiivueModel;
}
