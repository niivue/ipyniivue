// Copyright (c) NiiVue
// Distributed under the terms of the Modified BSD License.

//https://github.com/martinRenou/ipycanvas/blob/master/src/widget.ts for canvas functions
//Martin Renou, Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
  unpack_models
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

import * as niivue from '@niivue/niivue';

function serializeImageData(array: Uint8ClampedArray) {
  return new DataView(array.buffer.slice(0));
}

function deserializeImageData(dataview: DataView | null) {
  if (dataview === null) {
    return null;
  }
  return new Uint8ClampedArray(dataview.buffer);
}

function getContext(canvas: HTMLCanvasElement) {
  const context = canvas.getContext('webgl2');
  if (context === null) {
    throw 'Unable to get webgl2 context';
  }
  return context;
}

export class NiiVueModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: NiiVueModel.model_name,
      _model_module: NiiVueModel.model_module,
      _model_module_version: NiiVueModel.model_module_version,
      _view_name: NiiVueModel.view_name,
      _view_module: NiiVueModel.view_module,
      _view_module_version: NiiVueModel.view_module_version,
      width: 350,
      height: 250,
      sync_image_data: false,
      image_data: null,
      _send_client_ready_event: true
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

  private resizeCanvas() {
    this.canvas.setAttribute('width', this.get('width').toString());
    this.canvas.setAttribute('height', this.get('height').toString());
  }

  private setDivStyle() {
    this.div.setAttribute('style', 'width: '+this.get('width').toString()+'; height: '+this.get('height').toString()+'; background: black;');
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);

    this.div = document.createElement('div');
    this.canvas = document.createElement('canvas');
    this.div.appendChild(this.canvas);
    this.gl = getContext(this.canvas);

    this.setDivStyle();
    this.resizeCanvas();

    this.on_some_change(['width', 'height'], this.resizeCanvas, this);

    if (this.get('_send_client_ready_event')) {
      this.send({ event: 'client_ready' }, {});
    }
  }

  div: HTMLDivElement;
  canvas: HTMLCanvasElement;
  gl: WebGL2RenderingContext;
  nv: any;

  static model_name = 'NiiVueModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'NiiVueView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class NiiVueView extends DOMWidgetView {
  render() {
    this.setDivStyle();
    if (this.canvas == undefined) {
      this.canvas = document.createElement('canvas');
      this.el.appendChild(this.canvas);
    }
    if (this.nv == undefined) {
      this.nv = new niivue.Niivue({isResizeCanvas:true, logging:true});
      this.attach();
    }
    this.resizeCanvas();
    this.model.on_some_change(['width', 'height'], this.resizeCanvas, this);

  }

  protected async attach() {
    await this.nv.attachToCanvas(this.canvas);
    this.resizeCanvas();
  }

  protected setDivStyle() {
    this.el.setAttribute('style', 'width: '+this.model.get('width').toString()+'; height: '+this.model.get('height').toString()+'; background: black;');
    console.log(this.el);
  }

  protected resizeCanvas() {
    this.canvas.setAttribute('width', this.model.get('width').toString());
    this.canvas.setAttribute('height', this.model.get('height').toString());
  }

  el: HTMLDivElement;
  canvas: HTMLCanvasElement;
  nv: any;
}
