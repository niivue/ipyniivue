import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

import * as niivue from '@niivue/niivue';

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
      volumes: null,

      textHeight: null,
      colorbarHeight: null,
      colorBarMargin: null,
      crosshairWidth: null,
      rulerWidth: null,
      backColor: null,
      crosshairColor: null,
      selectionBoxColor: null,
      clipPlaneColor: null,
      rulerColor: null,
      show3Dcrosshair: null,
      trustCalMinMax: null,
      clipPlaneHotKey: null,
      viewModeHotKey: null,
      keyDebounceTime: null,
      doubleTouchTimeout: null,
      longTouchTimeout: null,
      isRadiologicalConvention: null,
      logging: null,
      loadingText: null,
      dragAndDropEnabled: null,
      isNearestInterpolation: null,
      isAtlasOutline: null,
      isRuler: null,
      isColorbar: null,
      isOrientCube: null,
      multiplanarPadPixels: null,
      meshThicknessOn2D: null,
      dragMode: null,
      isDepthPickMesh: null,
      isCornerOrientationText: null,
      sagittalNoseLeft: null,
      isSliceMM: null,
      isHighResolutionCapable: null,
      drawingEnabled: null,
      penValue: null,
      isFilledPen: null,
      maxDrawUndoBitmaps: null,
      thumbnail: null,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'NiivueModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'NiivueView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

export class NiivueView extends DOMWidgetView {
  private _canvas: HTMLCanvasElement;
  private _nv: any;

  render() {
    const divEl = document.createElement('div');
    divEl.setAttribute('style', 'width: 100%; height: 400px;');
    this._canvas = document.createElement('canvas');
    divEl.appendChild(this._canvas);
    this.el.appendChild(divEl);
    this.el.classList.add('custom-widget');

    this._nv = new niivue.Niivue({ logging: true });
    this._nv.attachToCanvas(this._canvas);
    this._nv.updateGLVolume();

    //NiivueOptions
    this.textHeight_changed();
    this.colorbarHeight_changed();
    this.colorBarMargin_changed();
    this.crosshairWidth_changed();
    this.rulerWidth_changed();
    this.backColor_changed();
    this.crosshairColor_changed();
    this.selectionBoxColor_changed();
    this.clipPlaneColor_changed();
    this.rulerColor_changed();
    this.show3Dcrosshair_changed();
    this.trustCalMinMax_changed();
    this.clipPlaneHotKey_changed();
    this.viewModeHotKey_changed();
    this.keyDebounceTime_changed();
    this.doubleTouchTimeout_changed();
    this.longTouchTimeout_changed();
    this.isRadiologicalConvention_changed();
    this.logging_changed();
    this.loadingText_changed();
    this.dragAndDropEnabled_changed();
    this.isNearestInterpolation_changed();
    this.isAtlasOutline_changed();
    this.isRuler_changed();
    this.isColorbar_changed();
    this.isOrientCube_changed();
    this.multiplanarPadPixels_changed();
    this.meshThicknessOn2D_changed();
    this.dragMode_changed();
    this.isDepthPickMesh_changed();
    this.isCornerOrientationText_changed();
    this.sagittalNoseLeft_changed();
    this.isSliceMM_changed();
    this.isHighResolutionCapable_changed();
    this.drawingEnabled_changed();
    this.penValue_changed();
    this.isFilledPen_changed();
    this.maxDrawUndoBitmaps_changed();
    this.thumbnail_changed();

    this.model.on('change:text_height', this.textHeight_changed, this);
    this.model.on('change:colorbar_height', this.colorbarHeight_changed, this);
    this.model.on('change:colorbar_margin', this.colorBarMargin_changed, this);
    this.model.on('change:crosshair_width', this.crosshairWidth_changed, this);
    this.model.on('change:ruler_width', this.rulerWidth_changed, this);
    this.model.on('change:back_color', this.backColor_changed, this);
    this.model.on('change:crosshair_color', this.crosshairColor_changed, this);
    this.model.on(
      'change:selection_box_color',
      this.selectionBoxColor_changed,
      this
    );
    this.model.on('change:clip_plane_color', this.clipPlaneColor_changed, this);
    this.model.on('change:ruler_color', this.rulerColor_changed, this);
    this.model.on(
      'change:show_3D_crosshair',
      this.show3Dcrosshair_changed,
      this
    );
    this.model.on(
      'change:trust_cal_min_max',
      this.trustCalMinMax_changed,
      this
    );
    this.model.on(
      'change:clip_plane_hot_key',
      this.clipPlaneHotKey_changed,
      this
    );
    this.model.on(
      'change:view_mode_hot_key',
      this.viewModeHotKey_changed,
      this
    );
    this.model.on(
      'change:key_debounce_time',
      this.keyDebounceTime_changed,
      this
    );
    this.model.on(
      'change:double_touch_timeout',
      this.doubleTouchTimeout_changed,
      this
    );
    this.model.on(
      'change:long_touch_timeout',
      this.longTouchTimeout_changed,
      this
    );
    this.model.on(
      'change:is_radiological_convention',
      this.isRadiologicalConvention_changed,
      this
    );
    this.model.on('change:logging', this.logging_changed, this);
    this.model.on('change:loading_text', this.loadingText_changed, this);
    this.model.on(
      'change:drag_and_drop_enabled',
      this.dragAndDropEnabled_changed,
      this
    );
    this.model.on(
      'change:is_nearest_interpolation',
      this.isNearestInterpolation_changed,
      this
    );
    this.model.on('change:is_atlas_outline', this.isAtlasOutline_changed, this);
    this.model.on('change:is_ruler', this.isRuler_changed, this);
    this.model.on('change:is_colorbar', this.isColorbar_changed, this);
    this.model.on('change:is_orient_cube', this.isOrientCube_changed, this);
    this.model.on(
      'change:multiplanar_pad_pixels',
      this.multiplanarPadPixels_changed,
      this
    );
    this.model.on(
      'change:mesh_thickness_on_2D',
      this.meshThicknessOn2D_changed,
      this
    );
    this.model.on('change:drag_mode', this.dragMode_changed, this);
    this.model.on(
      'change:is_depth_pick_mesh',
      this.isDepthPickMesh_changed,
      this
    );
    this.model.on(
      'change:is_corner_orientation_text',
      this.isCornerOrientationText_changed,
      this
    );
    this.model.on(
      'change:sagittal_nose_left',
      this.sagittalNoseLeft_changed,
      this
    );
    this.model.on('change:is_slice_MM', this.isSliceMM_changed, this);
    this.model.on(
      'change:is_high_resolution_capable',
      this.isHighResolutionCapable_changed,
      this
    );
    this.model.on('change:drawing_enabled', this.drawingEnabled_changed, this);
    this.model.on('change:pen_value', this.penValue_changed, this);
    this.model.on('change:is_filled_pen', this.isFilledPen_changed, this);
    this.model.on(
      'change:max_draw_undo_bitmaps',
      this.maxDrawUndoBitmaps_changed,
      this
    );
    this.model.on('change:thumbnail', this.thumbnail_changed, this);

    //other
    this.volumes_changed();
    this.model.on('change:volumes', this.volumes_changed, this);
  }

