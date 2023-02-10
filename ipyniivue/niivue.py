#!/usr/bin/env python
# coding: utf-8

# Copyright (c) NiiVue.
# Distributed under the terms of the Modified BSD License.

#Much of the structure and many of the functions/classes in this file
#are from https://github.com/martinRenou/ipycanvas. The Niivue class is based off of Canvas class.

import pathlib
import random
import string
from urllib.request import url2pathname
from urllib.parse import urlparse

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

class _CanvasBase(DOMWidget):
    """
    Attributes:
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
    
    Attributes:
        text_height (float): the text height for orientation labels (0 to 1). Zero for no text labels. Default is 0.06.
        colorbar_height (float): size of colorbar. 0 for no colorbars, fraction of Nifti j dimension. Default is 0.05.
        colorbar_margin (float): padding around colorbar when displayed. Default is 0.05.
        crosshair_width (float): crosshair size. Zero for no crosshair. Default is 1.
        ruler_width (float): ruler size. 0 for no ruler. Default is 4.
        back_color (list): the background color. RGBA values from 0 to 1. Default is black ([0,0,0,1]).
        crosshair_color (list): the crosshair color. RGBA values from 0 to 1. Default is red ([1,0,0,1]).
        selection_box_color (list): the selection box color when the intensty selection box is shown (right click and drag). RGBA values from 0 to 1. Default is transparent white ([1,1,1,0.5]).
        clip_plane_color (list): the color of the visible clip plane. RGBA values from 0 to 1. Default is white ([1,1,1,0.5]).
        ruler_color (list): the color of the ruler. RGBA values from 0 to 1. Default is translucent red ([1, 0, 0, 0.8]).
        show_3D_crosshair (bool): True/False whether crosshairs are shown on 3D rendering. Default is False.
        trust_cal_min_max (bool): True/False whether to trust the nifti header values for cal_min and cal_max. Trusting them results in faster loading because we skip computing these values from the data. Default is True.
        clip_plane_hot_key (str): the keyboard key used to cycle through clip plane orientations. Default is "KeyC".
        view_mode_hot_key (str): the keyboard key used to cycle through view modes. Default is "KeyV".
        key_debounce_time (float): the keyUp debounce time in milliseconds You must wait this long before a new hot-key keystroke will be registered by the event listener. The default is 50 ms.
        double_touch_timeout (float): the maximum time in milliseconds for a double touch to be detected. The default is 500 ms.
        long_touch_timeout (float): the minimum time in milliseconds for a touch to count as long touch. The default is 1000 ms.
        is_radiological_convention (bool): whether or not to use radiological convention in the display. Default is False.
        loading_text (str): the loading text to display when there is a blank canvas and no images. Default is "waiting on images...".
        drag_and_drop_enabled (bool): whether or not to allow file and url drag and drop on the canvas. Default is True.
        is_nearest_interpolation (bool): whether nearest neighbor interpolation is used, else linear interpolation. Default is False.
        is_atlas_outline (bool): whether atlas maps are only visible at the boundary of regions. Default is False.
        is_ruler (bool): whether a 10cm ruler is displayed. Default is False.
        is_colorbar (bool): whether colorbar(s) are shown illustrating values for color maps. Default is False.
        is_orient_cube (bool): whether orientation cube is shown for 3D renderings. Default is False.
        multiplanar_pad_pixels (int): spacing between tiles of a multiplanar view. Default is 0.
        mesh_thickness_on_2D (float): 2D slice views can show meshes within this range. Meshes only visible in sliceMM (world space) mode. Default is Infinity.
        drag_mode(str/int): behavior for dragging. string ("none", "contrast", "measurement", "pan") or integer (0, 1, 2, 3). Default is "contrast" or 1.
        is_depth_pick_mesh (bool): when both voxel-based image and mesh is loaded, will depth picking be able to detect mesh or only voxels. Default is False.
        is_corner_orientation_text (bool): should slice text be shown in the upper right corner instead of the center of left and top axes?. Default is False.
        sagittal_nose_left (bool): should 2D sagittal slices show the anterior direction toward the left or right?. Default is False.
        is_slice_MM (bool): are images aligned to voxel space (False) or world space (True). Default is False.
        is_high_resolution_capable (bool): demand that high-dot-per-inch displays use native voxel size. Default is True.
        drawing_enabled (bool): allow user to create and edit voxel-based drawings. Default is False.
        pen_value (float): color of drawing when user drags mouse (if drawing_enabled). Default is Infinity.
        is_filled_pen (bool): create filled drawings when user drags mouse (if drawing_enabled). Default is False.
        max_draw_undo_bitmaps (int): number of possible undo steps (if drawing_enabled). Default is 8.
        thumbnail (str): optional 2D png bitmap that can be rapidly loaded to defer slow loading of 3D image. Default is "".
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

    def save_scene(self, filename):
        """
        Save the webgl2 canvas as png format bitmap.
        
        Parameters:
            filename (str): for screen capture.
        """
        self._send_custom([COMMANDS["saveScene"], [filename]])

    def add_volume_from_url(self, url):
        """
        Add an image and notify subscribers
        
        Parameters:
            url (str): The url of the volume.
        """
        self._send_custom([COMMANDS["addVolumeFromUrl"], [url]])

    def remove_volume_by_url(self, url):
        """
        Remove volume by url
        
        Parameters:
            url (str): Volume added by url to remove.
        """
        self._send_custom([COMMANDS["removeVolumeByUrl"], [url]])

    def set_corner_orientation_text(self, is_corner_orientation_text):
        """
        Set text appearance at corner (True) or sides of 2D slice (False).
        
        Parameters:
            is_corner_orientation_text (bool): text appearance at corner.
        """
        self._send_custom([COMMANDS["setCornerOrientationText"], [is_corner_orientation_text]])

    def set_radiological_convention(self, is_radiological_convention):
        """
        Control whether 2D slices use radiological or neurological convention.

        Parameters:
            is_radiological_convention (bool): use radiological convention.
        """
        self._send_custom([COMMANDS["setRadiologicalConvention"], [is_radiological_convention]])

    def set_mesh_thickness_on_2D(self, mesh_thickness_on_2D):
        """
        Limit visibility of mesh in front of a 2D image. Requires world-space mode. Use float('inf') to show entire mesh or 0.0 to hide mesh.

        Parameters:
            mesh_thickness_on_2D (float): distance from voxels for clipping mesh
        """
        self._send_custom([COMMANDS["setMeshThicknessOn2D"], [mesh_thickness_on_2D]])

    def set_slice_mosaic_string(self, description):
        """
        Create a custom multi-slice mosaic (aka lightbox, montage) view.

        Parameters:
            description (str): description of mosaic.
        """
        self._send_custom([COMMANDS["setSliceMosaicString"], [description]])

    def set_slice_mm(self, is_slice_mm):
        """
        Control whether 2D slices use world space (true) or voxel space (false). Beware that voxel space mode limits properties like panning, zooming and mesh visibility.

        Parameters:
            is_slice_mm (bool): determines view mode.
        """
        self._send_custom([COMMANDS["setSliceMM"], [is_slice_mm]])

    def set_high_resolution_capable(self, is_high_resolution_capable):
        """
        Force WebGL canvas to use high resolution display, regardless of browser defaults.

        Parameters:
            is_high_resolution_capable (bool): allow high-DPI display
        """
        self._send_custom([COMMANDS["setHighResolutionCapable"], [is_high_resolution_capable]])

    def add_mesh(self, mesh):
        """
        todo: Add a new mesh to the canvas.

        Parameters:
            mesh (todo)
        """
        self._send_custom([COMMANDS["addMesh"], [mesh]])

    def draw_undo(self):
        """
        Restore drawing to previous state
        """
        self._send_custom([COMMANDS["drawUndo"], []])

    def load_drawing_from_url(self, url):
        """
        Open drawing

        Parameters:
            url (str): the url
        """
        self._send_custom([COMMANDS["loadDrawingFromUrl"], [url]])

    def draw_otsu(self, levels):
        """
        Draw otsu

        Parameters:
            levels (int): (2-4) segment brain into this many types
        """
        self._send_custom([COMMANDS["drawOtsu"], [levels]])

    def remove_haze(self, level, vol_index):
        """
        Remove dark voxels in air

        Parameters:
            level (int): (1-5) larger values for more preserved voxels
            vol_index (int): volume to dehaze
        """
        self._send_custom([COMMANDS["removeHaze"], [level, vol_index]])

    def save_image(self, filename, is_save_drawing):
        """
        Save voxel-based image to disk

        Parameters:
            filename (str): filename of NIfTI image to create
            is_save_drawing (bool): determines whether drawing or background image is saved
        """
        self._send_custom([COMMANDS["saveImage"], [filename, is_save_drawing]])

    def set_mesh_property(self, mesh_id, key, value):
        """
        Change property of mesh, tractogram or connectome

        Parameters:
            mesh_id (int): identity of mesh to change
            key (str): attribute to change
            value (float): for attribute
        """
        self._send_custom([COMMANDS["setMeshProperty"], [mesh_id, key, value]])

    def reverse_faces(self, mesh_id):
        """
        Reverse triangle winding of mesh (swap front and back faces)

        Parameters:
            mesh_id (int): identity of mesh to change
        """
        self._send_custom([COMMANDS["reverseFaces"], [mesh_id]])

    def set_mesh_layer_property(self, mesh_id, layer, key, val):
        """
        Reverse triangle winding of mesh (swap front and back faces)

        Parameters:
            mesh_id (int): identity of mesh to change
            layer (int): selects the mesh overlay (e.g. GIfTI or STC file)
            key (str): attribute to change
            value (float): for attribute
        """
        self._send_custom([COMMANDS["setMeshLayerProperty"], [mesh_id, layer, key, val]])

    def set_pan_2D_xyzmm(self, xyzmm_zoom):
        """
        Adjust offset position and scale of 2D sliceScale

        Parameters:
            xyzmm_zoom (list): first three components are spatial, fourth is scaling
        """
        self._send_custom([COMMANDS["setPan2Dxyzmm"], [xyzmm_zoom]])

    def set_render_azimuth_elevation(self, azimuth, elevation):
        """
        Set rotation of 3D render view

        Parameters:
            azimuth (float): which direction/angle to face
            elevation (float): how high up
        """
        self._send_custom([COMMANDS["setRenderAzimuthElevation"], [azimuth, elevation]])

    def set_volume(self, volume, to_index):
        """
        todo: Set the index of a volume. This will change it's ordering and appearance if there are multiple volumes loaded.

        volume (todo): the volume to update
        to_index (int): the index to move the volume to. The default is the background (0 index)
        """
        self._send_custom([COMMANDS["setVolume"], [volume, to_index]])

    def remove_volume(self, volume):
        """
        todo: Remove a volume

        Parameters:
            volume (todo): volume to remove
        """
        self._send_custom([COMMANDS["removeVolume"], [volume]])

    def remove_volume_by_index(self, index):
        """
        Remove a volume by index

        Parameters:
            index (int): index of volume to remove
        """
        self._send_custom([COMMANDS["removeVolumeByIndex"], [index]])

    def remove_mesh(self, mesh):
        """
        todo: Remove a triangulated mesh, connectome or tractogram

        Parameters:
            mesh (todo): mesh to delete
        """
        self._send_custom([COMMANDS["removeMesh"], [mesh]])

    def remove_mesh_by_url(self, url):
        """
        Remove a triangulated mesh, connectome or tractogram

        Parameters:
            url (str): URL of mesh to delete
        """
        self._send_custom([COMMANDS["removeMeshByUrl"], [url]])

    def move_volume_to_bottom(self, volume):
        """
        todo: Move a volume to the bottom of the stack of loaded volumes. The volume will become the background

        Parameters:
            volume (todo): the volume to move
        """
        self._send_custom([COMMANDS["moveVolumeToBottom"], [volume]])

    def move_volume_up(self, volume):
        """
        todo: Move a volume up one index position in the stack of loaded volumes. This moves it up one layer

        Parameters:
            volume (todo): the volume to move
        """
        self._send_custom([COMMANDS["moveVolumeUp"], [volume]])

    def move_volume_down(self, volume):
        """
        todo: Move a volume down one index position in the stack of loaded volumes. This moves it down one layer

        Parameters:
            volume (todo): the volume to move
        """
        self._send_custom([COMMANDS["moveVolumeDown"], [volume]])

    def move_volume_to_top(self, volume):
        """
        todo: Move a volume to the top position in the stack of loaded volumes. This will be the top layer

        Parameters:
            volume (todo): 
        """
        self._send_custom([COMMANDS["moveVolumeToTop"], [volume]])

    def set_clip_plane(self, depth_azimuth_elevation):
        """
        Update the clip plane orientation in 3D view mode

        Parameters:
            depth_azimuth_elevation (list): a two component vector. azimuth: camera position in degrees around object, typically 0..360 (or -180..+180). elevation: camera height in degrees, range -90..90
        """
        self._send_custom([COMMANDS["setClipPlane"], [depth_azimuth_elevation]])

    def set_crosshair_color(self, color):
        """
        Set the crosshair color

        Parameters:
            color (list): an RGBA array. Values range from 0 to 1
        """
        self._send_custom([COMMANDS["setCrosshairColor"], [color]])

    def set_crosshair_width(self, crosshair_width):
        """
        Set thickness of crosshair

        Parameters:
            crosshair_width (float): the crosshair width
        """
        self._send_custom([COMMANDS["setCrosshairWidth"], [crosshair_width]])

    def set_drawing_enabled(self, drawing):
        """
        Does dragging over a 2D slice create a drawing?

        Parameters:
            drawing (bool): enabled (true) or not (false)
        """
        self._send_custom([COMMANDS["setDrawingEnabled"], [drawing]])

    def set_pen_value(self, pen_value, is_filled_pen):
        """
        Determine color and style of drawing

        Parameters:
            pen_value (bool): sets the color of the pen
            is_filled_pen (bool): determines if dragging creates flood-filled shape
        """
        self._send_custom([COMMANDS["setPenValue"], [pen_value, is_filled_pen]])

    def set_draw_opacity(self, opacity):
        """
        Control whether drawing is tansparent (0), opaque (1) or translucent (between 0 and 1).

        Parameters:
            opacity (float): translucency of drawing
        """
        self._send_custom([COMMANDS["setDrawOpacity"], [opacity]])

    def set_selection_box_color(self, color):
        """
        Set the selection box color. A selection box is drawn when you right click and drag to change image intensity

        Parameters:
            color (list): an RGBA array. values range from 0 to 1
        """
        self._send_custom([COMMANDS["setSelectionBoxColor"], [color]])

    def set_slice_type(self, slice_type):
        """
        Set the slice type. This changes the view mode

        Parameters:
            slice_type (todo)
        """
        self._send_custom([COMMANDS["setSliceType"], [slice_type]])

    def set_opacity(self, vol_idx, new_opacity):
        """
        Set the opacity of a volume given by volume index

        Parameters:
            vol_idx (int): the volume index of the volume to change
            new_opacity (float): the opacity value. valid values range from 0 to 1. 0 will effectively remove a volume from the scene
        """
        self._send_custom([COMMANDS["setOpacity"], [vol_idx, new_opacity]])

    def set_scale(self, scale):
        """
        Set the scale of the 3D rendering. Larger numbers effectively zoom.

        Parameters:
            scale (float): the new scale value
        """
        self._send_custom([COMMANDS["setScale"], [scale]])

    def set_clip_plane_color(self, color):
        """
        Set the color of the 3D clip plane

        Parameters:
            color (list): the new color. expects an array of RGBA values. values can range from 0 to 1
        """
        self._send_custom([COMMANDS["setClipPlaneColor"], [color]])

    def load_document_from_url(self, url):
        """
        Load document from URL

        Parameters:
            url (str): URL of NVDocument
        """
        self._send_custom([COMMANDS["loadDocumentFromUrl"], [url]])

    def load_volumes(self, volume_list):
        """
        todo: load an array of volume objects

        Parameters:
            volume_list (list): the array of objects to load
        """
        self._send_custom([COMMANDS["loadVolumes"], [volume_list]])

    def add_mesh_from_url(self, url):
        """
        Add mesh and notify subscribers

        Parameters:
            url (str): url of mesh
        """
        self._send_custom([COMMANDS["addMeshFromUrl"], [url]])

    def load_meshes(self, mesh_list):
        """
        todo: load an array of meshes

        Parameters:
            mesh_list (list): the array of objects to load
        """
        self._send_custom([COMMANDS["loadMeshes"], [mesh_list]])

    def load_connectome(self, connectome):
        """
        Load a connectome specified by json

        Parameters:
            connectome (str): model
        """
        self._send_custom([COMMANDS["loadConnectome"], [connectome]])

    def create_empty_drawing(self):
        """
        Generate a blank canvas for the pen tool
        """
        self._send_custom([COMMANDS["createEmptyDrawing"], []])

    def draw_grow_cut(self):
        """
        Dilate drawing so all voxels are colored. works on drawing with multiple colors
        """
        self._send_custom([COMMANDS["drawGrowCut"], []])

    def set_mesh_shader(self, mesh_id, mesh_shader_name_or_number):
        """
        Select new shader for triangulated meshes and connectomes

        Parameters:
            mesh_id (int): id of mesh to change
            mesh_shader_name_or_number (str/int): identify shader for usage
        """
        self._send_custom([COMMANDS["setMeshShader"], [mesh_id, mesh_shader_name_or_number]])

    def set_custom_mesh_shader(self, fragment_shader_text, name):
        """
        control whether drawing is tansparent (0), opaque (1) or translucent (between 0 and 1).

        Parameters:
            fragment_shader_text (str): custom fragment shader
            name (str): title for new shader
        """
        self._send_custom([COMMANDS["setCustomMeshShader"], [fragment_shader_text, name]])

    def update_gl_volume(self):
        """
        update the webGL 2.0 scene after making changes to the array of volumes. Use if altering one or more volumes manually (outside of Niivue setter methods).
        """
        self._send_custom([COMMANDS["updateGLVolume"], []])

    def set_color_map(self, id_str, color_map):
        """
        Update the colormap of an image given its ID

        Parameters:
            id_str (str): the ID of the image
            color_map (str): the name of the color_map to use
        """
        self._send_custom([COMMANDS["setColorMap"], [id_str, color_map]])

    def set_color_map_negative(self, id_str, color_map_negative):
        """
        Use given color map for negative voxels in image

        Parameters:
            id_str (str): the ID of the image
            color_map_negative (str): the name of the color_map to use
        """
        self._send_custom([COMMANDS["setColorMapNegative"], [id_str, color_map_negative]])

    def set_modulation_image(self, id_target, id_modulation, modulate_alpha):
        """
        Modulate intensity of one image based on intensity of another

        Parameters:
            id_target (str): the ID of the image to be biased
            id_modulation (str): the ID of the image that controls bias (None to disable modulation)
            modulate_alpha (bool): the modulation influence alpha transparency (True) or RGB color (False) components
        """
        self._send_custom([COMMANDS["setModulationImage"], [id_target, id_modulation, modulate_alpha]])

    def set_frame_4D(self, id_str, frame_4D):
        """
        Show desired 3D volume from 4D time series

        Parameters:
            id_str: the ID of the 4D image
            frame_4D: to display (indexed from zero)
        """
        self._send_custom([COMMANDS["setFrame4D"], [id_str, frame_4D]])

    def set_interpolation(self, is_nearest):
        """
        Select between nearest and linear interpolation for voxel based images

        Parameters:
            is_nearest (bool): whether nearest neighbor interpolation is used, else linear interpolation
        """
        self._send_custom([COMMANDS["setInterpolation"], [is_nearest]])

    def move_crosshair_in_vox(self, x, y, z):
        """
        Move crosshair a fixed number of voxels (instead of mm)

        Parameters:
            x (float): translate left (-) or right (+)
            y (float): translate posterior (-) or +anterior (+)
            z (float): translate inferior (-) or superior (+)
        """
        self._send_custom([COMMANDS["moveCrosshairInVox"], [x, y, z]])

    def draw_mosaic(self, mosaic_str):
        """
        Display a lightbox or montage view

        Parameters:
            mosaic_str (str): specifies orientation (A,C,S) and location of slices.
        """
        self._send_custom([COMMANDS["drawMosaic"], [mosaic_str]])
    
    def add_volume(self, file):
        """
        Add a new volume to the canvas

        Parameters:
            file (str): the path to the file (either url or local path)
        """
        if (file.startswith('http://') or file.startswith('https://')):
            self._send_custom([COMMANDS["addVolumeFromUrl"], [file]])
        else:
            if file.startswith('file://'):
                parsed = urlparse(file)
                file = url2pathname(parsed.path)
            p = pathlib.Path(file)
            name = p.name
            filedata = p.read_bytes()
            self._send_custom([COMMANDS["addVolumeFromBase64"], [name]], [filedata])
            
    def add_object(self, img):
        """
        Load a nibabel.nifti1.Nifti1Image object as a volume

        Parameters:
            img (nibabel.nifti1.Nifti1Image): Nifti1 image
        """
        filename = img.get_filename() or ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        self._send_custom([COMMANDS["addVolumeFromBase64"], [filename]], [img.to_bytes()])