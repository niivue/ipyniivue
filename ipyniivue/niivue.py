#!/usr/bin/env python
# coding: utf-8

# Copyright (c) NiiVue.
# Distributed under the terms of the Modified BSD License.

#Much of the structure and many of the functions/classes in this file
#are from https://github.com/martinRenou/ipycanvas. The Niivue class is based off of Canvas class.

"""
TODO: Add module docstring
"""

from traitlets import (
    Unicode, 
    Instance,
    CInt,
    CFloat,
    List,
    Bool, 
    UseEnum,
    CaselessStrEnum,
    Undefined
)
from .traits import ( 
    DragModes, 
    keycodes
)
from ._frontend import module_name, module_version
from ipywidgets import (
    DOMWidget,
    Widget,
    widget_serialization
)

class _CanvasManager(Widget):
    """Private Canvas manager."""

    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    _model_name = Unicode("CanvasManagerModel").tag(sync=True)

    def __init__(self, *args, **kwargs):
        self._caching = kwargs.get("caching", False)
        self._commands_cache = []
        self._buffers_cache = []

        super(_CanvasManager, self).__init__()

    def send_draw_command(self, name, args=[], buffers=[]):
        while len(args) and args[len(args) - 1] is None:
            args.pop()
        self.send_command([name, args, len(buffers)], buffers)

    def send_command(self, command, buffers=[]):
        if self._caching:
            self._commands_cache.append(command)
            self._buffers_cache += buffers
            return
        self._send_custom(command, buffers)

    def flush(self):
        """Flush all the cached commands and clear the cache."""
        if not self._caching or not len(self._commands_cache):
            return

        self._send_custom(self._commands_cache, self._buffers_cache)

        self._commands_cache = []
        self._buffers_cache = []

    def _send_custom(self, command, buffers=[]):
        metadata, command_buffer = commands_to_buffer(command)
        self.send(metadata, buffers=[command_buffer] + buffers)

# Main canvas manager
_CANVAS_MANAGER = _CanvasManager()

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

    _canvas_manager = Instance(_CanvasManager, default_value=_CANVAS_MANAGER).tag(
        sync=True, **widget_serialization
    )

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

    value = Unicode("Hello World").tag(sync=True)

    #NiivueOptions
    text_height = CFloat(default_value = 0.06, help="the text height for orientation labels (0 to 1). Zero for no text labels").tag(sync=True)
    colorbar_height = CFloat(default_value = 0.05, help="size of colorbar. 0 for no colorbars, fraction of Nifti j dimension").tag(sync=True)
    colorbar_margin = CFloat(default_value = 0.05, help="padding around colorbar when displayed").tag(sync=True)
    crosshair_width = CFloat(default_value = 1, help="crosshair size. Zero for no crosshair").tag(sync=True)
    ruler_width = CFloat(default_value = 4, help="ruler size. 0 for no ruler").tag(sync=True)
    back_color = List(trait=CFloat(), default_value = [0, 0, 0, 1], help="the background color. RGBA values from 0 to 1. Default is black").tag(sync=True, min_len=4, max_len=4)
    crosshair_color = List(trait=CFloat(), default_value = [1, 0, 0, 1], help="the crosshair color. RGBA values from 0 to 1. Default is red").tag(sync=True, min_len=4, max_len=4)
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

    def set_volume(self, url):
        self.value = url