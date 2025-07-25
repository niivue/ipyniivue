import enum
import math
import pathlib
import typing

from ipyniivue.constants import (
    _SNAKE_TO_CAMEL_OVERRIDES,
    DragMode,
    DragModePrimary,
    MultiplanarType,
    ShowRender,
    SliceType,
)

RENAME_OVERRIDES = {v: k for k, v in _SNAKE_TO_CAMEL_OVERRIDES.items()}


def camel_to_snake(name: str):
    return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip("_")


def type_hint(value: typing.Any):
    if isinstance(value, bool):
        return "t.Bool"
    elif isinstance(value, int):
        return "t.Int"
    elif isinstance(value, float):
        return "t.Float"
    elif isinstance(value, str):
        return "t.Unicode"
    elif isinstance(value, tuple):
        return "t.Tuple"
    elif isinstance(value, list):
        return "t.List"
    elif value is None:
        return "t.Any"
    elif isinstance(value, enum.Enum):
        enum_class_name = type(value).__name__
        return f"t.UseEnum({enum_class_name}"
    else:
        return "t.Any"


def get_default_value(value: typing.Any):
    if value == float("inf"):
        return 'float("inf")'
    if isinstance(value, float) and math.isnan(value):
        return 'float("nan")'
    if isinstance(value, enum.Enum):
        enum_class_name = type(value).__name__
        return f"{enum_class_name}.{value.name}"
    if isinstance(value, str):
        return f'"{value}"'
    return repr(value)


def generate_config_options(options: dict[str, typing.Any]):
    lines = [
        "# This file is automatically generated by scripts/generate_options_mixin.py",
        "# Do not edit this file directly",
        "",
        '"""Defines a class for NiiVue configuration options."""',
        "",
        "import traitlets as t",
        "",
        "from ipyniivue.constants import (",
        "    DragMode,",
        "    DragModePrimary,",
        "    MultiplanarType,",
        "    ShowRender,",
        "    SliceType,",
        ")",
        "",
        '__all__ = ["CAMEL_TO_SNAKE", "SNAKE_TO_CAMEL", "ConfigOptions"]',
        "",
        "",
        "class ConfigOptions(t.HasTraits):",
        '    """Configuration options for NiiVue."""',
        "",
        "    _parent = None",
        "",
    ]

    for option, value in options.items():
        # Convert camelCase to snake_case
        snake_name = RENAME_OVERRIDES.get(option, camel_to_snake(option))
        hint = type_hint(value)
        default_value = get_default_value(value)
        if "UseEnum" in hint:
            # For Enums, default_value is passed as a keyword argument
            lines.append(
                f"    {snake_name} = {hint}, "
                f"default_value={default_value}).tag(sync=False)"
            )
        else:
            lines.append(f"    {snake_name} = {hint}({default_value}).tag(sync=False)")
    lines.append("")

    # Add __init__ method
    lines.append("    def __init__(self, parent=None, **kwargs):")
    lines.append("        super().__init__(**kwargs)")
    lines.append("        self._parent = parent")
    lines.append("")

    # Add observe method
    option_names = [
        RENAME_OVERRIDES.get(option, camel_to_snake(option))
        for option in options.keys()
    ]

    lines.append("    _OBSERVED_TRAITS = (")
    for name in option_names:
        lines.append(f'        "{name}",')
    lines.append("    )")
    lines.append("")

    lines.append("    @t.observe(*_OBSERVED_TRAITS)")
    lines.append("    def _propagate_parent_change(self, change):")
    lines.append(
        "        if self._parent and callable("
        'getattr(self._parent, "_notify_opts_changed", None)):'
    )
    lines.append("            self._parent._notify_opts_changed()")
    lines.append("")

    option_names = options.keys()
    snake_case_names = [
        RENAME_OVERRIDES.get(option, camel_to_snake(option)) for option in option_names
    ]
    mappings = dict(zip(option_names, snake_case_names))
    lines.append("CAMEL_TO_SNAKE = {")
    for orig_name, snake_name in mappings.items():
        lines.append(f'    "{orig_name}": "{snake_name}",')
    lines.append("}")
    lines.append("")

    lines.append("SNAKE_TO_CAMEL = {v: k for k, v in CAMEL_TO_SNAKE.items()}")

    return "\n".join(lines)