  //NiivueOptions
  textHeight_changed() {
    this._nv.opts.textHeight = this.model.get('text_height');
    this._nv.updateGLVolume();
  }
  colorbarHeight_changed() {
    this._nv.opts.colorbarHeight = this.model.get('colorbar_height');
    this._nv.updateGLVolume();
  }
  colorBarMargin_changed() {
    this._nv.opts.colorBarMargin = this.model.get('colorbar_margin');
    this._nv.updateGLVolume();
  }
  crosshairWidth_changed() {
    this._nv.opts.crosshairWidth = this.model.get('crosshair_width');
    this._nv.updateGLVolume();
  }
  rulerWidth_changed() {
    this._nv.opts.rulerWidth = this.model.get('ruler_width');
    this._nv.updateGLVolume();
  }
  backColor_changed() {
    this._nv.opts.backColor = this.model.get('back_color');
    this._nv.updateGLVolume();
  }
  crosshairColor_changed() {
    this._nv.opts.crosshairColor = this.model.get('crosshair_color');
    this._nv.updateGLVolume();
  }
  selectionBoxColor_changed() {
    this._nv.opts.selectionBoxColor = this.model.get('selection_box_color');
    this._nv.updateGLVolume();
  }
  clipPlaneColor_changed() {
    this._nv.opts.clipPlaneColor = this.model.get('clip_plane_color');
    this._nv.updateGLVolume();
  }
  rulerColor_changed() {
    this._nv.opts.rulerColor = this.model.get('ruler_color');
    this._nv.updateGLVolume();
  }
  show3Dcrosshair_changed() {
    this._nv.opts.show3Dcrosshair = this.model.get('show_3D_crosshair');
    this._nv.updateGLVolume();
  }
  trustCalMinMax_changed() {
    this._nv.opts.trustCalMinMax = this.model.get('trust_cal_min_max');
    this._nv.updateGLVolume();
  }
  clipPlaneHotKey_changed() {
    this._nv.opts.clipPlaneHotKey = this.model.get('clip_plane_hot_key');
    this._nv.updateGLVolume();
  }
  viewModeHotKey_changed() {
    this._nv.opts.viewModeHotKey = this.model.get('view_mode_hot_key');
    this._nv.updateGLVolume();
  }
  keyDebounceTime_changed() {
    this._nv.opts.keyDebounceTime = this.model.get('key_debounce_time');
    this._nv.updateGLVolume();
  }
  doubleTouchTimeout_changed() {
    this._nv.opts.doubleTouchTimeout = this.model.get('double_touch_timeout');
    this._nv.updateGLVolume();
  }
  longTouchTimeout_changed() {
    this._nv.opts.longTouchTimeout = this.model.get('long_touch_timeout');
    this._nv.updateGLVolume();
  }
  isRadiologicalConvention_changed() {
    this._nv.opts.isRadiologicalConvention = this.model.get(
      'is_radiological_convention'
    );
    this._nv.updateGLVolume();
  }
  logging_changed() {
    this._nv.opts.logging = this.model.get('logging');
    this._nv.updateGLVolume();
  }
  loadingText_changed() {
    this._nv.opts.loadingText = this.model.get('loading_text');
    this._nv.updateGLVolume();
  }
  dragAndDropEnabled_changed() {
    this._nv.opts.dragAndDropEnabled = this.model.get('drag_and_drop_enabled');
    this._nv.updateGLVolume();
  }
  isNearestInterpolation_changed() {
    this._nv.opts.isNearestInterpolation = this.model.get(
      'is_nearest_interpolation'
    );
    this._nv.updateGLVolume();
  }
  isAtlasOutline_changed() {
    this._nv.opts.isAtlasOutline = this.model.get('is_atlas_outline');
    this._nv.updateGLVolume();
  }
  isRuler_changed() {
    this._nv.opts.isRuler = this.model.get('is_ruler');
    this._nv.updateGLVolume();
  }
  isColorbar_changed() {
    this._nv.opts.isColorbar = this.model.get('is_colorbar');
    this._nv.updateGLVolume();
  }
  isOrientCube_changed() {
    this._nv.opts.isOrientCube = this.model.get('is_orient_cube');
    this._nv.updateGLVolume();
  }
  multiplanarPadPixels_changed() {
    this._nv.opts.multiplanarPadPixels = this.model.get(
      'multiplanar_pad_pixels'
    );
    this._nv.updateGLVolume();
  }
  meshThicknessOn2D_changed() {
    this._nv.opts.meshThicknessOn2D = this.model.get('mesh_thickness_on_2D');
    this._nv.updateGLVolume();
  }
  dragMode_changed() {
    this._nv.opts.dragMode = this.model.get('drag_mode');
    this._nv.updateGLVolume();
  }
  isDepthPickMesh_changed() {
    this._nv.opts.isDepthPickMesh = this.model.get('is_depth_pick_mesh');
    this._nv.updateGLVolume();
  }
  isCornerOrientationText_changed() {
    this._nv.opts.isCornerOrientationText = this.model.get(
      'is_corner_orientation_text'
    );
    this._nv.updateGLVolume();
  }
  sagittalNoseLeft_changed() {
    this._nv.opts.sagittalNoseLeft = this.model.get('sagittal_nose_left');
    this._nv.updateGLVolume();
  }
  isSliceMM_changed() {
    this._nv.opts.isSliceMM = this.model.get('is_slice_MM');
    this._nv.updateGLVolume();
  }
  isHighResolutionCapable_changed() {
    this._nv.opts.isHighResolutionCapable = this.model.get(
      'is_high_resolution_capable'
    );
    this._nv.updateGLVolume();
  }
  drawingEnabled_changed() {
    this._nv.opts.drawingEnabled = this.model.get('drawing_enabled');
    this._nv.updateGLVolume();
  }
  penValue_changed() {
    this._nv.opts.penValue = this.model.get('pen_value');
    this._nv.updateGLVolume();
  }
  isFilledPen_changed() {
    this._nv.opts.isFilledPen = this.model.get('is_filled_pen');
    this._nv.updateGLVolume();
  }
  maxDrawUndoBitmaps_changed() {
    this._nv.opts.maxDrawUndoBitmaps = this.model.get('max_draw_undo_bitmaps');
    this._nv.updateGLVolume();
  }
  thumbnail_changed() {
    this._nv.opts.thumbnail = this.model.get('thumbnail');
    this._nv.updateGLVolume();
  }

  //other
  volumes_changed() {
    console.log(this.model.get('volumes'));
    this._nv.loadVolumes(this.model.get('volumes'));
  }
}
