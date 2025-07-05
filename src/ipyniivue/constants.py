"""
Provides classes for reusable, readable versions of important data.

This module uses enum to enumerate important constants.
"""

import enum

__all__ = [
    "ColormapType",
    "DragMode",
    "DragModePrimary",
    "DragModeSecondary",
    "MultiplanarType",
    "ShowRender",
    "SliceType",
]


class SliceType(enum.Enum):
    """
    An enumeration of slice types for NiiVue instances.

    Members
    -------
    AXIAL : int
        Axial slice type (value 0).
    CORONAL : int
        Coronal slice type (value 1).
    SAGITTAL : int
        Sagittal slice type (value 2).
    MULTIPLANAR : int
        Multiplanar view type (value 3).
    RENDER : int
        Render view type (value 4).
    """

    AXIAL = 0
    CORONAL = 1
    SAGITTAL = 2
    MULTIPLANAR = 3
    RENDER = 4


class ShowRender(enum.Enum):
    """
    An enumeration for specifying when to show rendering in NiiVue instances.

    Members
    -------
    NEVER : int
        Never show rendering (value 0).
    ALWAYS : int
        Always show rendering (value 1).
    AUTO : int
        Automatically determine whether to show rendering (value 2).
    """

    NEVER = 0
    ALWAYS = 1
    AUTO = 2


class MultiplanarType(enum.Enum):
    """
    An enumeration of multiplanar types for NiiVue instances.

    Members
    -------
    AUTO : int
        Automatic multiplanar layout (value 0).
    COLUMN : int
        Vertical column multiplanar layout (value 1).
    GRID : int
        Grid multiplanar layout (value 2).
    ROW : int
        Horizontal row multiplanar layout (value 3).
    """

    AUTO = 0
    COLUMN = 1
    GRID = 2
    ROW = 3


class DragMode(enum.Enum):
    """
    An enumeration of drag modes for NiiVue instances.

    Members
    -------
    NONE : int
        No drag mode active (value 0).
    CONTRAST : int
        Contrast adjustment mode (value 1).
    MEASUREMENT : int
        Measurement mode for taking measurements (value 2).
    PAN : int
        Pan mode for moving around the image (value 3).
    SLICER_3D : int
        3D slicer interaction mode (value 4).
    CALLBACK_ONLY : int
        Callback only mode (value 5).
    ROI_SELECTION : int
        ROI (Region of Interest) selection mode (value 6).
    """

    NONE = 0
    CONTRAST = 1
    MEASUREMENT = 2
    PAN = 3
    SLICER_3D = 4
    CALLBACK_ONLY = 5
    ROI_SELECTION = 6


class DragModeSecondary(enum.Enum):
    """
    An enumeration of secondary drag modes for NiiVue instances.

    Members
    -------
    NONE : int
        No secondary drag mode active (value 0).
    CONTRAST : int
        Contrast adjustment secondary mode (value 1).
    MEASUREMENT : int
        Measurement secondary mode (value 2).
    PAN : int
        Pan secondary mode (value 3).
    SLICER_3D : int
        3D slicer secondary interaction mode (value 4).
    CALLBACK_ONLY : int
        Callback only secondary mode (value 5).
    ROI_SELECTION : int
        ROI selection secondary mode (value 6).
    """

    NONE = 0
    CONTRAST = 1
    MEASUREMENT = 2
    PAN = 3
    SLICER_3D = 4
    CALLBACK_ONLY = 5
    ROI_SELECTION = 6


class DragModePrimary(enum.Enum):
    """
    An enumeration of primary drag modes for NiiVue instances.

    Members
    -------
    CROSSHAIR : int
        Crosshair mode (value 0).
    WINDOWING : int
        Windowing mode (value 1).
    """

    CROSSHAIR = 0
    WINDOWING = 1


class ColormapType(enum.Enum):
    """
    An enumeration of colormap types.

    Members
    -------
    MIN_TO_MAX : int
        Colormap spans from minimum to maximum values (value 0).
    ZERO_TO_MAX_TRANSPARENT_BELOW_MIN : int
        Colormap spans from zero to maximum, transparent below minimum (value 1).
    ZERO_TO_MAX_TRANSLUCENT_BELOW_MIN : int
        Colormap spans from zero to maximum, translucent below minimum (value 2).
    """

    MIN_TO_MAX = 0
    ZERO_TO_MAX_TRANSPARENT_BELOW_MIN = 1
    ZERO_TO_MAX_TRANSLUCENT_BELOW_MIN = 2


_SNAKE_TO_CAMEL_OVERRIDES = {
    "show_3d_crosshair": "show3Dcrosshair",
    "mesh_thickness_on_2d": "meshThicknessOn2D",
    "yoke_3d_to_2d_zoom": "yoke3Dto2DZoom",
    "is_slice_mm": "isSliceMM",
    "limit_frames_4d": "limitFrames4D",
    "click_to_segment_is_2d": "clickToSegmentIs2D",
    "is_v1_slice_shader": "isV1SliceShader",
    "mesh_xray": "meshXRay",
    "click_to_segment_max_distance_mm": "clickToSegmentMaxDistanceMM",
    "is_2d_slice_shader": "is2DSliceShader",
}
