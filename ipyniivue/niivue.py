#!/usr/bin/env python
# coding: utf-8

# Copyright (c) NiiVue.
# Distributed under the terms of the Modified BSD License.

#Much of the structure and many of the functions/classes in this file
#are from https://github.com/martinRenou/ipycanvas. The Niivue class is based off of Canvas class.

"""
TODO: Add module docstring
"""

import pathlib

from traitlets import (
    Unicode, 
    CInt,
    CFloat,
    List,
    Bool, 
    UseEnum,
    CaselessStrEnum
)
from .traits import ( 
    DragModes, 
    keycodes
)
from ._frontend import module_name, module_version
from ipywidgets import (
    DOMWidget
)

_CMD_LIST = [
    "saveScene", 
    "addVolumeFromUrl", 
    "removeVolumeByUrl", 
    "setCornerOrientationText", 
    "setRadiologicalConvention", 
    "setMeshThicknessOn2D", 
    "setSliceMosaicString", 
    "setSliceMM", 
    "setHighResolutionCapable", 
    "addVolume", 
    "addMesh", 
    "drawUndo", 
    "loadDrawingFromUrl", 
    "drawOtsu", 
    "removeHaze", 
    "saveImage", 
    "setMeshProperty", 
    "reverseFaces", 
    "setMeshLayerProperty", 
    "setPan2Dxyzmm", 
    "setRenderAzimuthElevation", 
    "setVolume", 
    "removeVolume", 
    "removeVolumeByIndex", 
    "removeMesh", 
    "removeMeshByUrl", 
    "moveVolumeToBottom", 
    "moveVolumeUp", 
    "moveVolumeDown", 
    "moveVolumeToTop", 
    "setClipPlane", 
    "setCrosshairColor", 
    "setCrosshairWidth", 
    "setDrawingEnabled", 
    "setPenValue", 
    "setDrawOpacity", 
    "setSelectionBoxColor", 
    "setSliceType", 
    "setOpacity", 
    "setScale", 
    "setClipPlaneColor", 
    "loadDocumentFromUrl", 
    "loadVolumes", 
    "addMeshFromUrl", 
    "loadMeshes", 
    "loadConnectome", 
    "createEmptyDrawing", 
    "drawGrowCut", 
    "setMeshShader", 
    "setCustomMeshShader", 
    "updateGLVolume", 
    "setColorMap", 
    "setColorMapNegative", 
    "setModulationImage", 
    "setFrame4D", 
    "setInterpolation", 
    "moveCrosshairInVox", 
    "drawMosaic",
    "addVolumeFromBase64"
]
COMMANDS = {v: i for i, v in enumerate(_CMD_LIST)}

def read_file(file):
    try:
        with open(file, 'rb') as f:
            return f.read()
    except FileNotFoundError as error: 
        raise error

class _CanvasBase(DOMWidget):
    """
    Args
    ----
        height (int): The height (in pixels) of the canvas
        width (int): The width (in pixels) of the canvas
    """
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    height = CInt(480).tag(sync=True)
    width = CInt(640).tag(sync=True)

