import enum

__all__ = [
    "SliceType",
    "DragMode",
    "MuliplanarType",
]


class SliceType(enum.Enum):
    AXIAL = 1
    CORONAL = 2
    SAGITTAL = 3
    MULTIPLANAR = 4
    RENDER = 5


class DragMode(enum.Enum):
    CONTRAST = 1
    MEASUREMENT = 2
    PAN = 3


class MuliplanarType(enum.Enum):
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
