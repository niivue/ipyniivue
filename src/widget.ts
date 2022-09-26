// Copyright (c) anthony
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

import { Niivue } from '@niivue/niivue';

// Import the CSS
//import '../css/widget.css';

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
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'NiivueModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'NiivueView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class NiivueView extends DOMWidgetView {
  private _niivueInput: HTMLCanvasElement;

  render() {
    this._niivueInput = document.createElement('canvas');
    this.el.appendChild(this._niivueInput);
    this.el.classList.add('custom-widget');

    const nv = new Niivue();
    nv.attachToCanvas(this._niivueInput);

    this._niivueInput.height = 480;
    //this._niivueInput.width = 640;

    const volumeList = [
      {
        url: 'https://niivue.github.io/niivue/images/mni152.nii.gz',
        volume: { hdr: null, img: null },
        name: 'mni152',
        colorMap: 'freesurfer',
        opacity: 1,
        visible: true,
      },
    ];

    nv.setSliceType(nv.sliceTypeMultiplanar);
    nv.loadVolumes(volumeList);
  }
}