if __name__ == "__main__":
    # Copied from niivue (should be able to automatically generate this)
    DEFAULT_OPTIONS = {
        "textHeight": -1.0,
        "fontSizeScaling": 0.4,
        "fontMinPx": 13,
        "colorbarHeight": 0.05,
        "colorbarWidth": -1.0,
        "showColorbarBorder": True,
        "crosshairWidth": 1.0,
        "crosshairWidthUnit": "voxels",
        "crosshairGap": 0.0,
        "rulerWidth": 4.0,
        "show3Dcrosshair": False,
        "backColor": (0.0, 0.0, 0.0, 1.0),
        "crosshairColor": (1.0, 0.0, 0.0, 1.0),
        "fontColor": (0.5, 0.5, 0.5, 1.0),
        "selectionBoxColor": (1.0, 1.0, 1.0, 0.5),
        "clipPlaneColor": (0.7, 0.0, 0.7, 0.5),
        "clipThick": 2.0,
        "clipVolumeLow": (0.0, 0.0, 0.0),
        "clipVolumeHigh": (1.0, 1.0, 1.0),
        "rulerColor": (1.0, 0.0, 0.0, 0.8),
        "colorbarMargin": 0.05,
        "trustCalMinMax": True,
        "clipPlaneHotKey": "KeyC",
        "viewModeHotKey": "KeyV",
        "doubleTouchTimeout": 500,
        "longTouchTimeout": 1000,
        "keyDebounceTime": 50,
        "isNearestInterpolation": False,
        "isResizeCanvas": True,
        "atlasOutline": 0.0,
        "atlasActiveIndex": 0,
        "isRuler": False,
        "isColorbar": False,
        "isOrientCube": False,
        "tileMargin": 0.0,
        "multiplanarPadPixels": 0,
        "multiplanarForceRender": False,
        "multiplanarEqualSize": False,
        "multiplanarShowRender": ShowRender.AUTO,
        "isRadiologicalConvention": False,
        "meshThicknessOn2D": float("inf"),
        "dragMode": DragMode.CONTRAST,
        "dragModePrimary": DragModePrimary.CROSSHAIR,
        "yoke3Dto2DZoom": False,
        "isDepthPickMesh": False,
        "isCornerOrientationText": False,
        "isOrientationTextVisible": True,
        "heroImageFraction": 0,
        "heroSliceType": SliceType.RENDER,
        "sagittalNoseLeft": False,
        "isSliceMM": False,
        "isV1SliceShader": False,
        "forceDevicePixelRatio": 0.0,
        "logLevel": "info",
        "loadingText": "loading ...",
        "isForceMouseClickToVoxelCenters": False,
        "dragAndDropEnabled": True,
        "drawingEnabled": False,
        "penValue": 1.0,
        "floodFillNeighbors": 6,
        "isFilledPen": False,
        "thumbnail": "",
        "maxDrawUndoBitmaps": 8,
        "sliceType": SliceType.MULTIPLANAR,
        "meshXRay": 0.0,
        "isAntiAlias": None,
        "limitFrames4D": float("nan"),
        "isAdditiveBlend": False,
        "showLegend": True,
        "legendBackgroundColor": (0.3, 0.3, 0.3, 0.5),
        "legendTextColor": (1.0, 1.0, 1.0, 1.0),
        "multiplanarLayout": MultiplanarType.AUTO,
        "renderOverlayBlend": 1.0,
        "sliceMosaicString": "",
        "centerMosaic": False,
        "penSize": 1.0,
        "interactive": True,
        "clickToSegment": False,
        "clickToSegmentRadius": 3.0,
        "clickToSegmentBright": True,
        "clickToSegmentAutoIntensity": False,
        "clickToSegmentIntensityMax": float("nan"),
        "clickToSegmentIntensityMin": float("nan"),
        "clickToSegmentPercent": 0.0,
        "clickToSegmentMaxDistanceMM": float("inf"),
        "clickToSegmentIs2D": False,
        "selectionBoxLineThickness": 4.0,
        "selectionBoxIsOutline": False,
        "scrollRequiresFocus": False,
        "showMeasureUnits": True,
        "measureTextJustify": "center",
        "measureTextColor": (1.0, 0.0, 0.0, 1.0),
        "measureLineColor": (1.0, 0.0, 0.0, 1.0),
        "measureTextHeight": 0.06,
        "isAlphaClipDark": False,
        "gradientOrder": 1,
        "gradientOpacity": 0.0,
        "renderSilhouette": 0.0,
        "gradientAmount": 0.0,
        "invertScrollDirection": False,
        "is2DSliceShader": False,
    }
    code = generate_config_options(DEFAULT_OPTIONS)
    loc = pathlib.Path(__file__).parent / "../src/ipyniivue/config_options.py"
    loc.write_text(code)
