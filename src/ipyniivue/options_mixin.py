# This file is automatically generated by scripts/generate_options_mixin.py
# Do not edit this file directly

"""Defines a base class mapping NiiVue properties for AnyWidget."""

from __future__ import annotations

import typing

from .constants import DragMode, MultiplanarType, ShowRender, SliceType

__all__ = ["OptionsMixin"]


class OptionsMixin:
    """Base class implementing NiiVue properties."""

    @property
    def text_height(self) -> float:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("textHeight", 0.06)

    @text_height.setter
    def text_height(self, value: float):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "textHeight": value}

    @property
    def colorbar_height(self) -> float:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("colorbarHeight", 0.05)

    @colorbar_height.setter
    def colorbar_height(self, value: float):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "colorbarHeight": value}

    @property
    def crosshair_width(self) -> int:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("crosshairWidth", 1)

    @crosshair_width.setter
    def crosshair_width(self, value: int):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "crosshairWidth": value}

    @property
    def crosshair_gap(self) -> int:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("crosshairGap", 0)

    @crosshair_gap.setter
    def crosshair_gap(self, value: int):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "crosshairGap": value}

    @property
    def ruler_width(self) -> int:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("rulerWidth", 4)

    @ruler_width.setter
    def ruler_width(self, value: int):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "rulerWidth": value}

    @property
    def show_3d_crosshair(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("show3Dcrosshair", False)

    @show_3d_crosshair.setter
    def show_3d_crosshair(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "show3Dcrosshair": value}

    @property
    def back_color(self) -> tuple:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("backColor", (0, 0, 0, 1))

    @back_color.setter
    def back_color(self, value: tuple):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "backColor": value}

    @property
    def crosshair_color(self) -> tuple:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("crosshairColor", (1, 0, 0, 1))

    @crosshair_color.setter
    def crosshair_color(self, value: tuple):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "crosshairColor": value}

    @property
    def font_color(self) -> tuple:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("fontColor", (0.5, 0.5, 0.5, 1))

    @font_color.setter
    def font_color(self, value: tuple):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "fontColor": value}

    @property
    def selection_box_color(self) -> tuple:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("selectionBoxColor", (1, 1, 1, 0.5))

    @selection_box_color.setter
    def selection_box_color(self, value: tuple):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "selectionBoxColor": value}

    @property
    def clip_plane_color(self) -> tuple:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("clipPlaneColor", (0.7, 0, 0.7, 0.5))

    @clip_plane_color.setter
    def clip_plane_color(self, value: tuple):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "clipPlaneColor": value}

    @property
    def ruler_color(self) -> tuple:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("rulerColor", (1, 0, 0, 0.8))

    @ruler_color.setter
    def ruler_color(self, value: tuple):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "rulerColor": value}

    @property
    def colorbar_margin(self) -> float:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("colorbarMargin", 0.05)

    @colorbar_margin.setter
    def colorbar_margin(self, value: float):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "colorbarMargin": value}

    @property
    def trust_cal_min_max(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("trustCalMinMax", True)

    @trust_cal_min_max.setter
    def trust_cal_min_max(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "trustCalMinMax": value}

    @property
    def clip_plane_hot_key(self) -> str:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("clipPlaneHotKey", "KeyC")

    @clip_plane_hot_key.setter
    def clip_plane_hot_key(self, value: str):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "clipPlaneHotKey": value}

    @property
    def view_mode_hot_key(self) -> str:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("viewModeHotKey", "KeyV")

    @view_mode_hot_key.setter
    def view_mode_hot_key(self, value: str):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "viewModeHotKey": value}

    @property
    def double_touch_timeout(self) -> int:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("doubleTouchTimeout", 500)

    @double_touch_timeout.setter
    def double_touch_timeout(self, value: int):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "doubleTouchTimeout": value}

    @property
    def long_touch_timeout(self) -> int:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("longTouchTimeout", 1000)

    @long_touch_timeout.setter
    def long_touch_timeout(self, value: int):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "longTouchTimeout": value}

    @property
    def key_debounce_time(self) -> int:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("keyDebounceTime", 50)

    @key_debounce_time.setter
    def key_debounce_time(self, value: int):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "keyDebounceTime": value}

    @property
    def is_nearest_interpolation(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isNearestInterpolation", False)

    @is_nearest_interpolation.setter
    def is_nearest_interpolation(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isNearestInterpolation": value}

    @property
    def is_resize_canvas(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isResizeCanvas", True)

    @is_resize_canvas.setter
    def is_resize_canvas(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isResizeCanvas": value}

    @property
    def is_atlas_outline(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isAtlasOutline", False)

    @is_atlas_outline.setter
    def is_atlas_outline(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isAtlasOutline": value}

    @property
    def atlas_outline(self) -> float:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("atlasOutline", 0.0)

    @atlas_outline.setter
    def atlas_outline(self, value: float):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "atlasOutline": value}

    @property
    def is_ruler(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isRuler", False)

    @is_ruler.setter
    def is_ruler(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isRuler": value}

    @property
    def is_colorbar(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isColorbar", False)

    @is_colorbar.setter
    def is_colorbar(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isColorbar": value}

    @property
    def is_orient_cube(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isOrientCube", False)

    @is_orient_cube.setter
    def is_orient_cube(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isOrientCube": value}

    @property
    def multiplanar_pad_pixels(self) -> int:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("multiplanarPadPixels", 0)

    @multiplanar_pad_pixels.setter
    def multiplanar_pad_pixels(self, value: int):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "multiplanarPadPixels": value}

    @property
    def multiplanar_force_render(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("multiplanarForceRender", False)

    @multiplanar_force_render.setter
    def multiplanar_force_render(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "multiplanarForceRender": value}

    @property
    def multiplanar_show_render(self) -> ShowRender:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("multiplanarShowRender", ShowRender.AUTO)

    @multiplanar_show_render.setter
    def multiplanar_show_render(self, value: ShowRender):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "multiplanarShowRender": value}

    @property
    def is_radiological_convention(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isRadiologicalConvention", False)

    @is_radiological_convention.setter
    def is_radiological_convention(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isRadiologicalConvention": value}

    @property
    def mesh_thickness_on_2d(self) -> float:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("meshThicknessOn2D", float("inf"))

    @mesh_thickness_on_2d.setter
    def mesh_thickness_on_2d(self, value: float):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "meshThicknessOn2D": value}

    @property
    def drag_mode(self) -> DragMode:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("dragMode", DragMode.CONTRAST)

    @drag_mode.setter
    def drag_mode(self, value: DragMode):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "dragMode": value}

    @property
    def yoke_3d_to_2d_zoom(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("yoke3Dto2DZoom", False)

    @yoke_3d_to_2d_zoom.setter
    def yoke_3d_to_2d_zoom(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "yoke3Dto2DZoom": value}

    @property
    def is_depth_pick_mesh(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isDepthPickMesh", False)

    @is_depth_pick_mesh.setter
    def is_depth_pick_mesh(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isDepthPickMesh": value}

    @property
    def is_corner_orientation_text(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isCornerOrientationText", False)

    @is_corner_orientation_text.setter
    def is_corner_orientation_text(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isCornerOrientationText": value}

    @property
    def sagittal_nose_left(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("sagittalNoseLeft", False)

    @sagittal_nose_left.setter
    def sagittal_nose_left(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "sagittalNoseLeft": value}

    @property
    def is_slice_mm(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isSliceMM", False)

    @is_slice_mm.setter
    def is_slice_mm(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isSliceMM": value}

    @property
    def is_v1_slice_shader(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isV1SliceShader", False)

    @is_v1_slice_shader.setter
    def is_v1_slice_shader(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isV1SliceShader": value}

    @property
    def is_high_resolution_capable(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isHighResolutionCapable", True)

    @is_high_resolution_capable.setter
    def is_high_resolution_capable(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isHighResolutionCapable": value}

    @property
    def log_level(self) -> str:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("logLevel", "info")

    @log_level.setter
    def log_level(self, value: str):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "logLevel": value}

    @property
    def loading_text(self) -> str:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("loadingText", "waiting for images...")

    @loading_text.setter
    def loading_text(self, value: str):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "loadingText": value}

    @property
    def is_force_mouse_click_to_voxel_centers(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isForceMouseClickToVoxelCenters", False)

    @is_force_mouse_click_to_voxel_centers.setter
    def is_force_mouse_click_to_voxel_centers(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isForceMouseClickToVoxelCenters": value}

    @property
    def drag_and_drop_enabled(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("dragAndDropEnabled", True)

    @drag_and_drop_enabled.setter
    def drag_and_drop_enabled(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "dragAndDropEnabled": value}

    @property
    def drawing_enabled(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("drawingEnabled", False)

    @drawing_enabled.setter
    def drawing_enabled(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "drawingEnabled": value}

    @property
    def pen_value(self) -> int:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("penValue", 1)

    @pen_value.setter
    def pen_value(self, value: int):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "penValue": value}

    @property
    def flood_fill_neighbors(self) -> int:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("floodFillNeighbors", 6)

    @flood_fill_neighbors.setter
    def flood_fill_neighbors(self, value: int):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "floodFillNeighbors": value}

    @property
    def is_filled_pen(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isFilledPen", False)

    @is_filled_pen.setter
    def is_filled_pen(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isFilledPen": value}

    @property
    def thumbnail(self) -> str:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("thumbnail", "")

    @thumbnail.setter
    def thumbnail(self, value: str):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "thumbnail": value}

    @property
    def max_draw_undo_bitmaps(self) -> int:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("maxDrawUndoBitmaps", 8)

    @max_draw_undo_bitmaps.setter
    def max_draw_undo_bitmaps(self, value: int):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "maxDrawUndoBitmaps": value}

    @property
    def slice_type(self) -> SliceType:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("sliceType", SliceType.MULTIPLANAR)

    @slice_type.setter
    def slice_type(self, value: SliceType):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "sliceType": value}

    @property
    def mesh_x_ray(self) -> float:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("meshXRay", 0.0)

    @mesh_x_ray.setter
    def mesh_x_ray(self, value: float):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "meshXRay": value}

    @property
    def is_anti_alias(self) -> typing.Any:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isAntiAlias", None)

    @is_anti_alias.setter
    def is_anti_alias(self, value: typing.Any):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isAntiAlias": value}

    @property
    def limit_frames_4d(self) -> float:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("limitFrames4D", float("nan"))

    @limit_frames_4d.setter
    def limit_frames_4d(self, value: float):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "limitFrames4D": value}

    @property
    def is_additive_blend(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("isAdditiveBlend", False)

    @is_additive_blend.setter
    def is_additive_blend(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "isAdditiveBlend": value}

    @property
    def show_legend(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("showLegend", True)

    @show_legend.setter
    def show_legend(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "showLegend": value}

    @property
    def legend_background_color(self) -> tuple:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("legendBackgroundColor", (0.3, 0.3, 0.3, 0.5))

    @legend_background_color.setter
    def legend_background_color(self, value: tuple):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "legendBackgroundColor": value}

    @property
    def legend_text_color(self) -> tuple:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("legendTextColor", (1.0, 1.0, 1.0, 1.0))

    @legend_text_color.setter
    def legend_text_color(self, value: tuple):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "legendTextColor": value}

    @property
    def multiplanar_layout(self) -> MultiplanarType:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("multiplanarLayout", MultiplanarType.AUTO)

    @multiplanar_layout.setter
    def multiplanar_layout(self, value: MultiplanarType):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "multiplanarLayout": value}

    @property
    def render_overlay_blend(self) -> float:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("renderOverlayBlend", 1.0)

    @render_overlay_blend.setter
    def render_overlay_blend(self, value: float):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "renderOverlayBlend": value}

    @property
    def slice_mosaic_string(self) -> str:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("sliceMosaicString", "")

    @slice_mosaic_string.setter
    def slice_mosaic_string(self, value: str):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "sliceMosaicString": value}

    @property
    def center_mosaic(self) -> bool:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("centerMosaic", False)

    @center_mosaic.setter
    def center_mosaic(self, value: bool):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "centerMosaic": value}

    @property
    def gradient_amount(self) -> float:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("gradientAmount", 0.0)

    @gradient_amount.setter
    def gradient_amount(self, value: float):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "gradientAmount": value}

    @property
    def gradient_opacity(self) -> float:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("gradientOpacity", 0.0)

    @gradient_opacity.setter
    def gradient_opacity(self, value: float):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "gradientOpacity": value}

    @property
    def force_device_pixel_ratio(self) -> int:
        """Automatically generated property. See generate_options_mixin.py."""
        return self._opts.get("forceDevicePixelRatio", 0)

    @force_device_pixel_ratio.setter
    def force_device_pixel_ratio(self, value: int):
        """Automatically generated property. See generate_options_mixin.py."""
        self._opts = {**self._opts, "forceDevicePixelRatio": value}
