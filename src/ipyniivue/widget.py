"""
Widgets representing NiiVue, Volume, Mesh, and Mesh Model instances.

Aside from setting up the Mesh, Volume, and NiiVue widgets, this module
contains many of the classes needed to make NiiVue instances work, such as classes
to load objects in, change attributes of this instance, and more.
"""

import base64
import glob
import json
import math
import pathlib
import typing
import uuid
import warnings
from urllib.parse import urlparse

import anywidget
import ipywidgets
import numpy as np
import requests
import traitlets as t
from ipywidgets import CallbackDispatcher

from .config_options import ConfigOptions
from .constants import (
    ColormapType,
    SliceType,
)
from .serializers import (
    deserialize_colormap_label,
    deserialize_graph,
    deserialize_hdr,
    deserialize_mat4,
    deserialize_options,
    deserialize_volume_object_3d_data,
    parse_scene,
    serialize_colormap_label,
    serialize_enum,
    serialize_file,
    serialize_graph,
    serialize_hdr,
    serialize_ndarray,
    serialize_options,
    serialize_scene,
    serialize_to_none,
)
from .traits import (
    LUT,
    ColorMap,
    Graph,
    NIFTI1Hdr,
    Scene,
    VolumeObject3DData,
)
from .utils import (
    ChunkedDataHandler,
    lerp,
    make_draw_lut,
    make_label_lut,
    requires_canvas,
    sph2cart_deg,
)

__all__ = ["NiiVue"]


class BaseAnyWidget(anywidget.AnyWidget):
    """Base widget class that overrides set_state to handle chunked data."""

    _data_handlers: typing.ClassVar[dict] = {}
    _event_handlers: typing.ClassVar[dict] = {}

    _binary_trait_to_js_names: typing.ClassVar[dict] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._event_handlers = {}
        self._setup_binary_change_handlers()

    def set_state(self, state):
        """Override set_state to accept chunked-state attributes."""
        state_copy = state.copy()
        keys_to_remove = []

        for attr_name, attr_value in state.items():
            if attr_name.startswith("chunk_"):
                base, chunk_index = attr_name.rsplit("_", 1)
                data_property = base[6:]
                chunk_index = int(chunk_index)
                chunk_info = attr_value
                chunk_index_received = chunk_info["chunk_index"]
                total_chunks = chunk_info["total_chunks"]
                data_type = chunk_info["data_type"]
                chunk_data = chunk_info["chunk"]

                if isinstance(chunk_data, memoryview):
                    chunk_data = chunk_data.tobytes()
                elif isinstance(chunk_data, str):
                    chunk_data = base64.b64decode(chunk_data)
                else:
                    raise ValueError(f"Unsupported chunk data type: {type(chunk_data)}")

                if data_property not in self._data_handlers:
                    self._data_handlers[data_property] = ChunkedDataHandler(
                        total_chunks, data_type
                    )

                handler = self._data_handlers[data_property]
                handler.add_chunk(chunk_index_received, chunk_data)

                if handler.is_complete():
                    numpy_array = handler.get_numpy_array()
                    self.set_trait(data_property, numpy_array)
                    del self._data_handlers[data_property]

                keys_to_remove.append(attr_name)

        for key in keys_to_remove:
            del state_copy[key]

        super().set_state(state_copy)

    def _setup_binary_change_handlers(self):
        for trait_name in self._get_binary_traits():
            self.observe(self._handle_binary_trait_change, names=trait_name)

    def _get_binary_traits(self):
        return []

    def _get_js_name(self, trait_name):
        """Get the JavaScript attribute name for a trait."""
        return self._binary_trait_to_js_names.get(trait_name, trait_name)

    def _handle_binary_trait_change(self, change):
        trait_name = self._get_js_name(change["name"])
        old_value = change["old"]
        new_value = change["new"]
        if old_value is not None:
            if old_value.dtype != new_value.dtype:
                self.send(
                    {
                        "type": "buffer_change",
                        "data": {"attr": trait_name, "type": str(new_value.dtype)},
                    },
                    buffers=[new_value.tobytes()],
                )
            else:
                old_array = old_value.ravel()
                new_array = new_value.ravel()

                diff_indices = np.flatnonzero(new_array != old_array)

                if len(diff_indices) == 0:
                    return

                diff_values = new_array[diff_indices]

                indices_bytes = diff_indices.astype(np.uint32).tobytes()
                values_bytes = diff_values.tobytes()

                self.send(
                    {
                        "type": "buffer_update",
                        "data": {
                            "attr": trait_name,
                            "type": str(new_value.dtype),
                            "indices_type": "uint32",
                        },
                    },
                    buffers=[indices_bytes, values_bytes],
                )

        handler = self._event_handlers.get(f"{trait_name}_changed")
        if handler:
            handler(self)


class MeshLayer(BaseAnyWidget):
    """
    Represents a layer within a Mesh model.

    Parameters
    ----------
    path : str or pathlib.Path, optional
        Path to the volume data file. Cannot be modified once set.
    url : str, optional
        URL to the volume data.
    data : bytes, optional
        Bytes data of the volume.
    name : str, optional
        Name of the mesh.
    opacity : float, optional
        Opacity between 0.0 (transparent) and 1.0 (opaque). Default is 0.5.
    colormap : str, optional
        Colormap name for rendering. Default is 'warm'.
    colormap_negative : str, optional
        Colormap for negative values if `use_negative_cmap` is True.
        Default is 'winter'.
    colormap_type : :class:`ColormapType`, optional
        Colormap type used for the volume. Default is ``ColormapType.MIN_TO_MAX``.
    use_negative_cmap : bool, optional
        Use negative colormap for negative values. Default is False.
    cal_min : float or None, optional
        Minimum intensity value for brightness/contrast mapping.
    cal_max : float or None, optional
        Maximum intensity value for brightness/contrast mapping.
    outline_border : int, optional
        Outline border thickness. Default is 0.
    atlas_labels : list[str] or None, optional
        Read-only-ish: labels for atlas colormap (populated by the frontend).
    atlas_values : list[float] or None, optional
        Values mapping for atlas (set from Python, applied by the frontend)
    """

    path = t.Union(
        [t.Instance(pathlib.Path), t.Unicode()], default_value=None, allow_none=True
    ).tag(sync=True, to_json=serialize_file)
    url = t.Unicode(default_value=None, allow_none=True).tag(sync=True)
    data = t.Bytes(default_value=None, allow_none=True).tag(sync=True)

    id = t.Unicode(default_value="").tag(sync=True)
    name = t.Unicode(default_value="").tag(sync=True)
    opacity = t.Float(0.5).tag(sync=True)
    colormap = t.Unicode("warm").tag(sync=True)
    colormap_negative = t.Unicode("winter").tag(sync=True)
    use_negative_cmap = t.Bool(False).tag(sync=True)
    cal_min = t.Float(None, allow_none=True).tag(sync=True)
    cal_max = t.Float(None, allow_none=True).tag(sync=True)
    outline_border = t.Float(0).tag(sync=True)
    atlas_labels = t.List(t.Unicode(), default_value=None, allow_none=True).tag(
        sync=True
    )
    atlas_values = t.List(t.Float(), default_value=None, allow_none=True).tag(sync=True)

    # other properties that aren't in init
    colormap_invert = t.Bool(False).tag(sync=True)
    frame_4d = t.Int(0).tag(sync=True)
    colorbar_visible = t.Bool(True).tag(sync=True)
    colormap_type = t.UseEnum(ColormapType, default_value=ColormapType.MIN_TO_MAX).tag(
        sync=True, to_json=serialize_enum
    )
    is_additive_blend = t.Bool(False).tag(sync=True)

    def __init__(self, **kwargs):
        include_keys = {
            "path",
            "url",
            "data",
            "id",
            "opacity",
            "colormap",
            "colormap_negative",
            "use_negative_cmap",
            "cal_min",
            "cal_max",
            "outline_border",
            "atlas_labels",
            "atlas_values",
        }

        unknown_keys = set(kwargs.keys()) - include_keys
        if unknown_keys:
            warnings.warn(
                f"Ignored unsupported kwargs in {self.__class__.__name__}: "
                f"{list(unknown_keys)}",
                stacklevel=2,
            )

        filtered_kwargs = {k: v for k, v in kwargs.items() if k in include_keys}
        super().__init__(**filtered_kwargs)

        # Validate that one and only one of path, url, data is provided
        if not self.id:
            provided = [
                k for k in ("path", "url", "data") if getattr(self, k) is not None
            ]
            if len(provided) != 1:
                raise ValueError("Must provide only one of 'path', 'url', or 'data'.")

        # Set name if not provided
        # (here we assume that if ID is provided it's already been "loaded" somewhere)
        if not self.name and not self.id:
            if self.path:
                self.name = pathlib.Path(self.path).name
            elif self.url:
                self.name = pathlib.Path(urlparse(self.url).path).name
            elif self.data is not None:
                raise ValueError("Must provide 'name' when 'data' is provided.")
            else:
                raise ValueError("Cannot determine the name of the volume.")

        # set id
        if not self.id:
            self.id = str(uuid.uuid4()) + "_py"

    @t.validate(
        "path",
        "url",
        "data",
        "id",
    )
    def _validate_no_change(self, proposal):
        trait_name = proposal["trait"].name
        if (
            trait_name in self._trait_values
            and self._trait_values[trait_name]
            and self._trait_values[trait_name] != proposal["value"]
        ):
            raise t.TraitError(f"Cannot modify '{trait_name}' once set.")
        return proposal["value"]


class Mesh(BaseAnyWidget):
    """
    Represents a Mesh model.

    Parameters
    ----------
    path : str or pathlib.Path, optional
        Path to the volume data file. Cannot be modified once set.
    url : str, optional
        URL to the volume data.
    data : bytes, optional
        Bytes data of the volume.
    name : str, optional
        Name of the mesh.
    rgba255 : list of int, optional
        RGBA color as a list of four integers (0 to 255).
    opacity : float, optional
        Opacity between 0.0 (transparent) and 1.0 (opaque). Default is 1.0.
    visible : bool, optional
        Mesh visibility. Default is True.
    layers : list of dict or MeshLayer objects, optional
        List of layer data dictionaries or MeshLayer objects.
        See :class:`MeshLayer` for attribute options.
    """

    path = t.Union(
        [t.Instance(pathlib.Path), t.Unicode()], default_value=None, allow_none=True
    ).tag(sync=True, to_json=serialize_file)
    url = t.Unicode(default_value=None, allow_none=True).tag(sync=True)
    data = t.Bytes(default_value=None, allow_none=True).tag(sync=True)

    id = t.Unicode(default_value="").tag(sync=True)
    name = t.Unicode(default_value="").tag(sync=True)
    rgba255 = t.List([255, 255, 255, 255]).tag(sync=True)
    opacity = t.Float(1.0).tag(sync=True)
    visible = t.Bool(True).tag(sync=True)
    layers = t.List(t.Instance(MeshLayer), default_value=[]).tag(
        sync=True, **ipywidgets.widget_serialization
    )

    # other properties that aren't in init
    colormap_invert = t.Bool(False).tag(sync=True)
    colorbar_visible = t.Bool(True).tag(sync=True)
    mesh_shader_index = t.Int(default_value=0).tag(sync=True)
    legend_line_thickness = t.Float(0.0).tag(sync=True)
    edge_min = t.Float(2.0).tag(sync=True)
    edge_max = t.Float(6.0).tag(sync=True)
    edge_scale = t.Float(1.0).tag(sync=True)
    node_scale = t.Float(1.0).tag(sync=True)
    fiber_radius = t.Float(0.0).tag(sync=True)
    fiber_occlusion = t.Float(0.0).tag(sync=True)
    fiber_length = t.Float(2.0).tag(sync=True)
    fiber_dither = t.Float(0.1).tag(sync=True)
    fiber_color = t.Unicode("Global").tag(sync=True)
    fiber_decimation_stride = t.Int(1).tag(sync=True)
    colormap = t.Unicode(None, allow_none=True).tag(sync=True)

    # Set after bidirectional comms with frontend
    pts = t.Instance(np.ndarray, allow_none=True).tag(sync=True)
    tris = t.Instance(np.ndarray, allow_none=True).tag(sync=True)
    extents_min = t.List(t.Float()).tag(sync=True)
    extents_max = t.List(t.Float()).tag(sync=True)

    def __init__(self, **kwargs):
        include_keys = {
            "path",
            "url",
            "data",
            "id",
            "name",
            "rgba255",
            "opacity",
            "visible",
        }
        layers_data = kwargs.pop("layers", [])

        unknown_keys = set(kwargs.keys()) - include_keys
        if unknown_keys:
            warnings.warn(
                f"Ignored unsupported kwargs in {self.__class__.__name__}: "
                f"{list(unknown_keys)}",
                stacklevel=2,
            )

        filtered_kwargs = {k: v for k, v in kwargs.items() if k in include_keys}
        super().__init__(**filtered_kwargs)

        # Validate that one and only one of path, url, data is provided
        if not self.id:
            provided = [
                k for k in ("path", "url", "data") if getattr(self, k) is not None
            ]
            if len(provided) != 1:
                raise ValueError("Must provide only one of 'path', 'url', or 'data'.")

        # Set name if not provided
        # (here we assume that if ID is provided it's already been "loaded" somewhere)
        if not self.name and not self.id:
            if self.path:
                self.name = pathlib.Path(self.path).name
            elif self.url:
                self.name = pathlib.Path(urlparse(self.url).path).name
            elif self.data is not None:
                raise ValueError("Must provide 'name' when 'data' is provided.")
            else:
                raise ValueError("Cannot determine the name of the volume.")

        # set id
        if not self.id:
            self.id = str(uuid.uuid4()) + "_py"

        # accept either dicts or MeshLayer objs
        layers_list = []
        for layer in layers_data:
            if isinstance(layer, MeshLayer):
                layers_list.append(layer)
            elif isinstance(layer, dict):
                layers_list.append(MeshLayer(**layer))
        self.layers = layers_list

    def get_state(self, key=None, drop_defaults=False):
        """Exclude certain attributes from state on save."""
        state = super().get_state(key=key, drop_defaults=drop_defaults)
        if self.path or self.url or self.data:
            if "pts" in state:
                del state["pts"]
            if "tris" in state:
                del state["tris"]
        return state

    def _get_binary_traits(self):
        return ["pts", "tris"]

    @t.validate(
        "path",
        "url",
        "data",
        "id",
    )
    def _validate_no_change(self, proposal):
        trait_name = proposal["trait"].name
        if (
            trait_name in self._trait_values
            and self._trait_values[trait_name]
            and self._trait_values[trait_name] != proposal["value"]
        ):
            raise t.TraitError(f"Cannot modify '{trait_name}' once set.")
        return proposal["value"]

    def reverse_faces(self):
        """Reverse the winding order of the mesh faces."""
        self.send({"type": "reverse_faces", "data": []})


