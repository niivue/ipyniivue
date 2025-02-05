"""Defines constants for reuse across the package."""

import enum

__all__ = [
    "DragMode",
    "MuliplanarType",
    "SliceType",
]


class SliceType(enum.Enum):
    """Maps numerical values to slice type names."""

    AXIAL = 0
    CORONAL = 1
    SAGITTAL = 2
    MULTIPLANAR = 3
    RENDER = 4


class DragMode(enum.Enum):
    """Maps numerical values to types of mouse interactions."""

    CONTRAST = 1
    MEASUREMENT = 2
    PAN = 3


class MuliplanarType(enum.Enum):
    """Maps numerical values to types of panel arrangements."""

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