class Niivue(_CanvasBase):
    """Niivue class.
    
    Args
    ----
    text_height: float, default 0.06
        the text height for orientation labels (0 to 1). Zero for no text labels
    colorbar_height: float, default 0.05
        size of colorbar. 0 for no colorbars, fraction of Nifti j dimension
    colorbar_margin: float, default 0.05
        padding around colorbar when displayed
    crosshair_width: float, default 1
        crosshair size. Zero for no crosshair
    ruler_width: float, default 4
        ruler size. 0 for no ruler
    back_color: list, default [0,0,0,1]
        the background color. RGBA values from 0 to 1. Default is black
    crosshair_color: list, default [1,0,0,1]
        the crosshair color. RGBA values from 0 to 1. Default is red
    selection_box_color: list, default [1,1,1,0.5]
        the selection box color when the intensty selection box is shown (right click and drag). RGBA values from 0 to 1. Default is transparent white
    clip_plane_color: list, default [1,1,1,0.5]
        the color of the visible clip plane. RGBA values from 0 to 1. Default is white
    ruler_color: list, default [1, 0, 0, 0.8]
        the color of the ruler. RGBA values from 0 to 1. Default is translucent red
    show_3D_crosshair: bool, default False
        True/False whether crosshairs are shown on 3D rendering
    trust_cal_min_max: bool, default True
        True/False whether to trust the nifti header values for cal_min and cal_max. Trusting them results in faster loading because we skip computing these values from the data
    clip_plane_hot_key: str, default "KeyC"
        the keyboard key used to cycle through clip plane orientations
    view_mode_hot_key: str, default "KeyV"
        the keyboard key used to cycle through view modes
    key_debounce_time: float, default 50
        the keyUp debounce time in milliseconds. The default is 50 ms. You must wait this long before a new hot-key keystroke will be registered by the event listener
    double_touch_timeout: float, default 500
        the maximum time in milliseconds for a double touch to be detected. The default is 500 ms
    long_touch_timeout: float, default 1000
        the minimum time in milliseconds for a touch to count as long touch. The default is 1000 ms
    is_radiological_convention: bool, default False
        whether or not to use radiological convention in the display
    loading_text: str, default "waiting on images..."
        the loading text to display when there is a blank canvas and no images
    drag_and_drop_enabled: bool, default True
        whether or not to allow file and url drag and drop on the canvas
    is_nearest_interpolation: bool, default False
        whether nearest neighbor interpolation is used, else linear interpolation
    is_atlas_outline: bool, default False
        whether atlas maps are only visible at the boundary of regions
    is_ruler: bool, default False
        whether a 10cm ruler is displayed
    is_colorbar: bool, default False
        whether colorbar(s) are shown illustrating values for color maps
    is_orient_cube: bool, default False
        whether orientation cube is shown for 3D renderings
    multiplanar_pad_pixels: int, default 0
        spacing between tiles of a multiplanar view
    mesh_thickness_on_2D: float, default Infinity
        2D slice views can show meshes within this range. Meshes only visible in sliceMM (world space) mode
    drag_mode: str/int, default "contrast"/1
        behavior for dragging
        string ("none", "contrast", "measurement", "pan") or int (0, 1, 2, 3)
    is_depth_pick_mesh: bool, default False
        when both voxel-based image and mesh is loaded, will depth picking be able to detect mesh or only voxels
    is_corner_orientation_text: bool, default False
        should slice text be shown in the upper right corner instead of the center of left and top axes?
    sagittal_nose_left: bool, default False
        should 2D sagittal slices show the anterior direction toward the left or right?
    is_slice_MM: bool, default False
        are images aligned to voxel space (False) or world space (True)
    is_high_resolution_capable: bool, default True
        demand that high-dot-per-inch displays use native voxel size
    drawing_enabled: bool, default False
        allow user to create and edit voxel-based drawings
    pen_value: float, default Infinity
        color of drawing when user drags mouse (if drawing_enabled)
    is_filled_pen: bool, default False
        create filled drawings when user drags mouse (if drawing_enabled)
    max_draw_undo_bitmaps: int, default 8
        number of possible undo steps (if drawing_enabled)
    thumbnail: str, default ""
        optional 2D png bitmap that can be rapidly loaded to defer slow loading of 3D image
    """

    _model_name = Unicode("NiivueModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("NiivueView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode("").tag(sync=True)

    #NiivueOptions
    text_height = CFloat(default_value = 0.06, help="the text height for orientation labels (0 to 1). Zero for no text labels").tag(sync=True)
    colorbar_height = CFloat(default_value = 0.05, help="size of colorbar. 0 for no colorbars, fraction of Nifti j dimension").tag(sync=True)
    colorbar_margin = CFloat(default_value = 0.05, help="padding around colorbar when displayed").tag(sync=True)
    crosshair_width = CFloat(default_value = 1, help="crosshair size. Zero for no crosshair").tag(sync=True)
    ruler_width = CFloat(default_value = 4, help="ruler size. 0 for no ruler").tag(sync=True)
    back_color = List(trait=CFloat(), default_value = [0, 0, 0, 1], help="the background color. RGBA values from 0 to 1. Default is black").tag(sync=True, min_len=4, max_len=4)
    crosshair_color = List(trait=CFloat(), default_value = [1, 0, 0, 1], help="the crosshair color. RGBA values from 0 to 1. Default is red").tag(sync=True, min_len=4, max_len=4)
    font_color = List(trait=CFloat(), default_value = [0.5, 0.5, 0.5, 1], help="the font color. RGBA values from 0 to 1. Default is gray").tag(sync=True, min_len=4, max_len=4)
    selection_box_color = List(trait=CFloat(), default_value = [1, 1, 1, 0.5], help="the selection box color when the intensty selection box is shown (right click and drag). RGBA values from 0 to 1. Default is transparent white").tag(sync=True, min_len=4, max_len=4)
    clip_plane_color = List(trait=CFloat(), default_value = [1, 1, 1, 0.5], help="the color of the visible clip plane. RGBA values from 0 to 1. Default is white").tag(sync=True, min_len=4, max_len=4)
    ruler_color = List(trait=CFloat(), default_value = [1, 0, 0, 0.8], help="the color of the ruler. RGBA values from 0 to 1. Default is translucent red").tag(sync=True, min_len=4, max_len=4)
    show_3D_crosshair = Bool(default_value = False, help="True/False whether crosshairs are shown on 3D rendering").tag(sync=True)
    trust_cal_min_max = Bool(default_value = True, help="True/False whether to trust the nifti header values for cal_min and cal_max. Trusting them results in faster loading because we skip computing these values from the data").tag(sync=True)
    clip_plane_hot_key = CaselessStrEnum(keycodes, default_value="KeyC", help="the keyboard key used to cycle through clip plane orientations").tag(sync=True)
    view_mode_hot_key = CaselessStrEnum(keycodes, default_value="KeyV", help="the keyboard key used to cycle through view modes").tag(sync=True)
    key_debounce_time = CFloat(default_value = 50, help="the keyUp debounce time in milliseconds. The default is 50 ms. You must wait this long before a new hot-key keystroke will be registered by the event listener").tag(sync=True)
    double_touch_timeout = CFloat(default_value = 500, help="the maximum time in milliseconds for a double touch to be detected. The default is 500 ms").tag(sync=True)
    long_touch_timeout = CFloat(default_value = 1000, help="the minimum time in milliseconds for a touch to count as long touch. The default is 1000 ms").tag(sync=True)
    is_radiological_convention = Bool(default_value = False, help="whether or not to use radiological convention in the display").tag(sync=True)
    loading_text = Unicode(default_value = "waiting on images...", help="the loading text to display when there is a blank canvas and no images").tag(sync=True)
    drag_and_drop_enabled = Bool(default_value = True, help="whether or not to allow file and url drag and drop on the canvas").tag(sync=True)
    is_nearest_interpolation = Bool(default_value = False, help="whether nearest neighbor interpolation is used, else linear interpolation").tag(sync=True)
    is_atlas_outline = Bool(default_value = False, help="whether atlas maps are only visible at the boundary of regions").tag(sync=True)
    is_ruler = Bool(default_value = False, help="whether a 10cm ruler is displayed").tag(sync=True)
    is_colorbar = Bool(default_value = False, help="whether colorbar(s) are shown illustrating values for color maps").tag(sync=True)
    is_orient_cube = Bool(default_value = False, help="whether orientation cube is shown for 3D renderings").tag(sync=True)
    multiplanar_pad_pixels = CInt(default_value = 0, help="spacing between tiles of a multiplanar view").tag(sync=True)
    multiplanar_force_render = Bool(default_value = False, help="always show rendering in multiplanar view").tag(sync=True)
    mesh_thickness_on_2D = CFloat(default_value = 1.7976931348623157e+308, help="2D slice views can show meshes within this range. Meshes only visible in slice_MM (world space) mode").tag(sync=True)
    drag_mode = UseEnum(DragModes, default_value=DragModes.contrast, help="behavior for dragging (\"none\", \"contrast\", \"measurement\", \"pan\")").tag(sync=True)
    is_depth_pick_mesh = Bool(default_value = False, help="when both voxel-based image and mesh is loaded, will depth picking be able to detect mesh or only voxels").tag(sync=True)
    is_corner_orientation_text = Bool(default_value = False, help="should slice text be shown in the upper right corner instead of the center of left and top axes?").tag(sync=True)
    sagittal_nose_left = Bool(default_value = False, help="should 2D sagittal slices show the anterior direction toward the left or right?").tag(sync=True)
    is_slice_MM = Bool(default_value = False, help="are images aligned to voxel space (False) or world space (True)").tag(sync=True)
    is_high_resolution_capable = Bool(default_value = True, help="demand that high-dot-per-inch displays use native voxel size").tag(sync=True)
    drawing_enabled = Bool(default_value = False, help="allow user to create and edit voxel-based drawings").tag(sync=True)
    pen_value = CFloat(default_value = 1.7976931348623157e+308, help="color of drawing when user drags mouse (if drawingEnabled)").tag(sync=True)
    is_filled_pen = Bool(default_value = False, help="create filled drawings when user drags mouse (if drawingEnabled)").tag(sync=True)
    max_draw_undo_bitmaps = CInt(default_value = 8, help="number of possible undo steps (if drawingEnabled)").tag(sync=True)
    thumbnail = Unicode(default_value = "", help="optional 2D png bitmap that can be rapidly loaded to defer slow loading of 3D image").tag(sync=True)

    def __init__(self, *args, **kwargs):
        """Create an Niivue widget."""
        super(Niivue, self).__init__(*args, **kwargs)

        if "caching" in kwargs:
            self._canvas_manager._caching = kwargs["caching"]

        self.on_msg(self._handle_frontend_event)

    def _handle_frontend_event(self, _, content, buffers):
        print("_handle_frontend_event:", content, buffers)

    def _send_custom(self, command, buffers=[]):
        self.send(command, buffers=buffers)

    #NiiVue functions
    def save_scene(self, filename):
        self._send_custom([COMMANDS["saveScene"], [filename]])

    def add_volume_from_url(self, image_options):
        self._send_custom([COMMANDS["addVolumeFromUrl"], [image_options]])

    def remove_volume_by_url(self, url):
        self._send_custom([COMMANDS["removeVolumeByUrl"], [url]])

    def set_corner_orientation_text(self, is_corner_orientation_text):
        self._send_custom([COMMANDS["setCornerOrientationText"], [is_corner_orientation_text]])

    def set_radiological_convention(self, is_radiological_convention):
        self._send_custom([COMMANDS["setRadiologicalConvention"], [is_radiological_convention]])

    def set_mesh_thickness_on_2D(self, mesh_thickness_on_2D):
        self._send_custom([COMMANDS["setMeshThicknessOn2D"], [mesh_thickness_on_2D]])

    def set_slice_mosaic_string(self, string):
        self._send_custom([COMMANDS["setSliceMosaicString"], [string]])

    def set_slice_mm(self, is_slice_mm):
        self._send_custom([COMMANDS["setSliceMM"], [is_slice_mm]])

    def set_high_resolution_capable(self, is_high_resolution_capable):
        self._send_custom([COMMANDS["setHighResolutionCapable"], [is_high_resolution_capable]])

    '''
    #todo
    def add_volume(self, volume):
        self._send_custom([COMMANDS["addVolume"], [volume]])
    '''

    def add_mesh(self, mesh):
        self._send_custom([COMMANDS["addMesh"], [mesh]])

    def draw_undo(self):
        self._send_custom([COMMANDS["drawUndo"], []])

    def load_drawing_from_url(self, fnm):
        self._send_custom([COMMANDS["loadDrawingFromUrl"], [fnm]])

    def draw_otsu(self, levels):
        self._send_custom([COMMANDS["drawOtsu"], [levels]])

    def remove_haze(self, level, vol_index):
        self._send_custom([COMMANDS["removeHaze"], [level, vol_index]])

    def save_image(self, fnm, is_save_drawing):
        self._send_custom([COMMANDS["saveImage"], [fnm, is_save_drawing]])

    def set_mesh_property(self, id_str, key, val):
        self._send_custom([COMMANDS["setMeshProperty"], [id_str, key, val]])

    def reverse_faces(self, mesh):
        self._send_custom([COMMANDS["reverseFaces"], [mesh]])

    def set_mesh_layer_property(self, mesh, layer, key, val):
        self._send_custom([COMMANDS["setMeshLayerProperty"], [mesh, layer, key, val]])

    def set_pan_2D_xyzmm(self, xyzmm_zoom):
        self._send_custom([COMMANDS["setPan2Dxyzmm"], [xyzmm_zoom]])

    def set_render_azimuth_elevation(self, a, e):
        self._send_custom([COMMANDS["setRenderAzimuthElevation"], [a, e]])

    def set_volume(self, volume, to_index):
        self._send_custom([COMMANDS["setVolume"], [volume, to_index]])

    def remove_volume(self, volume):
        self._send_custom([COMMANDS["removeVolume"], [volume]])

    def remove_volume_by_index(self, index):
        self._send_custom([COMMANDS["removeVolumeByIndex"], [index]])

    def remove_mesh(self, mesh):
        self._send_custom([COMMANDS["removeMesh"], [mesh]])

    def remove_mesh_by_url(self, url):
        self._send_custom([COMMANDS["removeMeshByUrl"], [url]])

    def move_volume_to_bottom(self, volume):
        self._send_custom([COMMANDS["moveVolumeToBottom"], [volume]])

    def move_volume_up(self, volume):
        self._send_custom([COMMANDS["moveVolumeUp"], [volume]])

    def move_volume_down(self, volume):
        self._send_custom([COMMANDS["moveVolumeDown"], [volume]])

    def move_volume_to_top(self, volume):
        self._send_custom([COMMANDS["moveVolumeToTop"], [volume]])

    def set_clip_plane(self, depth_azimuth_elevation):
        self._send_custom([COMMANDS["setClipPlane"], [depth_azimuth_elevation]])

    def set_crosshair_color(self, color):
        self._send_custom([COMMANDS["setCrosshairColor"], [color]])

    def set_crosshair_width(self, crosshair_width):
        self._send_custom([COMMANDS["setCrosshairWidth"], [crosshair_width]])

    def set_drawing_enabled(self, true_or_false):
        self._send_custom([COMMANDS["setDrawingEnabled"], [true_or_false]])

    def set_pen_value(self, pen_value, is_filled_pen):
        self._send_custom([COMMANDS["setPenValue"], [pen_value, is_filled_pen]])

    def set_draw_opacity(self, opacity):
        self._send_custom([COMMANDS["setDrawOpacity"], [opacity]])

    def set_selection_box_color(self, color):
        self._send_custom([COMMANDS["setSelectionBoxColor"], [color]])

    def set_slice_type(self, st):
        self._send_custom([COMMANDS["setSliceType"], [st]])

    def set_opacity(self, vol_idx, new_opacity):
        self._send_custom([COMMANDS["setOpacity"], [vol_idx, new_opacity]])

    def set_scale(self, scale):
        self._send_custom([COMMANDS["setScale"], [scale]])

    def set_clip_plane_color(self, color):
        self._send_custom([COMMANDS["setClipPlaneColor"], [color]])

    def load_document_from_url(self, url):
        self._send_custom([COMMANDS["loadDocumentFromUrl"], [url]])

    def load_volumes(self, volume_list):
        self._send_custom([COMMANDS["loadVolumes"], [volume_list]])

    def add_mesh_from_url(self, mesh_options):
        self._send_custom([COMMANDS["addMeshFromUrl"], [mesh_options]])

    def load_meshes(self, mesh_list):
        self._send_custom([COMMANDS["loadMeshes"], [mesh_list]])

    def load_connectome(self, connectome):
        self._send_custom([COMMANDS["loadConnectome"], [connectome]])

    def create_empty_drawing(self):
        self._send_custom([COMMANDS["createEmptyDrawing"], []])

    def draw_grow_cut(self):
        self._send_custom([COMMANDS["drawGrowCut"], []])

    def set_mesh_shader(self, id_str, mesh_shader_name_or_number):
        self._send_custom([COMMANDS["setMeshShader"], [id_str, mesh_shader_name_or_number]])

    def set_custom_mesh_shader(self, fragment_shader_text, name):
        self._send_custom([COMMANDS["setCustomMeshShader"], [fragment_shader_text, name]])

    def update_gl_volume(self):
        self._send_custom([COMMANDS["updateGLVolume"], []])

    def set_color_map(self, id_str, color_map):
        self._send_custom([COMMANDS["setColorMap"], [id_str, color_map]])

    def set_color_map_negative(self, id_str, color_map_negative):
        self._send_custom([COMMANDS["setColorMapNegative"], [id_str, color_map_negative]])

    def set_modulation_image(self, id_target, id_modulation, modulate_alpha):
        self._send_custom([COMMANDS["setModulationImage"], [id_target, id_modulation, modulate_alpha]])

    def set_frame_4D(self, id_str, frame_4D):
        self._send_custom([COMMANDS["setFrame4D"], [id_str, frame_4D]])

    def set_interpolation(self, is_nearest):
        self._send_custom([COMMANDS["setInterpolation"], [is_nearest]])

    def move_crosshair_in_vox(self, x, y, z):
        self._send_custom([COMMANDS["moveCrosshairInVox"], [x, y, z]])

    def draw_mosaic(self, mosaic_str):
        self._send_custom([COMMANDS["drawMosaic"], [mosaic_str]])
    
    def add_volume(self, file):
        if (file.startswith('http://') or file.startswith('https://')):
            self._send_custom([COMMANDS["addVolumeFromUrl"], [file]])
        else:
            if file.startswith('file://'):
                file = file[7:]
            filename = pathlib.Path(file).name
            filedata = read_file(file)
            self._send_custom([COMMANDS["addVolumeFromBase64"], [filename]], [filedata])
            
