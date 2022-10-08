from ipywidgets import DOMWidget, ValueWidget, register
from traitlets import Unicode, List, Int, Float, Bool, UseEnum, CaselessStrEnum
from .traits import Volume, DragModes, keycodes 
import sys

from ._frontend import module_name, module_version

@register
class Niivue(DOMWidget, ValueWidget):
    _model_name = Unicode('NiivueModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    _view_name = Unicode('NiivueView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    volumes = List(trait=Volume, default_value=[]).tag(sync=True)
    height = Int(default_value=300).tag(sync=True)

    #NiivueOptions
    text_height = Float(default_value = 0.06, help="the text height for orientation labels (0 to 1). Zero for no text labels").tag(sync=True)
    colorbar_height = Float(default_value = 0.05, help="size of colorbar. 0 for no colorbars, fraction of Nifti j dimension").tag(sync=True)
    colorbar_margin = Float(default_value = 0.05, help="padding around colorbar when displayed").tag(sync=True)
    crosshair_width = Int(default_value = 1, help="crosshair size. Zero for no crosshair").tag(sync=True)
    ruler_width = Int(default_value = 4, help="ruler size. Zero (or isRuler is False) for no ruler").tag(sync=True)
    back_color = List(trait=Float, min_len=4, max_len=4, default_value = [0, 0, 0, 1], help="the background color. RGBA values from 0 to 1. Default is black").tag(sync=True)
    crosshair_color = List(trait=Float, min_len=4, max_len=4, default_value = [1, 0, 0, 1], help="the crosshair color. RGBA values from 0 to 1. Default is red").tag(sync=True)
    selection_box_color = List(trait=Float, min_len=4, max_len=4, default_value = [1, 1, 1, 0.5], help="the selection box color when the intensty selection box is shown (right click and drag). RGBA values from 0 to 1. Default is transparent white").tag(sync=True)
    clip_plane_color = List(trait=Float, min_len=4, max_len=4, default_value = [1, 1, 1, 0.5], help="the color of the visible clip plane. RGBA values from 0 to 1. Default is white").tag(sync=True)
    ruler_color = List(trait=Float, min_len=4, max_len=4, default_value = [1, 0, 0, 0.8], help="the color of the ruler. RGBA values from 0 to 1. Default is translucent red").tag(sync=True)
    show_3D_crosshair = Bool(default_value = False, help="True/False whether crosshairs are shown on 3D rendering").tag(sync=True)
    trust_cal_min_max = Bool(default_value = True, help="True/False whether to trust the nifti header values for cal_min and cal_max. Trusting them results in faster loading because we skip computing these values from the data").tag(sync=True)
    clip_plane_hot_key = CaselessStrEnum(keycodes, default_value="KeyC", help="the keyboard key used to cycle through clip plane orientations. The default is \"c\"").tag(sync=True)
    view_mode_hot_key = CaselessStrEnum(keycodes, default_value="KeyV", help="the keyboard key used to cycle through view modes. The default is \"v\"").tag(sync=True)
    key_debounce_time = Int(default_value = 50, help="the keyUp debounce time in milliseconds. The default is 50 ms. You must wait this long before a new hot-key keystroke will be registered by the event listener").tag(sync=True)
    double_touch_timeout = Int(default_value = 500, help="the maximum time in milliseconds for a double touch to be detected. The default is 500 ms").tag(sync=True)
    long_touch_timeout = Int(default_value = 1000, help="the minimum time in milliseconds for a touch to count as long touch. The default is 1000 ms").tag(sync=True)
    is_radiological_convention = Bool(default_value = False, help="whether or not to use radiological convention in the display").tag(sync=True)
    logging = Bool(default_value = False, help="turn on logging or not (True/False)").tag(sync=True)
    loading_text = Unicode(default_value = "waiting on images...", help="the loading text to display when there is a blank canvas and no images").tag(sync=True)
    drag_and_drop_enabled = Bool(default_value = True, help="whether or not to allow file and url drag and drop on the canvas").tag(sync=True)
    is_nearest_interpolation = Bool(default_value = False, help="whether nearest neighbor interpolation is used, else linear interpolation").tag(sync=True)
    is_atlas_outline = Bool(default_value = False, help="whether atlas maps are only visible at the boundary of regions").tag(sync=True)
    is_ruler = Bool(default_value = False, help="whether a 10cm ruler is displayed").tag(sync=True)
    is_colorbar = Bool(default_value = False, help="whether colorbar(s) are shown illustrating values for color maps").tag(sync=True)
    is_orient_cube = Bool(default_value = False, help="whether orientation cube is shown for 3D renderings").tag(sync=True)
    multiplanar_pad_pixels = Int(default_value = 0, help="spacing between tiles of a multiplanar view").tag(sync=True)
    mesh_thickness_on_2D = Float(default_value = sys.float_info.max, help="2D slice views can show meshes within this range. Meshes only visible in slice_MM (world space) mode").tag(sync=True)
    drag_mode = UseEnum(DragModes, default_value=DragModes.contrast, help="behavior for dragging (\"none\", \"contrast\", \"measurement\", \"pan\")").tag(sync=True)
    is_depth_pick_mesh = Bool(default_value = False, help="when both voxel-based image and mesh is loaded, will depth picking be able to detect mesh or only voxels").tag(sync=True)
    is_corner_orientation_text = Bool(default_value = False, help="should slice text be shown in the upper right corner instead of the center of left and top axes?").tag(sync=True)
    sagittal_nose_left = Bool(default_value = False, help="should 2D sagittal slices show the anterior direction toward the left or right?").tag(sync=True)
    is_slice_MM = Bool(default_value = False, help="are images aligned to voxel space (False) or world space (True)").tag(sync=True)
    is_high_resolution_capable = Bool(default_value = True, help="demand that high-dot-per-inch displays use native voxel size").tag(sync=True)
    drawing_enabled = Bool(default_value = False, help="allow user to create and edit voxel-based drawings").tag(sync=True)
    pen_value = Float(default_value = sys.float_info.max, help="color of drawing when user drags mouse (if drawingEnabled)").tag(sync=True)
    is_filled_pen = Bool(default_value = False, help="create filled drawings when user drags mouse (if drawingEnabled)").tag(sync=True)
    max_draw_undo_bitmaps = Int(default_value = 8, help="number of possible undo steps (if drawingEnabled)").tag(sync=True)
    thumbnail = Unicode(default_value = "", help="optional 2D png bitmap that can be rapidly loaded to defer slow loading of 3D image").tag(sync=True)

    def __init__(
        self,
        text_height = 0.06,
        colorbar_height = 0.05,
        colorbar_margin = 0.05,
        crosshair_width = 1,
        ruler_width = 4,
        back_color = [0, 0, 0, 1],
        crosshair_color = [1, 0, 0, 1],
        selection_box_color = [1, 1, 1, 0.5],
        clip_plane_color = [1, 1, 1, 0.5],
        ruler_color = [1, 0, 0, 0.8],
        show_3D_crosshair = False,
        trust_cal_min_max = True,
        clip_plane_hot_key = "KeyC",
        view_mode_hot_key = "KeyV",
        key_debounce_time = 50,
        double_touch_timeout = 500,
        long_touch_timeout = 1000,
        is_radiological_convention = False,
        logging = False,
        loading_text = "waiting on images...",
        drag_and_drop_enabled = True,
        is_nearest_interpolation = False,
        is_atlas_outline = False,
        is_ruler = False,
        is_colorbar = False,
        is_orient_cube = False,
        multiplanar_pad_pixels = 0,
        mesh_thickness_on_2D = sys.float_info.max,
        drag_mode = "contrast",
        is_depth_pick_mesh = False,
        is_corner_orientation_text = False,
        sagittal_nose_left = False,
        is_slice_MM = False,
        is_high_resolution_capable = True,
        drawing_enabled = False,
        pen_value = sys.float_info.max,
        is_filled_pen = False,
        max_draw_undo_bitmaps = 8,
        thumbnail = ""
    ):
        super(Niivue, self).__init__()
        self.text_height = text_height
        self.colorbar_height = colorbar_height
        self.colorbar_margin = colorbar_margin
        self.crosshair_width = crosshair_width
        self.ruler_width = ruler_width
        self.back_color = back_color
        self.crosshair_color = crosshair_color
        self.selection_box_color = selection_box_color
        self.clip_plane_color = clip_plane_color
        self.ruler_color = ruler_color
        self.show_3D_crosshair = show_3D_crosshair
        self.trust_cal_min_max = trust_cal_min_max
        self.clip_plane_hot_key = clip_plane_hot_key
        self.view_mode_hot_key = view_mode_hot_key
        self.key_debounce_time = key_debounce_time
        self.double_touch_timeout = double_touch_timeout
        self.long_touch_timeout = long_touch_timeout
        self.is_radiological_convention = is_radiological_convention
        self.logging = logging
        self.loading_text = loading_text
        self.drag_and_drop_enabled = drag_and_drop_enabled
        self.is_nearest_interpolation = is_nearest_interpolation
        self.is_atlas_outline = is_atlas_outline
        self.is_ruler = is_ruler
        self.is_colorbar = is_colorbar
        self.is_orient_cube = is_orient_cube
        self.multiplanar_pad_pixels = multiplanar_pad_pixels
        self.mesh_thickness_on_2D = mesh_thickness_on_2D
        self.drag_mode = drag_mode
        self.is_depth_pick_mesh = is_depth_pick_mesh
        self.is_corner_orientation_text = is_corner_orientation_text
        self.sagittal_nose_left = sagittal_nose_left
        self.is_slice_MM = is_slice_MM
        self.is_high_resolution_capable = is_high_resolution_capable
        self.drawing_enabled = drawing_enabled
        self.pen_value = pen_value
        self.is_filled_pen = is_filled_pen
        self.max_draw_undo_bitmaps = max_draw_undo_bitmaps
        self.thumbnail = thumbnail

    def load_volumes(self, volumes):
        self.volumes = volumes

    def set_height(self, height):
        self.height = height