class Volume(BaseAnyWidget):
    """
    Represents a Volume model.

    Parameters
    ----------
    path : str or pathlib.Path, optional
        Path to the volume data file. Cannot be modified once set.
    url : str, optional
        URL to the volume data.
    data : bytes, optional
        Bytes data of the volume.
    paired_img_path : str or pathlib.Path, optional
        Path to the paired image data file.
    paired_img_url : str, optional
        URL to the paired image data.
    paired_img_data : bytes, optional
        Bytes data of the paired image.
    name : str, optional
        Name of the volume. If not provided, it will be inferred from the source.
    opacity : float, optional
        Opacity between 0.0 and 1.0 (default is 1.0).
    colormap : str, optional
        Colormap name (default is '').
    colorbar_visible : bool, optional
        Show colorbar (default is True).
    cal_min : float or None, optional
        Minimum intensity value for brightness/contrast mapping.
    cal_max : float or None, optional
        Maximum intensity value for brightness/contrast mapping.
    cal_min_neg : float or None, optional
        Minimum (most negative) intensity for negative-value colormap mapping.
    cal_max_neg : float or None, optional
        Maximum (least negative) intensity for negative-value colormap mapping.
    frame_4d : int, optional
        Frame index for 4D volume data (default is 0).
    colormap_negative : str, optional
        Colormap for negative values (default is '').
    colormap_label : :class:`LUT`, optional
        Colormap label data.
    colormap_type : :class:`ColormapType`, optional
        Colormap type used for the volume. Default is ``ColormapType.MIN_TO_MAX``.
    """

    # Input-only traits (not accessible after initialization)
    path = t.Union(
        [t.Instance(pathlib.Path), t.Unicode()], default_value=None, allow_none=True
    ).tag(sync=True, to_json=serialize_file)
    url = t.Unicode(default_value=None, allow_none=True).tag(sync=True)
    data = t.Bytes(default_value=None, allow_none=True).tag(sync=True)
    paired_img_path = t.Union(
        [t.Instance(pathlib.Path), t.Unicode()], default_value=None, allow_none=True
    ).tag(sync=True, to_json=serialize_file)
    paired_img_url = t.Unicode(default_value=None, allow_none=True).tag(sync=True)
    paired_img_data = t.Bytes(default_value=None, allow_none=True).tag(sync=True)

    # Main traits
    id = t.Unicode(default_value="").tag(sync=True)
    name = t.Unicode(default_value="").tag(sync=True)
    opacity = t.Float(1.0).tag(sync=True)
    colormap = t.Unicode("").tag(sync=True)
    colorbar_visible = t.Bool(True).tag(sync=True)
    cal_min = t.Float(None, allow_none=True).tag(sync=True)
    cal_max = t.Float(None, allow_none=True).tag(sync=True)
    cal_min_neg = t.Float(None, allow_none=True).tag(sync=True)
    cal_max_neg = t.Float(None, allow_none=True).tag(sync=True)
    frame_4d = t.Int(0).tag(sync=True)
    colormap_negative = t.Unicode("").tag(sync=True)
    colormap_label = t.Instance(LUT, allow_none=True).tag(
        sync=True,
        to_json=serialize_colormap_label,
        from_json=deserialize_colormap_label,
    )
    colormap_type = t.UseEnum(ColormapType, default_value=ColormapType.MIN_TO_MAX).tag(
        sync=True, to_json=serialize_enum
    )

    # Other properties
    colormap_invert = t.Bool(False).tag(sync=True)
    n_frame_4d = t.Int(None, allow_none=True).tag(sync=True)  # readonly after set
    modulation_image = t.Int(None, allow_none=True).tag(sync=True)
    modulate_alpha = t.Int(0).tag(sync=True)

    # Set after bidirectional comms with frontend
    hdr = t.Instance(NIFTI1Hdr, allow_none=True).tag(
        sync=True, to_json=serialize_hdr, from_json=deserialize_hdr
    )  # currently only supports frontend->backend communication
    img = t.Instance(np.ndarray, allow_none=True).tag(
        sync=True, to_json=serialize_ndarray
    )
    dims = t.Tuple(allow_none=True).tag(sync=True)
    extents_min_ortho = t.List(t.Float()).tag(sync=True)
    extents_max_ortho = t.List(t.Float()).tag(sync=True)
    frac2mm = t.Instance(np.ndarray, allow_none=True).tag(
        sync=True, to_json=serialize_to_none, from_json=deserialize_mat4
    )
    frac2mm_ortho = t.Instance(np.ndarray, allow_none=True).tag(
        sync=True, to_json=serialize_to_none, from_json=deserialize_mat4
    )
    dims_ras = t.List(t.Float()).tag(sync=True)
    mat_ras = t.Instance(np.ndarray, allow_none=True).tag(
        sync=True, to_json=serialize_to_none, from_json=deserialize_mat4
    )

    def __init__(self, **kwargs):
        include_keys = {
            "path",
            "url",
            "data",
            "paired_img_path",
            "paired_img_url",
            "paired_img_data",
            "id",
            "name",
            "opacity",
            "colormap",
            "colorbar_visible",
            "cal_min",
            "cal_max",
            "cal_min_neg",
            "cal_max_neg",
            "frame_4d",
            "colormap_negative",
            "colormap_label",
            "colormap_type",
        }

        unknown_keys = set(kwargs.keys()) - include_keys
        if unknown_keys:
            warnings.warn(
                f"Ignored unsupported kwargs in {self.__class__.__name__}: "
                f"{list(unknown_keys)}",
                stacklevel=2,
            )

        filtered_kwargs = {k: v for k, v in kwargs.items() if k in include_keys}
        super().__init__(**filtered_kwargs)

        # Validate that one and only one of path, url, data is provided
        if not self.id:
            provided = [
                k for k in ("path", "url", "data") if getattr(self, k) is not None
            ]
            if len(provided) != 1:
                raise ValueError("Must provide only one of 'path', 'url', or 'data'.")

        # Validate paired image data
        paired_provided = [
            k
            for k in ("paired_img_path", "paired_img_url", "paired_img_data")
            if getattr(self, k) is not None
        ]
        if len(paired_provided) > 1:
            raise ValueError(
                "Up to one of 'paired_img_path', "
                "'paired_img_url', or 'paired_img_data' can be provided."
            )

        # Set name if not provided
        # (here we assume that if ID is provided it's already been "loaded" somewhere)
        if not self.name and not self.id:
            if self.path:
                self.name = pathlib.Path(self.path).name
            elif self.url:
                self.name = pathlib.Path(urlparse(self.url).path).name
            elif self.data is not None:
                raise ValueError("Must provide 'name' when 'data' is provided.")
            else:
                raise ValueError("Cannot determine the name of the volume.")

        # set id
        if not self.id:
            self.id = str(uuid.uuid4()) + "_py"

    def get_state(self, key=None, drop_defaults=False):
        """Exclude certain attributes from state on save."""
        state = super().get_state(key=key, drop_defaults=drop_defaults)
        if self.path or self.url or self.data:
            if "img" in state:
                del state["img"]
        return state

    def _get_binary_traits(self):
        return ["img"]

    @t.validate(
        "path",
        "url",
        "data",
        "id",
        "paired_img_path",
        "paired_img_url",
        "paired_img_data",
    )
    def _validate_no_change(self, proposal):
        trait_name = proposal["trait"].name
        if (
            trait_name in self._trait_values
            and self._trait_values[trait_name]
            and self._trait_values[trait_name] != proposal["value"]
        ):
            raise t.TraitError(f"Cannot modify '{trait_name}' once set.")
        return proposal["value"]

    @t.validate("n_frame_4d")
    def _validate_nframe4d(self, proposal):
        # separate since n_frame_4d can be 0
        if (
            "n_frame_4d" in self._trait_values
            and self.n_frame_4d is not None
            and self.n_frame_4d != proposal["value"]
        ):
            raise t.TraitError("Cannot modify 'n_frame_4d' once set.")
        return proposal["value"]

    def _notify_colormap_label_changed(self):
        self.notify_change(
            {
                "name": "colormap_label",
                "old": self.colormap_label,
                "new": self.colormap_label,
                "owner": self,
                "type": "change",
            }
        )

    def set_colormap_label(self, colormap_data: dict):
        """Set colormap label for the volume.

        Parameters
        ----------
        colormap_data : dict
            The colormap dict data.

            Colormaps contain the following keys ('R', 'G', 'B' are required):

            - R
            - G
            - B
            - A
            - I
            - min
            - max
            - labels

        Examples
        --------
        ::

            nv.volumes[0].set_colormap_label(colormap_data)
        """
        if isinstance(colormap_data, dict):
            colormap = ColorMap(**colormap_data)
            lut = make_label_lut(colormap)
            lut._parent = self
            self.colormap_label = lut
        else:
            raise TypeError("colormap_data must be a dict.")

    def set_colormap_label_from_url(self, url):
        """Set colormap label from a URL.

        Parameters
        ----------
        url : str
            The colormap json url.

        Examples
        --------
        ::

            nv.volumes[0].set_colormap_label_from_url(url)
        """
        response = requests.get(url)
        response.raise_for_status()
        cmap = response.json()
        self.set_colormap_label(cmap)

    def save_to_disk(self, filename="image.nii"):
        """Generate the NIfTI file data and triggers a browser download.

        Parameters
        ----------
        filename : str, optional
            The filename (default: "image.nii").
        """
        self.send({"type": "save_to_disk", "data": [filename]})

    def convert_frac2mm(self, frac: list, is_force_slice_mm: bool = False) -> list:
        """
        Convert fractional volume coordinates to millimeter space.

        Parameters
        ----------
        frac : list of float
            Fractional coordinates [X, Y, Z] in the range [0, 1].
        is_force_slice_mm : bool, optional
            If True, use world space coordinates. If False, use orthogonal space.
            Default is False.

        Returns
        -------
        list of float
            Position in millimeters [X, Y, Z, W] where W is always 1.

        Raises
        ------
        RuntimeError
            If the volume data is not fully loaded.

        Examples
        --------
        ::

            mm_pos = volume.convert_frac2mm([0.5, 0.5, 0.5])
        """
        if self.frac2mm is None or self.frac2mm_ortho is None:
            raise RuntimeError(
                "Volume coordinate transformation matrices are not available. "
                "Ensure canvas is attached."
            )

        pos = [frac[0], frac[1], frac[2], 1.0]

        if is_force_slice_mm:
            matrix = self.frac2mm.T
        else:
            matrix = self.frac2mm_ortho.T

        result = np.dot(matrix, pos)
        return result.tolist()

    def convert_mm2frac(self, mm: list, is_force_slice_mm: bool = False) -> list:
        """
        Convert millimeter coordinates to fractional volume coordinates.

        Parameters
        ----------
        mm : list of float
            Position in millimeters [X, Y, Z] or [X, Y, Z, W].
        is_force_slice_mm : bool, optional
            If True, use world space coordinates. If False, use orthogonal space.
            Default is False.

        Returns
        -------
        list of float
            Fractional coordinates [X, Y, Z] in the range [0, 1].

        Raises
        ------
        RuntimeError
            If the volume data is not fully loaded.

        Examples
        --------
        ::

            frac_pos = volume.convert_mm2frac([10.0, 20.0, 30.0])
        """
        if len(mm) == 3:
            mm4 = [mm[0], mm[1], mm[2], 1.0]
        else:
            mm4 = list(mm[:4])

        frac = [0.0, 0.0, 0.0]

        if not is_force_slice_mm:
            # Use orthogonal space
            if self.frac2mm_ortho is None:
                raise RuntimeError(
                    "Volume orthogonal transformation matrix is not available. "
                    "Ensure canvas is attached."
                )
            matrix = self.frac2mm_ortho.T
            inv_matrix = np.linalg.inv(matrix)
            result = np.dot(inv_matrix, mm4)
            frac = result[:3].tolist()
        else:
            # Use world space with RAS coordinates
            if self.dims_ras is None or self.mat_ras is None:
                raise RuntimeError(
                    "Volume RAS dimensions or matrix not available. "
                    "Ensure the volume is fully loaded."
                )

            d = self.dims_ras
            if d[1] < 1 or d[2] < 1 or d[3] < 1:
                return frac

            sform = self.mat_ras.T
            sform = np.linalg.inv(sform)
            sform = sform.T

            result = np.dot(sform, mm4)
            frac[0] = (result[0] + 0.5) / d[1]
            frac[1] = (result[1] + 0.5) / d[2]
            frac[2] = (result[2] + 0.5) / d[3]

        return frac


