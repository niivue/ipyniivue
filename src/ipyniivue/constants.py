"""
Provides classes for reusable, readable versions of important data.

This module uses enum to enumerate important constants for slice types,
drag modes, and multiplanar types in more readable formats for use in notebooks.
"""

import enum

__all__ = [
    "DragMode",
    "MultiplanarType",
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


class DragMode(enum.Enum):
    """
    An enumeration of drag modes for NiiVue instances.

    Members
    -------
    CONTRAST : int
        Contrast adjustment mode (value 1).
    MEASUREMENT : int
        Measurement mode for taking measurements (value 2).
    PAN : int
        Pan mode for moving around the image (value 3).
    """

    NONE = 0
    CONTRAST = 1
    MEASUREMENT = 2
    PAN = 3
    SLIDER_3D = 4
    CALLBACK_ONLY = 5
    ROI_SELECTION = 6


class MultiplanarType(enum.Enum):
    """
    An enumeration of multiplanar types for NiiVue instances.

    Members
    -------
    AUTO : int
        Automatic multiplanar type (value 0).
    COLUMN : int
        Column multiplanar type (value 1).
    GRID : int
        Grid multiplanar type (value 2).
    ROW : int
        Row multiplanar type (value 3).
    """

    AUTO = 0
    COLUMN = 1
    GRID = 2
    ROW = 3


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


_SNAKE_TO_CAMEL_OVERRIDES = {
    "show_3d_crosshair": "show3Dcrosshair",
    "mesh_thickness_on_2d": "meshThicknessOn2D",
    "yoke_3d_to_2d_zoom": "yoke3Dto2DZoom",
    "is_slice_mm": "isSliceMM",
    "limit_frames_4d": "limitFrames4D",
    "click_to_segment_is_2d": "clickToSegmentIs2D",
}
