// Copyright (c) Niivue
// Distributed under the terms of the Modified BSD License.

// Much of the structure and many of the functions/classes in this file
// are from https://github.com/martinRenou/ipycanvas. NiivueModel is based off of  CanvasModel and NiivueView is based off of CanvasView.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

import * as niivue from '@niivue/niivue';

import {
  arrayBufferToBase64,
  arrayBufferToString,
  stringToArrayBuffer,
  filterNVImage,
  filterNVMesh,
} from './utils';

const setters: string[] = [
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
  'addVolumeFromBase64' //from nvimage.js
];

export class NiivueModel extends DOMWidgetModel {
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
      width: 640,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
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

  private async callNVFunctionByName(functionName: string, argsList: any[]) {
    const isAsync = this.nv[functionName].constructor.name === 'AsyncFunction';

    if (isAsync) {
      await this.nv[functionName](...argsList);
    } else {
      this.nv[functionName](...argsList);
    }
  }

  private async onCommand(command: any, buffers: DataView[]) {
    const preVolumes = this.nv.volumes.map(filterNVImage);
    const preMeshes = this.nv.meshes.map(filterNVMesh);

    console.log("onCommand:", command, buffers)
    const name: string = command[0];
    const args: any[] = command[1];
    try {
      await this.processCommand(name, args, buffers);
    } catch (e) {
      if (e instanceof Error) {
        if (
          e.name === 'TypeError' &&
          e.message ===
            "Cannot read properties of null (reading 'createTexture')"
        ) {
          console.warn(
            'Niivue widget not attached to a canvas. Display the widget to attach it to a canvas.'
          );
          return;
        }
        console.error(e);
      }
    }

    //check for changes in volumes and meshes
    const postVolumes = this.nv.volumes.map(filterNVImage);
    const postMeshes = this.nv.meshes.map(filterNVMesh);

    //push those changes to the python end. 
    //Todo: have ipyniivue.volumes and .meshes be traitlets so that changes on the python side are reflected on the ts side
    if (preVolumes !== postVolumes) {
      buffers = [];
      for (let i = 0; i < postVolumes.length; ++i) {
        buffers.push(postVolumes[i].dataBuffer || new ArrayBuffer(0));
      }
      this.send({ event: ['updateVolumes', JSON.stringify(postVolumes)] }, undefined, buffers);
    }
    if (preMeshes !== postMeshes) {
      this.send({ event: ['updateMeshes', JSON.stringify(postMeshes)] });
    }
  }

  private async processCommand(name: string, args: any[], buffers: DataView[]) {
    //if function is a sette
    if (setters.indexOf(name) > -1) {
      switch (name) {
        case 'addVolumeFromBase64':
          console.log('case addVolumeFromBase64')
          let volume = niivue.NVImage.loadFromBase64({
            name: args[0],
            base64: arrayBufferToBase64(buffers[0].buffer),
          })
            this.nv.addVolume(volume); //errors out on updateGLVolume() ...but addVolumeFromUrl() doesn't for some reason
          break;
        case 'addVolume':
            this.nv.addVolume(new niivue.NVImage(args[0]));
          break;
        case 'addMesh':
            this.nv.addMesh(new niivue.NVMesh(args[0]));
          break;
        default:
          await this.callNVFunctionByName(name, args);
          break;
      }
    }

    //else if function is a getter
    if (name == 'runCustomCode') {
        let result,
          hasResult = false;
        const code = arrayBufferToString(buffers[0].buffer);
        try {
          result = eval(code);
          hasResult = true;
        } catch (e) {
          if (e instanceof Error) {
            console.error(e.stack);
          }
        }
        this.sendCustomCodeResult(args[0], hasResult, result);
    }
  }

  private sendCustomCodeResult(id: number, hasResult: boolean, result: any) {
    let data: ArrayBuffer = new ArrayBuffer(0);
    if (hasResult) {
      const str = result === undefined ? 'undefined' : JSON.stringify(result);
      data = stringToArrayBuffer(str);
    }

    //chunk data into 5mb chunks
    const chunkSize = 5 * 1024 * 1024;
    const numChunks = Math.ceil(data.byteLength / chunkSize);
    for (let i = 0; i < numChunks; ++i) {
      const begin = i * chunkSize;
      const end = Math.min(begin + chunkSize, data.byteLength);
      const chunk = data.slice(begin, end);
      this.send({ event: ['customCodeResult', id, numChunks - 1 - i] }, undefined, [
        chunk,
      ]);
    }
    if (numChunks === 0) {
      this.send({ event: ['customCodeResult', id, 0] }, undefined);
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
      meshThicknessOn2D:
        this.get('mesh_thickness_on_2D') === 1.7976931348623157e308
          ? undefined
          : this.get('mesh_thickness_on_2D'),
      dragMode: this.get('drag_mode'),
      isDepthPickMesh: this.get('is_depth_pick_mesh'),
      isCornerOrientationText: this.get('is_corner_orientation_text'),
      sagittalNoseLeft: this.get('sagittal_nose_left'),
      isSliceMM: this.get('is_slice_MM'),
      isHighResolutionCapable: this.get('is_high_resolution_capable'),
      drawingEnabled: this.get('drawing_enabled'),
      penValue:
        this.get('pen_value') === 1.7976931348623157e308
          ? undefined
          : this.get('pen_value'),
      isFilledPen: this.get('is_filled_pen'),
      maxDrawUndoBitmaps: this.get('max_draw_undo_bitmaps'),
      thumbnail: this.get('thumbnail') || '',
    });
  }

  private currentProcessing: Promise<void> = Promise.resolve();
  nv: any;

  static model_name = 'NiivueModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'NiivueView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
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
    this.isColorbar_changed();

    this.model.on_some_change(['width', 'height'], this.resize, this);
    this.model.on('change:is_colorbar', this.isColorbar_changed, this);
  }

  //todo: add the rest of the options
  protected isColorbar_changed() {
    console.log('isColorbar_changed', this.model.get('is_colorbar'))
    this.model.nv.opts.isColorbar = this.model.get('is_colorbar')
    if (this.model.nv.gl) {
      this.model.nv.updateGLVolume();
    }
  }

  protected resize() {
    //resize div
    this.el.setAttribute('width', this.model.get('width'));
    this.el.setAttribute('height', this.model.get('height'));
    this.el.setAttribute(
      'style',
      `width: ${this.model.get('width')}px; height: ${this.model.get(
        'height'
      )}px;`
    );
    //resize canvas
    this.canvas.setAttribute('width', this.model.get('width'));
    this.canvas.setAttribute('height', this.model.get('height'));
    this.canvas.setAttribute(
      'style',
      `width: ${this.model.get('width')}px; height: ${this.model.get(
        'height'
      )};`
    );
    //redraw
    this.model.nv.drawScene();
  }

  updateCanvas() {
    this.el.appendChild(this.canvas);
    this.model.nv.attachToCanvas(this.canvas);
    this.el.style.backgroundColor = 'transparent';
  }

  el: HTMLDivElement;
  canvas: HTMLCanvasElement;
  model: NiivueModel;
}