class NiiVue(BaseAnyWidget):
    """
    Represents a NiiVue widget instance.

    This class provides a Jupyter widget for visualizing neuroimaging data using
    NiiVue.
    """

    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"

    _binary_trait_to_js_names: typing.ClassVar[dict] = {"draw_bitmap": "drawBitmap"}

    height = t.Int().tag(sync=True)
    opts = t.Instance(ConfigOptions).tag(
        sync=True, to_json=serialize_options, from_json=deserialize_options
    )
    volumes = t.List(t.Instance(Volume), default_value=[]).tag(
        sync=True, **ipywidgets.widget_serialization
    )
    meshes = t.List(t.Instance(Mesh), default_value=[]).tag(
        sync=True, **ipywidgets.widget_serialization
    )

    _canvas_attached = t.Bool(False).tag(sync=True)
    _volume_object_3d_data = t.Instance(VolumeObject3DData, allow_none=True).tag(
        sync=True,
        to_json=serialize_to_none,
        from_json=deserialize_volume_object_3d_data,
    )

    this_model_id = t.Unicode().tag(sync=True)

    # other props
    background_masks_overlays = t.Int(0).tag(sync=True)
    draw_lut = t.Instance(LUT, allow_none=True).tag(
        sync=True,
        to_json=serialize_colormap_label,
        from_json=deserialize_colormap_label,
    )
    draw_opacity = t.Float(0.8).tag(sync=True)
    draw_fill_overwrites = t.Bool(True).tag(sync=True)
    graph = t.Instance(Graph, allow_none=True).tag(
        sync=True,
        to_json=serialize_graph,
        from_json=deserialize_graph,
    )
    scene = t.Instance(Scene, allow_none=True).tag(
        sync=True,
        to_json=serialize_scene,
    )
    overlay_outline_width = t.Float(0.0).tag(sync=True)  # 0 for none
    overlay_alpha_shader = t.Float(1.0).tag(sync=True)  # 1 for opaque

    other_nv = t.List(t.Instance(object, allow_none=False), default_value=[]).tag(
        sync=False
    )

    draw_bitmap = t.Instance(np.ndarray, allow_none=True).tag(
        sync=True, to_json=serialize_ndarray
    )

    @t.validate("other_nv")
    def _validate_other_nv(self, proposal):
        value = proposal["value"]
        for nv_inst in value:
            if nv_inst is self:
                raise t.TraitError("Cannot sync to self.")
            if (
                f"{type(nv_inst).__module__}.{type(nv_inst).__qualname__}"
                != "ipyniivue.widget.NiiVue"
            ):
                raise t.TraitError(
                    "All items in `other_nv` must be NiiVue instances."
                    + str(type(self))
                )
        return value

    def __init__(self, height: int = 300, **options):  # noqa: D417
        r"""
        Initialize the NiiVue widget.

        **Note:** See the :meth:`NiiVue.close` method to close
        the NiiVue widget and free up resources.

        Parameters
        ----------
        height : int, optional
            The height of the widget in pixels (default: 300).
        \*\*options : dict, optional
            Additional keyword arguments to configure the NiiVue widget.
            See :class:`ipyniivue.config_options.ConfigOptions` for all options.
        """
        # Get options
        opts = ConfigOptions(parent=self, **options)
        super().__init__(height=height, opts=opts, volumes=[], meshes=[])

        # Initialize values
        self.this_model_id = self._model_id
        self._cluts = self._get_initial_colormaps()
        self.graph = Graph(parent=self)
        self.scene = Scene(parent=self)
        self.other_nv = []
        self.sync_opts = {
            "3d": False,
            "2d": False,
            "zoom_pan": False,
            "cal_min": False,
            "cal_max": False,
            "clip_plane": False,
            "gamma": False,
            "slice_type": False,
            "crosshair": False,
        }

        # Handle messages coming from frontend
        self.on_msg(self._handle_custom_msg)

    def _get_binary_traits(self):
        return ["draw_bitmap"]

    def set_state(self, state):
        """Override set_state to silence notifications for certain updates."""
        if "scene" in state:
            parsed = parse_scene(state["scene"])
            self.scene._trait_values.update(parsed)
            self.sync()
            return
        return super().set_state(state)

    def _notify_opts_changed(self):
        self.notify_change(
            {
                "name": "opts",
                "old": self.opts,
                "new": self.opts,
                "owner": self,
                "type": "change",
            }
        )
        self.send({"type": "update_gl_volume", "data": []})

    def _notify_graph_changed(self):
        self.notify_change(
            {
                "name": "graph",
                "old": self.graph,
                "new": self.graph,
                "owner": self,
                "type": "change",
            }
        )
        self.send({"type": "update_gl_volume", "data": []})

    def _notify_scene_changed(self):
        self.notify_change(
            {
                "name": "scene",
                "old": self.scene,
                "new": self.scene,
                "owner": self,
                "type": "change",
            }
        )
        self.send({"type": "draw_scene", "data": []})

    def _register_callback(self, event_name, callback, remove=False):
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = CallbackDispatcher()

        self._event_handlers[event_name].register_callback(callback, remove=remove)

    def _handle_custom_msg(self, content, buffers):
        event = content.get("event", "")
        data = content.get("data", {})

        # handle add_volume and add_mesh events separately
        if event == "add_volume":
            self._add_volume_from_frontend(data)
            return
        elif event == "add_mesh":
            self._add_mesh_from_frontend(data)
            return

        # check if the event has a registered handler
        handler = self._event_handlers.get(event)
        if not handler:
            return

        # handle events that require specific processing
        if event == "document_loaded":
            self.volumes = [i for i in self.volumes if i.id in data["volumes"]]
            self.meshes = [i for i in self.meshes if i.id in data["meshes"]]
        if event == "azimuth_elevation_change":
            handler(data["azimuth"], data["elevation"])
        elif event == "frame_change":
            idx = self.get_volume_index_by_id(data["id"])
            if idx != -1:
                handler(self.volumes[idx], data["frame_index"])
        elif event == "intensity_change":
            idx = self.get_volume_index_by_id(data["id"])
            if idx != -1:
                handler(self.volumes[idx])
            else:
                handler(data)
        elif event == "image_loaded":
            idx = self.get_volume_index_by_id(data["id"])
            if idx != -1:
                volume = self.volumes[idx]

                # set other traits available on-loaded
                for key, value in data.items():
                    if (
                        key != "id"
                        and not key.startswith("_")
                        and key in volume.trait_names()
                    ):
                        volume.set_trait(key, value)

                # only fire loaded event once certain traits are defined
                if volume.img is not None and volume.hdr is not None:
                    handler(volume)
                else:

                    def check_ready(change):
                        if volume.img is not None and volume.hdr is not None:
                            volume.unobserve(check_ready, names=["img", "hdr"])
                            handler(volume)

                    volume.observe(check_ready, names=["img", "hdr"])
            else:
                handler(data)
        elif event == "mesh_loaded":
            idx = self.get_mesh_index_by_id(data["id"])
            if idx != -1:
                mesh = self.meshes[idx]

                # set other traits available on-loaded
                for key, value in data.items():
                    if (
                        key != "id"
                        and not key.startswith("_")
                        and key in mesh.trait_names()
                    ):
                        mesh.set_trait(key, value)

                # only fire loaded event once certain traits are defined
                if mesh.pts is not None and mesh.tris is not None:
                    handler(mesh)
                else:

                    def check_ready(change):
                        if mesh.pts is not None and mesh.tris is not None:
                            mesh.unobserve(check_ready, names=["pts", "tris"])
                            handler(mesh)

                    mesh.observe(check_ready, names=["pts", "tris"])
            else:
                handler(data)
        elif event == "mesh_added_from_url":
            mesh_options = {"url": data["url"], "headers": data["headers"]}
            handler(mesh_options, data["mesh"])
        elif event == "volume_added_from_url":
            image_options = {"url": data["url"], "headers": data["headers"]}
            handler(image_options, data["volume"])
        else:
            handler(data)

    def _handle_image_loaded(self, volume_id):
        handler = self._event_handlers.get("image_loaded")
        if not handler:
            return

        # ensure that volume actually exists in parent
        idx = self.get_volume_index_by_id(volume_id)
        if idx != -1:
            handler(self.volumes[idx])
        else:
            handler({"id": volume_id})

    def _add_volume_from_frontend(self, volume_data):
        index = volume_data.pop("index", None)
        volume = Volume(**volume_data)
        if index is not None and 0 <= index <= len(self.volumes):
            self.volumes = [*self.volumes[:index], volume, *self.volumes[index:]]
        else:
            self.volumes = [*self.volumes, volume]

    def _add_mesh_from_frontend(self, mesh_data):
        index = mesh_data.pop("index", None)
        layers_data = mesh_data.pop("layers", [])
        mesh = Mesh(**mesh_data)
        mesh.layers = [MeshLayer(**layer_data) for layer_data in layers_data]
        if index is not None and 0 <= index <= len(self.meshes):
            self.meshes = [*self.meshes[:index], mesh, *self.meshes[index:]]
        else:
            self.meshes = [*self.meshes, mesh]

    def close(self):
        """
        Close the NiiVue widget and free up resources.

        This method disposes of the widget on both the frontend and backend.
        After calling this method, the widget will no longer be usable.

        Examples
        --------
        ::

            nv = NiiVue()
            # use nv ...
            nv.close()
        """
        super().close()

    def get_volume_index_by_id(self, volume_id: str) -> int:
        """Return the index of the volume with the given id.

        Parameters
        ----------
        volume_id : str
            The id of the volume.
        """
        for idx, vol in enumerate(self.volumes):
            if vol.id == volume_id:
                return idx
        return -1

    def get_mesh_index_by_id(self, mesh_id: str) -> int:
        """Return the index of the mesh with the given id.

        Parameters
        ----------
        mesh_id : str
            The id of the mesh.
        """
        for idx, mesh in enumerate(self.meshes):
            if mesh.id == mesh_id:
                return idx
        return -1

    def load_volumes(self, volumes: list):
        """
        Load a list of volume objects.

        Parameters
        ----------
        volumes : list
            A list of dictionaries or Volume objects.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv = NiiVue()
            nv.load_volumes([{"path": "mni152.nii.gz"}])

        """
        volume_objects = []
        for item in volumes:
            if isinstance(item, Volume):
                volume_objects.append(item)
            elif isinstance(item, dict):
                volume_objects.append(Volume(**item))
        self.volumes = volume_objects

    def add_volume(self, volume: typing.Union[dict, Volume]):
        """
        Add a new volume to the widget.

        Parameters
        ----------
        volume : dict or Volume object
            The volume information.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv = NiiVue()
            nv.add_volume({"path": "mni152.nii.gz"})

        """
        if isinstance(volume, Volume):
            new_volume = volume
        elif isinstance(volume, dict):
            new_volume = Volume(**volume)
        else:
            return
        self.volumes = [*self.volumes, new_volume]

    def load_meshes(self, meshes: list):
        """
        Load a list of meshes objects.

        Parameters
        ----------
        meshes : list
            A list of dictionaries containing the mesh information.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv = NiiVue()
            nv.load_meshes([{"path": "BrainMesh_ICBM152.lh.mz3"}])

        """
        mesh_objects = []
        for item in meshes:
            if isinstance(item, Mesh):
                mesh_objects.append(item)
            elif isinstance(item, dict):
                mesh_objects.append(Mesh(**item))
        self.meshes = mesh_objects

    def add_mesh(self, mesh: typing.Union[dict, Volume]):
        """
        Add a single mesh to the widget.

        Parameters
        ----------
        mesh : dict
            A dictionary containing the mesh information.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv = NiiVue()
            nv.add_mesh({"path": "BrainMesh_ICBM152.lh.mz3"})

        """
        if isinstance(mesh, Mesh):
            new_mesh = mesh
        elif isinstance(mesh, dict):
            new_mesh = Mesh(**mesh)
        else:
            return
        self.meshes = [*self.meshes, new_mesh]

    """
    Other functions
    """

    def save_document(self, file_name: str = "document.nvd", compress: bool = True):
        """
        Save the entire scene with settings as a document.

        Parameters
        ----------
        file_name : str
            The file name to save the document as.
        compress : bool
            A value represneing if the file should be compressed.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv.save_document("mydoc.nvd", False)

        """
        self.send({"type": "save_document", "data": [file_name, compress]})

    def save_html(self, file_name: str = "untitled.html", canvas_id: str = "gl1"):
        """
        Save the current instance as an html page.

        Parameters
        ----------
        file_name : str
            The file name to save the page as.
        canvas_id : str
            The id of the canvas that NiiVue will be attached to.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv.save_html("mypage.html")

        """
        self.send({"type": "save_html", "data": [file_name, canvas_id]})

    def save_image(
        self,
        file_name: str = "image.nii.gz",
        is_save_drawing: bool = False,
        volume_by_index: int = 0,
    ):
        """
        Save the current image as a nii file.

        Parameters
        ----------
        file_name : str
            The file name to save the image as.
        is_save_drawing : bool
            A value representing if the drawings should be saved.
        volume_by_index : int
            The volume layer which should be saved (0 for background)

        Returns
        -------
        None

        Examples
        --------
        ::

            nv.save_image("myimage.nii.gz", True, 2)

        """
        self.send(
            {
                "type": "save_image",
                "data": [file_name, is_save_drawing, volume_by_index],
            }
        )

    def save_scene(self, file_name: str = "scene.png"):
        """
        Save the current scene with the provided file name.

        Parameters
        ----------
        file_name : str
            The file name to save the scene as.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv.save_scene("myscene.png")

        """
        self.send({"type": "save_scene", "data": [file_name]})

    def set_mesh_property(self, mesh_id: str, attribute: str, value: typing.Any):
        """Set a property of a mesh.

        Parameters
        ----------
        mesh_id : str
            Identifier of the mesh to change (mesh id).
        attribute : str
            The attribute to change.
        value : Any
            The value to set.

        Raises
        ------
        ValueError
            If the attribute is not allowed or the mesh is not found.

        Examples
        --------
        ::

            nv.set_mesh_property(nv.meshes[0].id, 'opacity', 0.5)
        """
        allowed_attributes = [
            name
            for name, trait in Mesh.__dict__.items()
            if isinstance(trait, t.TraitType)
            and not name.startswith("_")
            and name not in {"id", "path"}
        ]

        if attribute not in allowed_attributes:
            raise ValueError(
                f"Attribute '{attribute}' is not allowed. "
                f"Allowed attributes are: {', '.join(allowed_attributes)}."
            )

        idx = self.get_mesh_index_by_id(mesh_id)
        if idx == -1:
            raise ValueError(f"Mesh with id '{mesh_id}' not found.")

        mesh = self.meshes[idx]
        setattr(mesh, attribute, value)

    def get_mesh_layer_property(self, mesh_id: str, layer_index: int, attribute: str):
        """Return the value of a mesh layer property.

        Parameters
        ----------
        mesh_id : str
            Identifier of the mesh to query.
        layer_index : int
            Index of the layer within the mesh.
        attribute : str
            Name of the attribute to retrieve.

        Returns
        -------
        Any
            The current value of the requested attribute.

        Raises
        ------
        ValueError
            If the attribute is not allowed or the mesh is not found.
        IndexError
            If the layer index is out of range.

        Notes
        -----
        This method provides the same result as directly accessing the
        property via::

            val = nv.meshes[0].layers[0].opacity

        but adds validation safeguards. Specifically, it verifies that
        the requested attribute is a defined and allowed trait, that the
        mesh ID exists, and that the requested layer index is valid. Use
        this method when you need a safe, validated query for arbitrary
        attributes.

        Examples
        --------
        ::
            val = nv.get_mesh_layer_property(nv.meshes[0].id, 0, 'opacity')
        """
        allowed_attributes = [
            name
            for name, trait in MeshLayer.__dict__.items()
            if isinstance(trait, t.TraitType)
            and not name.startswith("_")
            and name not in {"id", "path"}
        ]

        if attribute not in allowed_attributes:
            raise ValueError(
                f"Attribute '{attribute}' is not allowed. "
                f"Allowed attributes are: {', '.join(allowed_attributes)}."
            )

        idx = self.get_mesh_index_by_id(mesh_id)
        if idx == -1:
            raise ValueError(f"Mesh with id '{mesh_id}' not found.")

        mesh = self.meshes[idx]
        if layer_index < 0 or layer_index >= len(mesh.layers):
            raise IndexError(f"Layer index {layer_index} out of range.")

        layer = mesh.layers[layer_index]
        return getattr(layer, attribute)

    def set_mesh_layer_property(
        self, mesh_id: str, layer_index: int, attribute: str, value: typing.Any
    ):
        """Set a property of a mesh layer.

        Parameters
        ----------
        mesh_id : str
            Identifier of the mesh to change (mesh id).
        layer_index : int
            The index of the layer within the mesh.
        attribute : str
            The attribute to change.
        value : Any
            The value to set.

        Raises
        ------
        ValueError
            If the attribute is not allowed or the mesh is not found.
        IndexError
            If the layer index is out of range.

        Examples
        --------
        ::

            nv.set_mesh_layer_property(nv.meshes[0].id, 0, 'opacity', 0.5)
        """
        allowed_attributes = [
            name
            for name, trait in MeshLayer.__dict__.items()
            if isinstance(trait, t.TraitType)
            and not name.startswith("_")
            and name not in {"id", "path"}
        ]

        if attribute not in allowed_attributes:
            raise ValueError(
                f"Attribute '{attribute}' is not allowed. "
                f"Allowed attributes are: {', '.join(allowed_attributes)}."
            )

        idx = self.get_mesh_index_by_id(mesh_id)
        if idx == -1:
            raise ValueError(f"Mesh with id '{mesh_id}' not found.")

        mesh = self.meshes[idx]
        if layer_index < 0 or layer_index >= len(mesh.layers):
            raise IndexError(f"Layer index {layer_index} out of range.")

        layer = mesh.layers[layer_index]
        setattr(layer, attribute, value)

    def _get_initial_colormaps(self):
        colormaps_dir = pathlib.Path(__file__).parent / "static" / "colormaps"

        if not colormaps_dir.is_dir():
            return {}

        colormap_files = glob.glob(str(colormaps_dir / "*.json"))

        cluts = {}
        for f in colormap_files:
            file = pathlib.Path(f)
            cmap_name = file.stem
            file_data = json.loads(file.read_text())
            try:
                cluts[cmap_name.lower()] = ColorMap(**file_data)
            except t.TraitError:
                pass

        return cluts

    def colormaps(self):
        """Retrieve the list of available colormap names.

        Returns
        -------
        list of str
            A list containing the names of all available colormaps

        Examples
        --------
        ::

            colormaps = nv.colormaps()
        """
        exclude = {"$itksnap", "$slicer3d"}
        return [cmap for cmap in self._cluts.keys() if cmap not in exclude]

    def add_colormap(self, name: str, color_map: dict):
        """Add a colormap to the widget.

        Parameters
        ----------
        name : str
            The name of the colormap.
        color_map : dict
            The colormap data.

        Raises
        ------
        ValueError
            If the colormap does not meet the required format.
        TypeError
            If the colormap values are not of the correct type.

        Examples
        --------
        ::

            nv.add_colormap("custom_color_map", {
                "R": [0, 255, 0],
                "G": [0, 0, 255],
                "B": [0, 0, 0],
                "A": [0, 64, 64],
                "I": [0, 85, 255]
            })
            nv.set_colormap(nv.volumes[0].id, "custom_color_map")
        """
        self._cluts[name.lower()] = ColorMap(**color_map)

        # Send the colormap to the frontend
        self.send({"type": "add_colormap", "data": [name.lower(), color_map]})

    def set_colormap(self, image_id: str, colormap: str):
        """Set the colormap for a volume.

        Parameters
        ----------
        image_id : str
            The ID of the volume.
        colormap : str
            The name of the colormap to set.

        Raises
        ------
        ValueError
            If the volume with the given ID is not found.

        Examples
        --------
        ::

            nv.set_colormap(nv.volumes[0].id, "green2cyan")
        """
        idx = self.get_volume_index_by_id(image_id)
        if idx != -1:
            self.volumes[idx].colormap = colormap
        else:
            raise ValueError(f"Volume with ID '{image_id}' not found")

    def set_selection_box_color(self, color: tuple):
        """Set the selection box color.

        Parameters
        ----------
        color : tuple of floats
            An RGBA array with values ranging from 0 to 1.

        Raises
        ------
        ValueError
            If the color is not a list of four numeric values.

        Examples
        --------
        ::

            nv.set_selection_box_color((0, 1, 0, 0.7))
        """
        if not isinstance(color, (list, tuple)) or len(color) != 4:
            raise ValueError(
                "Color must be a list or tuple of four numeric values (RGBA)."
            )
        if not all(isinstance(c, (int, float)) and 0 <= c <= 1 for c in color):
            raise ValueError("Each color component must be a number between 0 and 1.")

        self.opts.selection_box_color = tuple(color)

    def set_clip_plane_color(self, color: tuple):
        """Set the clip plane color.

        Parameters
        ----------
        color : tuple of floats
            An RGBA array where the RGB components range from 0 to 1,
            and the A (alpha) component can range from -1 to 1.
            A negative alpha value means the color appears inside the volume.

        Raises
        ------
        ValueError
            If the color is not a tuple/list of four numeric values
            or any component is outside the valid range.

        Examples
        --------
        ::

            nv.set_clip_plane_color((0, 1, 0, -0.7))
        """
        if not isinstance(color, (list, tuple)) or len(color) != 4:
            raise ValueError("Color must be have four numeric values (RGBA).")

        # Validate RGB (0..1) and A (-1..1)
        r, g, b, a = color
        if not all(isinstance(c, (int, float)) for c in color):
            raise ValueError("Each color component must be numeric (int or float).")

        if not (0.0 <= r <= 1.0 and 0.0 <= g <= 1.0 and 0.0 <= b <= 1.0):
            raise ValueError("RGB components must each be between 0 and 1.")

        if not (-1.0 <= a <= 1.0):
            raise ValueError("Alpha component must be between -1 and 1.")

        self.opts.clip_plane_color = tuple(color)

    def set_crosshair_color(self, color: tuple):
        """Set the crosshair and colorbar outline color.

        Parameters
        ----------
        color : tuple of floats
            An RGBA array with values ranging from 0 to 1.

        Raises
        ------
        ValueError
            If the color is not a list of four numeric values.

        Examples
        --------
        ::

            nv.set_crosshair_color((0, 1, 0, 1))
        """
        if not isinstance(color, (list, tuple)) or len(color) != 4:
            raise ValueError(
                "Color must be a list or tuple of four numeric values (RGBA)."
            )
        if not all(isinstance(c, (int, float)) and 0 <= c <= 1 for c in color):
            raise ValueError("Each color component must be a number between 0 and 1.")

        self.opts.crosshair_color = tuple(color)

    def set_crosshair_width(self, width: int):
        """Set the crosshair width.

        Parameters
        ----------
        width : int
            The width of the crosshair in pixels.

        Examples
        --------
        ::

            nv.set_crosshair_width(3)
        """
        self.opts.crosshair_width = width

    def set_gamma(self, gamma: float = 1.0):
        """Adjust screen gamma.

        Parameters
        ----------
        gamma : float
            Selects luminance

        Raises
        ------
        TypeError
            If gamma is not a number

        Examples
        --------
        ::

            nv.set_gamma(3.0)
        """
        if not isinstance(gamma, (int, float)):
            raise TypeError("gamma must be a number")

        self.scene.gamma = gamma
        self.send({"type": "set_gamma", "data": [gamma]})

    def set_slice_type(self, slice_type: SliceType):
        """Set the type of slice display.

        Parameters
        ----------
        slice_type : SliceType
            The type of slice display.

        Raises
        ------
        TypeError
            If slice_type is not a valid SliceType.

        Examples
        --------
        ::

            nv.set_slice_type(SliceType.AXIAL)
        """
        self.opts.slice_type = slice_type

    def set_clip_plane(self, depth: float, azimuth: float, elevation: float):
        """Update the clip plane orientation in 3D view mode.

        Parameters
        ----------
        depth : float
            distance of clip plane from the center of the volume
        azimuth : float
            camera position in degrees around the object
        elevation : float
            camera height in degrees

        Raises
        ------
        TypeError
            If any of the inputs are not a number.

        Examples
        --------
        ::

            nv.set_clip_plane(2.0, 42.0, 42.0)
        """
        # Verify that all inputs are numeric types
        if not all(isinstance(x, (int, float)) for x in [depth, azimuth, elevation]):
            raise TypeError("depth, azimuth, and elevation must all be numeric values.")
        v = sph2cart_deg(azimuth + 180, elevation)
        self.scene.clip_planes = [[v[0], v[1], v[2], depth]]

        # self.scene.clip_planes = [[0.6427876096865393, -0.7660444431189781, -0, 0.25]]
        self.scene.clip_plane_depth_azi_elevs = [[depth, azimuth, elevation]]
        self._notify_scene_changed()

    def set_clip_planes(self, depth_azi_elevs: list[list[float]]) -> None:
        """
        Update multiple clip planes in the 3D view.

        Each clip plane is defined by a `[depth, azimuth, elevation]` triple.
        This method converts those spherical definitions into Cartesian plane
        equations and updates the scene accordingly.

        Parameters
        ----------
        depth_azi_elevs : list of list of float
            A list of `[depth, azimuth, elevation]` triples, one per clip plane.

        Raises
        ------
        TypeError
            If any entry in `depth_azi_elevs` is not a list or tuple of three
            numeric values.

        Notes
        -----
        The azimuth is rotated by 180 degrees to match the existing shader
        convention, and the depth value is negated when forming the plane
        equation. After updating all planes, this method notifies the scene
        to refresh.
        """
        if not isinstance(depth_azi_elevs, (list, tuple)):
            raise TypeError(
                "depth_azi_elevs must be a list of [depth, azimuth, elevation] triples."
            )

        self.scene.clip_planes = []
        self.scene.clip_plane_depth_azi_elevs = []

        for i, dae in enumerate(depth_azi_elevs):
            if not isinstance(dae, (list, tuple)) or len(dae) < 3:
                raise TypeError(
                    f"Entry {i} must be a list or tuple of three numeric values."
                )

            depth, azimuth, elevation = dae[0], dae[1], dae[2]

            if not all(
                isinstance(x, (int, float)) for x in (depth, azimuth, elevation)
            ):
                raise TypeError(
                    f"Entry {i} contains non-numeric values; "
                    "expected [depth, azimuth, elevation]."
                )

            n = sph2cart_deg(azimuth + 180, elevation)
            d = -depth
            plane = [n[0], n[1], n[2], d]

            self.scene.clip_planes.append(plane)
            self.scene.clip_plane_depth_azi_elevs.append([depth, azimuth, elevation])

        self._notify_scene_changed()

    def set_render_azimuth_elevation(self, azimuth: float, elevation: float):
        """Set the rotation of the 3D render view.

        Parameters
        ----------
        azimuth : float
            The azimuth angle in degrees around the object.
        elevation : float
            The elevation angle in degrees.

        Raises
        ------
        TypeError
            If azimuth or elevation is not a number.

        Examples
        --------
        ::

            nv.set_render_azimuth_elevation(45, 15)
        """
        if not isinstance(azimuth, (int, float)):
            raise TypeError("Azimuth must be a number.")
        if not isinstance(elevation, (int, float)):
            raise TypeError("Elevation must be a number.")
        self.scene._trait_values["render_azimuth"] = azimuth
        self.scene._trait_values["render_elevation"] = elevation
        self._notify_scene_changed()

    def _mesh_shader_name_to_number(self, mesh_shader_name: str) -> int:
        name = mesh_shader_name.lower()
        mesh_names = self.mesh_shader_names()
        for i in range(len(mesh_names)):
            if name == mesh_names[i].lower():
                return i
        return -1

    def set_mesh_shader(self, mesh_id: str, mesh_shader: typing.Union[str, int]):
        """Set the shader for a mesh.

        Parameters
        ----------
        mesh_id : str
            Identifier of the mesh to change (mesh id).
        mesh_shader : str or int
            The name or index of the shader to set.

        Raises
        ------
        ValueError
            If the mesh is not found.
            If the mesh shader is not found.
        TypeError
            If the mesh_shader is not a string nor integer.

        Examples
        --------
        ::

            nv.set_mesh_shader(nv.meshes[0].id, 'toon')
        """
        idx = self.get_mesh_index_by_id(mesh_id)
        if idx == -1:
            raise ValueError(f"Mesh with id '{mesh_id}' not found.")

        if isinstance(mesh_shader, str):
            mesh_shader_idx = self._mesh_shader_name_to_number(mesh_shader)
            if mesh_shader_idx == -1:
                raise ValueError(f"Mesh shader with name '{mesh_shader}' not found.")
        elif isinstance(mesh_shader, int):
            mesh_shader_idx = mesh_shader
        else:
            raise TypeError("shader_name must be a string or integer.")

        self.meshes[idx].mesh_shader_index = mesh_shader_idx

    def mesh_shader_names(self):
        """Retrieve the list of available mesh shader names.

        Returns
        -------
        list of str
            A list containing the names of all available mesh shader names

        Examples
        --------
        ::

            shaders = nv.mesh_shader_names()
        """
        fallback_shader_names = [
            "Crevice",
            "Diffuse",
            "Edge",
            "Flat",
            "Harmonic",
            "Hemispheric",
            "Matcap",
            "Matte",
            "Outline",
            "Phong",
            "Specular",
            "Toon",
        ]
        shader_names_path = (
            pathlib.Path(__file__).parent / "static" / "meshShaderNames.txt"
        )
        try:
            with open(shader_names_path) as f:
                shader_names_list = f.read().splitlines()
        except FileNotFoundError:
            return fallback_shader_names

        return shader_names_list

    def reverse_faces(self, mesh_id: str):
        """
        Reverse the triangle winding of a mesh (swap front and back faces).

        Parameters
        ----------
        mesh_id : str
            The ID of the mesh to reverse.
        """
        idx = self.get_mesh_index_by_id(mesh_id)
        if idx != -1:
            self.meshes[idx].reverse_faces()
        else:
            raise ValueError(f"Mesh with id '{mesh_id}' not found.")

        self.update_gl_volume()

    def refresh_colormaps(self):
        """Rebuild and upload all colormap textures for volumes and meshes."""
        self.send({"type": "refresh_colormaps", "data": []})

    @requires_canvas
    def set_volume_render_illumination(self, gradient_amount: float):
        """Set proportion of volume rendering influenced by selected matcap.

        Parameters
        ----------
        gradient_amount : float
            Amount of matcap (``NaN`` or ``0..1``).
            Default is ``0.0`` (matte, surface normal does not influence color).
            ``NaN`` renders the gradients.

        Examples
        --------
        ::

            nv.set_volume_render_illumination(0.6)
        """
        if not isinstance(gradient_amount, (int, float)):
            raise TypeError("gradient_amount must be a number.")
        if not math.isnan(gradient_amount):
            self.opts.gradient_amount = gradient_amount
        self.send({"type": "set_volume_render_illumination", "data": [gradient_amount]})

    def update_gl_volume(self):
        """
        Refresh voxel data and redraw the canvas.

        Examples
        --------
        ::

            nv.update_gl_volume()
        """
        self.send({"type": "update_gl_volume", "data": []})

    def draw_scene(self):
        """
        Redraw the canvas.

        Examples
        --------
        ::

            nv.draw_scene()
        """
        self.send({"type": "draw_scene", "data": []})

    def set_high_resolution_capable(
        self, force_device_pixel_ratio: typing.Union[int, bool]
    ):
        """Force the rendering canvas to use a high-resolution display.

        Parameters
        ----------
        force_device_pixel_ratio : int or bool
            Determines how the device pixel ratio is handled.
            ``True`` allows high DPI (equivalent to ``0``).
            ``False`` blocks high DPI (equivalent to ``-1``).

        Examples
        --------
        ::

            nv.set_high_resolution_capable(True)
        """
        if isinstance(force_device_pixel_ratio, bool):
            force_device_pixel_ratio = 0 if force_device_pixel_ratio else -1
        self.opts.force_device_pixel_ratio = force_device_pixel_ratio
        self.send({"type": "resize_listener", "data": []})
        self.send({"type": "draw_scene", "data": []})

    def _load_png_as_texture(self, png_url: str, texture_num: int):
        self.send({"type": "load_png_as_texture", "data": [png_url, texture_num]})

    def load_mat_cap_texture(self, png_data: bytes):
        """Load matcap for illumination model.

        Parameters
        ----------
        png_data : bytes
            Image data binary.

        Examples
        --------
        ::

            matcap_path = './matcaps/gold.jpg'
            with open(matcap_path, 'rb') as f:
                matcap_data = f.read()
            nv.load_mat_cap_texture(matcap_data)
        """
        base64_data = base64.b64encode(png_data).decode("utf-8")
        data_url = f"data:image/png;base64,{base64_data}"
        self._load_png_as_texture(data_url, 5)

    def set_atlas_outline(self, outline: float):
        """Set the outline thickness for atlas label regions.

        Parameters
        ----------
        outline : float
            The width of the outline to apply to atlas label regions.
            A value of `0` disables the outline.

        Examples
        --------
        ::

            nv.set_atlas_outline(2.0)
        """
        self.opts.atlas_outline = outline

    def set_atlas_active_index(self, idx: int):
        """Set atlas region that is highlighted.

        Parameters
        ----------
        idx : integer
            The index of the atlas region to be high lighted.
            A value of `0` disables the high lighting.

        Examples
        --------
        ::

            nv.set_atlas_active_index(2)
        """
        self.opts.atlas_active_index = idx

    def set_interpolation(self, is_nearest: bool):
        """Select between nearest neighbor and linear interpolation for images.

        Parameters
        ----------
        is_nearest : bool
            If True, use nearest neighbor interpolation.
            If False, use linear interpolation.

        Examples
        --------
        ::

            nv.set_interpolation(True)
        """
        self.opts.is_nearest_interpolation = is_nearest
        self.send({"type": "set_interpolation", "data": [is_nearest]})

    def set_cutaway(self, is_cutaway: bool):
        """Set whether clip planes form cutaway.

        Parameters
        ----------
        is_cutaway : bool
            If True, cutaway.
            If False, classic clip planes.

        Examples
        --------
        ::

            nv.set_clip_planes_cutaway(True)
        """
        self.opts.is_clip_planes_cutaway = is_cutaway
        self.send({"type": "set_cutaway", "data": [is_cutaway]})

    def set_pen_value(self, pen_value: float, is_filled_pen: bool):
        """Determine color and style of drawing.

        Parameters
        ----------
        pen_value : float
            sets the color of the pen
        is_filled_pen : bool
            determines if dragging creates flood-filled shape

        Examples
        --------
        ::

            nv.set_pen_value(1.0, True)
        """
        self.opts.pen_value = pen_value
        self.opts.is_filled_pen = is_filled_pen

    def set_drawing_enabled(self, drawing_enabled: bool):
        """Set/unset drawing state.

        Parameters
        ----------
        drawing_enabled: bool
            enabled or not

        Examples
        --------
        ::

            nv.set_drawing_enabled(True)
        """
        if drawing_enabled != self.opts.drawing_enabled:
            self.opts.drawing_enabled = drawing_enabled
            self.send({"type": "set_drawing_enabled", "data": [drawing_enabled]})

    def colormap_from_key(self, colormap_name: str) -> ColorMap:
        """Retrieve a colormap by name (case-insensitive).

        Parameters
        ----------
        colormap_name : str
            The name of the colormap to retrieve.

        Returns
        -------
        ColorMap
            An instance of `ColorMap` corresponding to the given colormap name.

        Examples
        --------
        ::
            cmap = nv.colormap_from_key('Hot')
        """
        return self._cluts[colormap_name.lower()]

    def set_draw_colormap(self, colormap: typing.Union[str, ColorMap]):
        """Set colors and labels for different drawing values.

        Parameters
        ----------
        colormap : str or ColorMap
            A colormap name (string) or a `ColorMap` instance.

        Examples
        --------
        ::

            cmap = {
                'R': [0, 255, 0],
                'G': [0, 20, 0],
                'B': [0, 20, 80],
                'A': [0, 255, 255],
                'labels': ['', 'white-matter', 'delete T1'],
            }
            nv.set_draw_colormap(cmap)
        """
        if isinstance(colormap, str):
            cmap = self.colormap_from_key(colormap)
            draw_lut = make_draw_lut(cmap)
            draw_lut._parent = self
            self.draw_lut = draw_lut
        elif isinstance(colormap, ColorMap):
            draw_lut = make_draw_lut(colormap)
            draw_lut._parent = self
            self.draw_lut = draw_lut
        else:
            raise ValueError("Colormap must be string or type ColorMap.")

    def draw_otsu(self, levels: int):
        """Segment brain into specified number of levels using Otsu's method.

        This method removes dark voxels by segmenting
        the image into the specified number of levels.

        Parameters
        ----------
        levels : int
            Number of levels to segment the brain into (2-4).

        Examples
        --------
        ::

            nv.draw_otsu(3)
        """
        self.send({"type": "draw_otsu", "data": [levels]})

    def draw_grow_cut(self):
        """Dilate drawing so all voxels are colored.

        Examples
        --------
        ::

            nv.draw_grow_cut()
        """
        self.send({"type": "draw_grow_cut", "data": []})

    def move_crosshair_in_vox(self, x: float, y: float, z: float):
        """Move crosshair by a fixed number of voxels.

        Parameters
        ----------
        x : float
            Translate left (-) or right (+)
        y : float
            Translate posterior (-) or anterior (+)
        z : float
            Translate inferior (-) or superior (+)

        Examples
        --------
        ::

            nv.move_crosshair_in_vox(1, 0, 0)
        """
        # todo: update backend scene data
        self.send({"type": "move_crosshair_in_vox", "data": [x, y, z]})

    def remove_haze(self, level: int = 5, vol_index: int = 0):
        """Remove dark voxels in air.

        Parameters
        ----------
        level : int, optional
            Level of dehazing (1-5); larger values preserve more voxels. Default is 5.
        vol_index : int, optional
            Index of the volume to dehaze. Default is 0.

        Examples
        --------
        ::

            nv.remove_haze(3, 0)
        """
        self.send({"type": "remove_haze", "data": [level, vol_index]})

    def set_slice_mm(self, is_slice_mm: bool):
        """Control 2D slice view mode.

        Parameters
        ----------
        is_slice_mm : bool
            Control whether 2D slices use world space (True) or voxel space (False).

        Examples
        --------
        ::

            nv.set_slice_mm(True)
        """
        self.opts.is_slice_mm = is_slice_mm

    def draw_undo(self):
        """Restore drawing to previous state.

        Examples
        --------
        ::

            nv.draw_undo()
        """
        self.send({"type": "draw_undo", "data": []})

    def close_drawing(self):
        """Close the current drawing.

        Examples
        --------
        ::

            nv.close_drawing()
        """
        self.send({"type": "close_drawing", "data": []})

    def set_radiological_convention(self, is_radiological_convention: bool):
        """Set radiological or neurological convention for 2D slices.

        Parameters
        ----------
        is_radiological_convention : bool
            If True, use radiological convention.
            If False, use neurological convention.

        Examples
        --------
        ::

            nv.set_radiological_convention(True)
        """
        self.opts.is_radiological_convention = is_radiological_convention

    @requires_canvas
    def load_drawing(self, path: str, is_binarize: bool = False):
        """Load a drawing.

        Parameters
        ----------
        path : str
            The url or path of the drawing.
        is_binarize : bool
            If true will force drawing voxels to be either 0 or 1.


        Examples
        --------
        ::

            nv.load_drawing("./images/lesion.nii.gz")
        """
        if not self.volumes:
            raise ValueError("Cannot load drawing: No volumes are loaded.")
        if pathlib.Path(path).exists():
            file_bytes = pathlib.Path(path).read_bytes()
            self.send(
                {
                    "type": "load_drawing_from_url",
                    "data": [f"local>{path}", is_binarize],
                },
                buffers=[file_bytes],
            )
        else:
            self.send({"type": "load_drawing_from_url", "data": [path, is_binarize]})

    def set_multiplanar_pad_pixels(self, pixels: int):
        """Insert a gap between slices of a mutliplanar view.

        Parameters
        ----------
        pixels : int
            spacing between tiles of multiplanar view
        """
        self.opts.multiplanar_pad_pixels = pixels

    def set_colormap_negative(self, image_id: str, colormap_negative: str):
        """
        Set the colormap negative for a specific volume.

        Parameters
        ----------
        image_id : str
            The ID of the volume for which to set the negative colormap.
        colormap_negative : str
            The name of the negative colormap to use (e.g., "winter").

        Raises
        ------
        ValueError
            If the volume with the given ID is not found.

        Examples
        --------
        ::

            nv.set_colormap_negative(nv.volumes[1].id, "winter")
        """
        idx = self.get_volume_index_by_id(image_id)
        if idx != -1:
            self.volumes[idx].colormap_negative = colormap_negative
        else:
            raise ValueError(f"Volume with ID '{image_id}' not found")

    def set_slice_mosaic_string(self, mosaic_string: str):
        """Create a custom multi-slice mosaic view.

        Parameters
        ----------
        mosaic_string : str
            description of mosaic
        """
        self.opts.slice_mosaic_string = mosaic_string

    def set_corner_orientation_text(self, is_corner_orientation_text: bool):
        """Determine if text appears at corner (true) or sides of 2D slice.

        Parameters
        ----------
        is_corner_orientation_text : str
            controls position of text
        """
        self.opts.is_corner_orientation_text = is_corner_orientation_text

    def set_mesh_thickness_on_2d(self, mesh_thickness_on_2d: float):
        """Limit visibility of mesh in front of a 2D image. Requires world-space mode.

        Parameters
        ----------
        mesh_thickness_on_2d : str
            distance from voxels for clipping mesh. Use float("inf")
            to show entire mesh or 0.0 to hide mesh.
        """
        self.opts.mesh_thickness_on_2d = mesh_thickness_on_2d

    def set_opacity(self, vol_idx: int, new_opacity: float):
        """Set the opacity of a volume given by volume index.

        Parameters
        ----------
        vol_idx : int
            The volume index of the volume to change.
        new_opacity : float
            The opacity value. Valid values range from 0 to 1.

        Raises
        ------
        ValueError
            If `new_opacity` is not between 0 and 1 inclusive.
        IndexError
            If `vol_idx` is out of range of the `self.volumes` list.
        """
        if not (0 <= new_opacity <= 1):
            raise ValueError("new_opacity must be between 0 and 1 inclusive.")
        if not 0 <= vol_idx < len(self.volumes):
            raise IndexError("vol_idx is out of range.")

        self.volumes[vol_idx].opacity = new_opacity

    def set_hero_image(self, fraction: float):
        """
        Determine proportion of screen devoted to rendering in multiplanar view.

        Parameters
        ----------
        fraction : float
            Proportion of screen devoted to primary (hero) image (0 to disable).
        """
        self.opts.hero_image_fraction = fraction

    @requires_canvas
    def set_modulation_image(
        self, id_target: str, id_modulation: str, modulate_alpha: int = 0
    ):
        """
        Modulate the intensity of one volume based on the intensity of another.

        Parameters
        ----------
        id_target : str
            The ID of the volume to be modulated.
        id_modulation : str
            The ID of the volume that controls the modulation.
            Pass an empty string ('') to disable modulation.
        modulate_alpha : int, optional
            Determines if the modulation influences alpha transparency.
            Values greater than 1 will affect transparency. Default is 0.

        Raises
        ------
        ValueError
            If the target or modulation volume ID is not found.
        RuntimeError
            If the canvas has not been attached yet.
            This function requires nv._gl to be valid in the frontend.

        Examples
        --------
        ::

            nv.set_modulation_image(nv.volumes[0].id, nv.volumes[1].id)
        """
        idx_target = self.get_volume_index_by_id(id_target)
        if idx_target == -1:
            raise ValueError(f"Volume with ID '{id_target}' not found.")

        volume_target = self.volumes[idx_target]

        if id_modulation:
            idx_modulation = self.get_volume_index_by_id(id_modulation)
            if idx_modulation == -1:
                raise ValueError(
                    f"Modulation volume with ID '{id_modulation}' not found."
                )
            volume_target.modulation_image = idx_modulation
        else:
            volume_target.modulation_image = None

        volume_target.modulate_alpha = modulate_alpha

    @requires_canvas
    def load_document(self, path: str):
        """
        Load a NiiVue document from a URL or file path.

        Parameters
        ----------
        path : str
            The URL or path of the document (.nvd file).
        """
        # should we check if path is valid before clearing these?
        self._trait_values["volumes"] = []
        self._trait_values["meshes"] = []

        if pathlib.Path(path).exists():
            file_bytes = pathlib.Path(path).read_bytes()
            self.send(
                {
                    "type": "load_document_from_url",
                    "data": [f"local>{path}"],
                },
                buffers=[file_bytes],
            )
        else:
            self.send({"type": "load_document_from_url", "data": [path]})

    """
    Custom event callbacks
    """

    def on_canvas_attached(self, callback, remove=False):
        """
        Register a callback for when the canvas becomes attached.

        If canvas is already attached the callback just gets called.

        Parameters
        ----------
        callback : callable
            Called when the canvas becomes attached.
        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.
        """
        self._register_callback("canvas_attached", callback, remove=remove)

        if not remove:
            dispatcher = self._event_handlers["canvas_attached"]
            if len(dispatcher.callbacks) == 1:

                def _canvas_attached_observer(change):
                    if change["new"] and not change["old"]:
                        dispatcher()

                self.observe(_canvas_attached_observer, names="_canvas_attached")

            if self._canvas_attached:
                callback()

    def on_azimuth_elevation_change(self, callback, remove=False):
        """
        Register a callback for the 'azimuth_elevation_change' event.

        Set a callback function to run when the user changes the rotation of the 3D
        rendering.

        Parameters
        ----------
        callback : callable
            A function that takes two arguments:

            - **azimuth** (float): The azimuth angle in degrees.
            - **elevation** (float): The elevation angle in degrees.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(azimuth, elevation):
                with out:
                    print('Azimuth:', azimuth)
                    print('Elevation:', elevation)

            nv.on_azimuth_elevation_change(my_callback)

        """
        self._register_callback("azimuth_elevation_change", callback, remove=remove)

    def on_click_to_segment(self, callback, remove=False):
        """
        Register a callback for the 'click_to_segment' event.

        Set a callback function when ``clickToSegment`` is enabled and the user clicks
        on the image.

        Parameters
        ----------
        callback : callable
            A function that takes one argument - a ``dict`` with the following keys:

            - **mm3** (float): The segmented volume in cubic millimeters.
            - **mL** (float): The segmented volume in milliliters.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(data):
                with out:
                    print('Clicked to segment')
                    print('Volume mm3:', data['mm3'])
                    print('Volume mL:', data['mL'])

            nv.on_click_to_segment(my_callback)

        """
        self._register_callback("click_to_segment", callback, remove=remove)

    def on_clip_plane_change(self, callback, remove=False):
        """
        Register a callback for the 'clip_plane_change' event.

        Set a callback function to run when the user changes the clip plane.

        Parameters
        ----------
        callback : callable
            A function that takes one argument - a list of numbers representing the
            clip plane.
        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            @nv.on_clip_plane_change
            def my_callback(clip_plane):
                with out:
                    print('Clip plane changed:', clip_plane)

        """
        self._register_callback("clip_plane_change", callback, remove=remove)

    # todo: make volumes be a list of Volumes and meshes be a list of Meshes
    def on_document_loaded(self, callback, remove=False):
        """
        Register a callback for the 'document_loaded' event.

        Set a callback function to run when the user loads a new NiiVue document.

        Parameters
        ----------
        callback : callable
            A function that takes one argument - a ``dict`` representing the loaded
            document with the following keys:

            - **title** (str): The title of the loaded document.
            - **opts** (dict): Options associated with the document.
            - **volumes** (list of str): A list of volume IDs loaded in the document.
            - **meshes** (list of str): A list of mesh IDs loaded in the document.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            @nv.on_document_loaded
            def my_callback(document):
                with out:
                    print('Document loaded:')
                    print('Title:', document['title'])
                    print('Options:', document['opts'])
                    print('Volumes:', document['volumes'])
                    print('Meshes:', document['meshes'])

        """
        self._register_callback("document_loaded", callback, remove=remove)

    def on_image_loaded(self, callback, remove=False):
        """
        Register a callback for the 'image_loaded' event.

        Set a callback function to run when a new volume is loaded.

        Parameters
        ----------
        callback : callable
            A function that takes one argument - a ``Volume`` object.
        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            @nv.on_image_loaded
            def my_callback(volume):
                with out:
                    print('Image loaded:', volume.id)

        """
        self._register_callback("image_loaded", callback, remove=remove)

    def on_drag_release(self, callback, remove=False):
        """
        Register a callback for the 'drag_release' event.

        Set a callback function to run when the right mouse button is released
        after dragging.

        Parameters
        ----------
        callback : callable
            A function that takes one argument - a ``dict`` containing drag release
            parameters with the following keys:

            - **frac_start** (list of float): Starting fractional coordinates
                ``[X, Y, Z]`` before the drag.
            - **frac_end** (list of float): Ending fractional coordinates
                ``[X, Y, Z]`` after the drag.
            - **vox_start** (list of float): Starting voxel coordinates ``[X, Y, Z]``
                before the drag.
            - **vox_end** (list of float): Ending voxel coordinates ``[X, Y, Z]``
                after the drag.
            - **mm_start** (list of float): Starting coordinates in millimeters
                ``[X, Y, Z]`` before the drag.
            - **mm_end** (list of float): Ending coordinates in millimeters
                ``[X, Y, Z]`` after the drag.
            - **mm_length** (float): Length of the drag in millimeters.
            - **tile_idx** (int): Index of the image tile where the drag occurred.
            - **ax_cor_sag** (int): View index (axial=0, coronal=1, sagittal=2) where
                the drag occurred.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            @nv.on_drag_release
            def my_callback(params):
                with out:
                    print('Drag release event:', params)

        """
        self._register_callback("drag_release", callback, remove=remove)

    def on_frame_change(self, callback, remove=False):
        """
        Register a callback for the 'frame_change' event.

        Set a callback function to run whenever the current frame (timepoint) of a
        4D image volume changes.

        Parameters
        ----------
        callback : callable
            A function that takes two arguments:

            - **volume** (``Volume``): The image volume object that has changed frame.
            - **frame_index** (int): The index of the new frame.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            @nv.on_frame_change
            def my_callback(volume, frame_index):
                with out:
                    print('Frame changed')
                    print('Volume:', volume)
                    print('Frame index:', frame_index)

        """
        self._register_callback("frame_change", callback, remove=remove)

    def on_intensity_change(self, callback, remove=False):
        """
        Register a callback for the 'intensity_change' event.

        Set a callback function to run when the user changes the intensity range
        with the selection-box action (right click).

        Parameters
        ----------
        callback : callable
            A function that takes one argument - a ``Volume`` object.
        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            @nv.on_intensity_change
            def my_callback(volume):
                with out:
                    print('Intensity changed for volume:', volume)

        """
        self._register_callback("intensity_change", callback, remove=remove)

    # todo: maybe create NiiVueLocation and NiiVueLocationValue classes?
    def on_location_change(self, callback, remove=False):
        """
        Register a callback for the 'location_change' event.

        Set a callback function to run when the crosshair location changes.

        Parameters
        ----------
        callback : callable
            A function that takes one argument - a ``dict`` containing the new
            location data - with the following keys:

            - **ax_cor_sag** (int): The view index where the location changed.
            - **frac** (list of float): The fractional coordinates ``[X, Y, Z]``
                in the volume.
            - **mm** (list of float): The coordinates ``[X, Y, Z]`` in millimeters.
            - **vox** (list of int): The voxel coordinates ``[X, Y, Z]``.
            - **values** (list of float): Intensity values at the current location
                for each volume.
            - **string** (str): Formatted string representing the location and
                intensity values.
            - **xy** (list of float): The canvas coordinates ``[X, Y]``.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            @nv.on_location_change
            def my_callback(location):
                with out:
                    print('Location changed', location)

        """
        self._register_callback("location_change", callback, remove=remove)

    def on_mesh_added_from_url(self, callback, remove=False):
        """
        Register a callback for the 'mesh_added_from_url' event.

        Set a callback function to run when a mesh is added from a URL.

        **Note:** This is called before the ``mesh_loaded`` event is emitted, so
        the mesh object will **not** be available in the callback.

        Parameters
        ----------
        callback : callable
            A function that takes two arguments:

            - **mesh_options** (dict): Dictionary containing:
                - **url** (str): The URL from which the mesh was loaded.
                - **headers** (dict): HTTP headers used when loading the mesh.

            - **mesh** (dict): Dictionary containing:
                - **id** (str): The ID of the mesh.
                - **name** (str): The name of the mesh.
                - **rgba255** (list of int): RGBA color values (0-255) of the mesh.
                - **opacity** (float): The opacity of the mesh.
                - **visible** (bool): Whether the mesh is visible.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            @nv.on_mesh_added_from_url
            def my_callback(mesh_options, mesh):
                with out:
                    print('Mesh added from URL')
                    print('URL:', mesh_options['url'])
                    print('Headers:', mesh_options['headers'])
                    print('Mesh ID:', mesh['id'])

        """
        self._register_callback("mesh_added_from_url", callback, remove=remove)

    def on_mesh_loaded(self, callback, remove=False):
        """
        Register a callback for the 'mesh_loaded' event.

        Set a callback function to run when a new mesh is loaded.

        Parameters
        ----------
        callback : callable
            A function that takes one argument - the loaded mesh (``Mesh`` object).
        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            @nv.on_mesh_loaded
            def my_callback(mesh):
                with out:
                    print('Mesh loaded', mesh)

        """
        self._register_callback("mesh_loaded", callback, remove=remove)

    def on_mouse_up(self, callback, remove=False):
        """
        Register a callback for the 'mouse_up' event.

        Set a callback function to run when the left mouse button is released.

        Parameters
        ----------
        callback : callable
            A function that takes one argument - a ``dict`` containing mouse event data
            with the following keys:

            - **is_dragging** (bool): Indicates if a drag action is in progress
                (``True``) or not (``False``).
            - **mouse_pos** (tuple of int): The ``(x, y)`` pixel coordinates of the
                mouse on the canvas when the button was released.
            - **frac_pos** (tuple of float): The fractional position ``(X, Y, Z)``
                within the volume, with each coordinate ranging from ``0.0`` to ``1.0``.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            @nv.on_mouse_up
            def my_callback(data):
                with out:
                    print('Mouse button released', data)

        """
        self._register_callback("mouse_up", callback, remove=remove)

    def on_volume_added_from_url(self, callback, remove=False):
        """
        Register a callback for the 'volume_added_from_url' event.

        Set a callback function to run when a volume is added from a URL.

        **Note:** This is called before the ``image_loaded`` event is emitted, so
        the volume object will **not** be available in the callback.

        Parameters
        ----------
        callback : callable
            A function that takes two arguments:

            - **image_options** (dict): Dictionary containing:

                - **url** (str): The URL from which the volume was loaded.
                - **url_image_data** (str): The URL to the image data associated with
                    the volume (if separate from header).
                - **headers** (dict): HTTP headers used when loading the volume.
                - **name** (str): A name for this image (default is an empty string).
                - **colormap** (str): A colormap to use (default is 'gray').
                - **opacity** (float): The opacity for this image (default is 1).
                - **cal_min** (float): Minimum intensity for color brightness/contrast.
                - **cal_max** (float): Maximum intensity for color brightness/contrast.
                - **trust_cal_min_max** (bool): Whether to trust `cal_min` and `cal_max`
                    from the NIfTI header (default is True).
                - **percentile_frac** (float): The percentile to use for setting the
                    robust range of the display values (default is 0.02).
                - **use_qform_not_sform** (bool): Whether to use QForm instead of SForm
                    during construction (default is False).
                - **alpha_threshold** (bool): Whether to use alpha thresholding
                    (default is False).
                - **colormap_negative** (str): Colormap for negative values.
                - **cal_min_neg** (float): Minimum intensity for negative color
                    brightness/contrast.
                - **cal_max_neg** (float): Maximum intensity for negative color
                    brightness/contrast.
                - **colorbar_visible** (bool): Visibility of the colorbar
                    (default is True).
                - **ignore_zero_voxels** (bool): Whether to ignore zero voxels when
                    setting the display range (default is False).
                - **image_type** (int): The image type (default is 0).
                - **frame_4d** (int): Frame number for 4D images (default is 0).
                - **colormap_label** (str or None): Label for the colormap.
                - **limit_frames4D** (int): Limit the number of frames for 4D images.
                - **is_manifest** (bool): Whether the image is loaded from a manifest
                    (default is False).

            - **volume** (dict): Dictionary containing:

                - **id** (str): The ID of the volume.
                - **name** (str): The name of the volume.
                - **colormap** (str): The colormap used for the volume.
                - **opacity** (float): The opacity of the volume.
                - **colorbar_visible** (bool): Visibility of the colorbar.
                - **cal_min** (float or None): Minimum calibration value.
                - **cal_max** (float or None): Maximum calibration value.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            @nv.on_volume_added_from_url
            def my_callback(image_options, volume):
                with out:
                    print('Volume added from URL')
                    print('URL:', image_options['url'])
                    print('Headers:', image_options['headers'])
                    print('Volume ID:', volume['id'])

        """
        self._register_callback("volume_added_from_url", callback, remove=remove)

    def on_volume_updated(self, callback, remove=False):
        """
        Register a callback for the 'volume_updated' event.

        Sets a callback function to run when `updateGLVolume` is called.
        Most users will not need to use this directly.

        Parameters
        ----------
        callback : callable
            A function that takes no arguments.
        remove : bool, optional
            If True, remove the callback. Defaults to False.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display

            out = Output()
            display(out)

            @nv.on_volume_updated
            def my_callback():
                with out:
                    print('Volumes updated')

        """
        self._register_callback("volume_updated", callback, remove=remove)

    def on_hover_idx_change(self, callback, remove=False):
        """
        Register a callback for the 'hover_idx_change' event.

        Set a callback function to run whenever the mouse moves over the canvas
        and the index (`idx`) values under the cursor position change.

        This event provides the index (`idx`) values of the data under the cursor
        for all volumes. The callback function receives a dictionary containing
        the index values for each volume.

        Parameters
        ----------
        callback : callable
            The function to call when the event occurs. It should accept one argument:

            - **data** (dict): A dictionary containing idx values for each volume.

            The dictionary has a key `'idx_values'`, which is a list of dictionaries
            with the following keys:

            - **id** (str): The ID of the volume.
            - **idx** (float or None): The index of the cursor position for the volume.

        remove : bool, optional
            If `True`, remove the callback. Defaults to `False`.

        Examples
        --------
        ::

            def hover_idx_callback(data):
                idx_values = data['idx_values']
                for idx_info in idx_values:
                    volume_id = idx_info['id']
                    idx = idx_info['idx']
                    print(f'Volume ID: {volume_id}, Index: {idx}')

            nv.on_hover_idx_change(hover_idx_callback)

        """
        self._register_callback("hover_idx_change", callback, remove=remove)

    """
    Sync
    """

    def broadcast_to(self, other_nv, sync_opts=None):
        """
        Sync the scene controls from one NiiVue instance to others.

        Useful for using one canvas to drive another.

        Parameters
        ----------
        other_nv : :class:`NiiVue` or list of :class:`NiiVue`
            The other NiiVue instance(s) to broadcast state to.
        sync_opts : dict, optional
            Options specifying which properties to sync. E.g., {'2d': True, '3d': True}
            Possible keys are:
            - gamma
            - crosshair
            - zoom_pan
            - slice_type
            - cal_min
            - cal_max
            - clip_plane
            - 2d
            - 3d
        """
        if not isinstance(sync_opts, dict):
            sync_opts = {"2d": True, "3d": True}

        if not isinstance(other_nv, (list, tuple)):
            other_nv = [other_nv]

        self.other_nv = other_nv
        self.sync_opts = sync_opts

    def _do_sync_3d(self, other_nv):
        """Synchronize 3D view settings with another NiiVue instance.

        Do not call this by itself. This should be called by the sync method.
        """
        other_nv.scene._trait_values["render_azimuth"] = self.scene.render_azimuth
        other_nv.scene._trait_values["render_elevation"] = self.scene.render_elevation
        other_nv.scene._trait_values["vol_scale_multiplier"] = (
            self.scene.vol_scale_multiplier
        )

    def _do_sync_2d(self, other_nv):
        """Synchronize 2D crosshair pos + pan settings with another NiiVue instance.

        Do not call this by itself. This should be called by the sync method.
        """
        this_mm = self.frac2mm(self.scene.crosshair_pos)
        other_nv.scene._trait_values["crosshair_pos"] = other_nv.mm2frac(this_mm)
        other_nv.scene._trait_values["pan2d_xyzmm"] = list(self.scene.pan2d_xyzmm)

    def _do_sync_gamma(self, other_nv):
        """Synchronize gamma correction setting with another NiiVue instance."""
        this_gamma = self.scene.gamma
        other_gamma = other_nv.scene.gamma
        if this_gamma != other_gamma:
            other_nv.set_gamma(this_gamma)

    def _do_sync_zoom_pan(self, other_nv):
        """Synchronize zoom/pan settings with another NiiVue instance.

        Do not call this by itself. This should be called by the sync method.
        """
        other_nv.scene._trait_values["pan2d_xyzmm"] = list(self.scene.pan2d_xyzmm)

    def _do_sync_crosshair(self, other_nv):
        """Synchronize crosshair position with another NiiVue instance.

        Do not call this by itself. This should be called by the sync method.
        """
        this_mm = self.frac2mm(self.scene.crosshair_pos)
        other_nv.scene._trait_values["crosshair_pos"] = other_nv.mm2frac(this_mm)

    def _do_sync_cal_min(self, other_nv):
        """Synchronize cal_min with another NiiVue instance."""
        if (
            self.volumes
            and other_nv.volumes
            and self.volumes[0].cal_min != other_nv.volumes[0].cal_min
        ):
            other_nv.volumes[0].cal_min = self.volumes[0].cal_min

    def _do_sync_cal_max(self, other_nv):
        """Synchronize cal_max with another NiiVue instance."""
        if (
            self.volumes
            and other_nv.volumes
            and self.volumes[0].cal_max != other_nv.volumes[0].cal_max
        ):
            other_nv.volumes[0].cal_max = self.volumes[0].cal_max

    def _do_sync_slice_type(self, other_nv):
        """Synchronize slice view type with another NiiVue instance."""
        other_nv.set_slice_type(self.opts.slice_type)

    def _do_sync_clip_plane(self, other_nv):
        """Synchronize clip plane settings with another NiiVue instance."""
        # todo: add ui_data class + property with active_clip_plane_index?
        if len(self.scene.clip_plane_depth_azi_elevs) > 0:
            other_nv.set_clip_plane(*self.scene.clip_plane_depth_azi_elevs[0])

    def sync(self):
        """Sync the scene controls from this NiiVue instance to others."""
        for nv_obj in self.other_nv:
            if not nv_obj._canvas_attached:
                # todo: add logging msg here
                continue

            if self.sync_opts.get("gamma"):
                self._do_sync_gamma(nv_obj)
            if self.sync_opts.get("crosshair"):
                self._do_sync_crosshair(nv_obj)
            if self.sync_opts.get("zoom_pan"):
                self._do_sync_zoom_pan(nv_obj)
            if self.sync_opts.get("slice_type"):
                self._do_sync_slice_type(nv_obj)
            if self.sync_opts.get("cal_min"):
                self._do_sync_cal_min(nv_obj)
            if self.sync_opts.get("cal_max"):
                self._do_sync_cal_max(nv_obj)
            if self.sync_opts.get("clip_plane"):
                self._do_sync_clip_plane(nv_obj)

            # legacy 2d and 3d opts:
            if self.sync_opts.get("2d"):
                self._do_sync_2d(nv_obj)
            if self.sync_opts.get("3d"):
                self._do_sync_3d(nv_obj)

            nv_obj._notify_scene_changed()

    """
    Custom utils
    """

    def scene_extents_min_max(self, is_slice_mm: bool = True) -> tuple:
        """
        Return the scene's min, max, and range extents in mm or voxel space.

        Includes both volume and mesh geometry.

        Parameters
        ----------
        is_slice_mm : bool, optional
            If True, returns extents in mm space.
            If False, returns extents in voxel space. Default is True.

        Returns
        -------
        tuple
            A tuple containing three lists:
            - min_extents: [x, y, z] minimum coordinates
            - max_extents: [x, y, z] maximum coordinates
            - range: [x, y, z] range (max - min) for each dimension

        Raises
        ------
        RuntimeError
            If volumes exist but volume_object_3d_data is not defined.

        Examples
        --------
        ::

            min_ext, max_ext, range_ext = nv.scene_extents_min_max()
            print(f"Min: {min_ext}, Max: {max_ext}, Range: {range_ext}")
        """
        mn = np.array([0.0, 0.0, 0.0])
        mx = np.array([0.0, 0.0, 0.0])

        if len(self.volumes) > 0:
            if not self._volume_object_3d_data:
                raise RuntimeError(
                    "_volume_object_3d_data not defined. Canvas needs to be attached."
                )

            if is_slice_mm:
                mn = np.array(self._volume_object_3d_data.extents_min)
                mx = np.array(self._volume_object_3d_data.extents_max)
            else:
                if (
                    self.volumes[0].extents_min_ortho
                    and self.volumes[0].extents_max_ortho
                ):
                    mn = np.array(self.volumes[0].extents_min_ortho)
                    mx = np.array(self.volumes[0].extents_max_ortho)

        if len(self.meshes) > 0:
            if len(self.volumes) < 1:
                if self.meshes[0].extents_min and self.meshes[0].extents_max:
                    mn = np.array(self.meshes[0].extents_min)
                    mx = np.array(self.meshes[0].extents_max)

            for mesh in self.meshes:
                if mesh.extents_min and mesh.extents_max:
                    mesh_min = np.array(mesh.extents_min)
                    mesh_max = np.array(mesh.extents_max)
                    mn = np.minimum(mn, mesh_min)
                    mx = np.maximum(mx, mesh_max)

        range_extents = mx - mn

        return (mn.tolist(), mx.tolist(), range_extents.tolist())

    def mm2frac(
        self, mm: list, vol_idx: int = 0, is_force_slice_mm: bool = False
    ) -> list:
        """
        Convert mm coords to frac volume coords for a volume.

        Parameters
        ----------
        mm : list of float
            Position in millimeters [X, Y, Z] or [X, Y, Z, W].
        vol_idx : int, optional
            Index of the volume to use for conversion. Default is 0.
        is_force_slice_mm : bool, optional
            If True, use world space coordinates. If False, use orthogonal space
            unless `opts.is_slice_mm` is True. Default is False.

        Returns
        -------
        list of float
            Fractional coordinates [X, Y, Z] in the range [0, 1].

        Examples
        --------
        ::

            frac_pos = nv.mm2frac([10.0, 20.0, 30.0])
        """
        if len(self.volumes) < 1:
            frac = [0.1, 0.5, 0.5]
            mn, _, range_ext = self.scene_extents_min_max()

            if len(mm) >= 3:
                frac[0] = (mm[0] - mn[0]) / range_ext[0] if range_ext[0] != 0 else 0.5
                frac[1] = (mm[1] - mn[1]) / range_ext[1] if range_ext[1] != 0 else 0.5
                frac[2] = (mm[2] - mn[2]) / range_ext[2] if range_ext[2] != 0 else 0.5

            for i in range(3):
                if not math.isfinite(frac[i]):
                    frac[i] = 0.5

            if len(self.meshes) < 1 and not all(math.isfinite(f) for f in frac):
                print("mm2frac() not finite: objects not yet loaded.")

            return frac

        if vol_idx < 0 or vol_idx >= len(self.volumes):
            raise IndexError(f"Volume index {vol_idx} out of range.")

        return self.volumes[vol_idx].convert_mm2frac(
            mm, is_force_slice_mm or self.opts.is_slice_mm
        )

    def frac2mm(
        self,
        frac: list,
        vol_idx: int = 0,
        is_force_slice_mm: bool = False,
    ) -> list:
        """
        Convert frac volume coords to mm space for a volume.

        Parameters
        ----------
        frac : list of float
            Fractional coordinates [X, Y, Z] in the range [0, 1].
        vol_idx : int, optional
            Index of the volume to use for conversion. Default is 0.
        is_force_slice_mm : bool, optional
            If True, use world space coordinates. If False, use orthogonal space
            unless `opts.is_slice_mm` is True. Default is False.

        Returns
        -------
        list of float
            Position in millimeters [X, Y, Z, W] where W is always 1.

        Examples
        --------
        ::

            mm_pos = nv.frac2mm([0.5, 0.5, 0.5])
        """
        pos = [frac[0], frac[1], frac[2], 1.0]

        if len(self.volumes) > 0:
            if vol_idx < 0 or vol_idx >= len(self.volumes):
                raise IndexError(f"Volume index {vol_idx} out of range.")

            return self.volumes[vol_idx].convert_frac2mm(
                frac, is_force_slice_mm or self.opts.is_slice_mm
            )
        else:
            mn, mx, _ = self.scene_extents_min_max()

            pos[0] = lerp(mn[0], mx[0], frac[0])
            pos[1] = lerp(mn[1], mx[1], frac[1])
            pos[2] = lerp(mn[2], mx[2], frac[2])

        return pos


class WidgetObserver:
    """Creates an observer on the `attribute` of `object` for a `widget`."""

    def __init__(self, widget, obj, attribute):
        self.widget = widget
        self.object = obj
        self.attribute = attribute
        self._observe()

    def _widget_change(self, change):
        setattr(self.object, self.attribute, change["new"])

    def _observe(self):
        self.widget.observe(self._widget_change, names=["value"])
