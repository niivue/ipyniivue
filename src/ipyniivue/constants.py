"""
Provides classes for reusable, readable versions of important data.

This module uses enum to enumerate important constants for slice types,
drag modes, and multiplanar types in more readable formats for use in notebooks.
"""

import enum

__all__ = [
    "DragMode",
    "MuliplanarType",
    "SliceType",
]


class SliceType(enum.Enum):
    """
    Defines the number value equivalents for each SliceType of a NiiVue instance.

    Parameters
    ----------
    enum.Enum
        A new enumeration for this class to store members.
    """

    AXIAL = 0
    CORONAL = 1
    SAGITTAL = 2
    MULTIPLANAR = 3
    RENDER = 4


class DragMode(enum.Enum):
    """
    Defines the number value equivalents for each DragMode of a NiiVue instance.

    Paramters
    ---------
    enum.Enum
        A new enumeration for this class to store members.
    """

    CONTRAST = 1
    MEASUREMENT = 2
    PAN = 3


class MuliplanarType(enum.Enum):
    """
    Defines the number value equivalents for each MultiplanarType of a NiiVue instance.

    Paramters
    ---------
    enum.Enum
        A new enumeration for this class to store members.
    """

    AUTO = 0
    COLUMN = 1
    GRID = 2
    ROW = 3


_SNAKE_TO_CAMEL_OVERRIDES = {
    "show_3d_crosshair": "show3Dcrosshair",
    "mesh_thickness_on_2d": "meshThicknessOn2D",
    "yoke_3d_to_2d_zoom": "yoke3Dto2DZoom",
    "is_slice_mm": "isSliceMM",
    "limit_frames_4d": "limitFrames4D",
}
