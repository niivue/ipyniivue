// Copyright (c) NiiVue
// Distributed under the terms of the Modified BSD License.

//Much of the structure and many of the functions/classes in this file
//are from https://github.com/martinRenou/ipycanvas. NiivueModel comes from CanvasModel and NiivueView comes from CanvasView.
//The main difference is the use of NiiVue and setting NiivueView's tagname to be a div.

import {
  WidgetModel,
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
  unpack_models
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

import * as niivue from '@niivue/niivue';

function getContext(canvas: HTMLCanvasElement) {
  const context = canvas.getContext('webgl2');
  if (context === null) {
    throw 'Unable to get webgl2 context.';
  }
  return context;
}

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
    console.log('onCommand CanvasManagerModel', command, buffers);
  }

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

    this.canvas = document.createElement('canvas');
    this.gl = getContext(this.canvas);

    this.drawImageData();
    this.resizeCanvas();

    this.on_some_change(['width', 'height'], this.resizeCanvas, this);
  }

  private resizeCanvas() {
    this.canvas.setAttribute('width', this.get('width'));
    this.canvas.setAttribute('height', this.get('height'));
    this.canvas.setAttribute('style', `width: ${this.get('width')}px; height: ${this.get('height')};`);
  }

  private async drawImageData() {
    this.nv = new niivue.Niivue({ isResizeCanvas: false, logging: true });
  }

  static model_name = 'NiivueModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'NiivueView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;

  canvas: HTMLCanvasElement;
  gl: WebGL2RenderingContext;
  nv: any;
}

export class NiivueView extends DOMWidgetView {
  //for changing things / listening to callbacks
  render() {
    this.updateCanvas();
    this.resizeDiv();

    this.value_changed();
    this.model.on('change:value', this.value_changed, this);
  }

  protected resizeDiv() {
    this.el.setAttribute('width', this.model.get('width'));
    this.el.setAttribute('height', this.model.get('height'));
    this.el.setAttribute('style', `width: ${this.model.get('width')}px; height: ${this.model.get('height')}px;`);
  }

  updateCanvas() {
    this.el.appendChild(this.model.canvas);
    this.model.nv.attachToCanvas(this.model.canvas);
  }

  value_changed() {
    this.model.nv.loadVolumes([{url: this.model.get("value")}]);
  }

  //this makes this.el become a custom tag
  preinitialize() {
    this.tagName = 'div';
  }

  el: HTMLDivElement;
  canvas: HTMLCanvasElement;
  model: NiivueModel;
}
