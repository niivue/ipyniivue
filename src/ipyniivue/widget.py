"""
Widgets representing NiiVue model instances as well as volume, mesh, and drawing models.

Aside from setting up the Mesh, Volume, Drawing, and NiiVue widgets, this module
contains many of the classes needed to make NiiVue instances work, such as classes
to load objects in, change attributes of this instance, and more.
"""

import pathlib
import typing
import uuid

import anywidget
import ipywidgets
import traitlets as t
from ipywidgets import CallbackDispatcher

from .constants import _SNAKE_TO_CAMEL_OVERRIDES, SliceType
from .options_mixin import OptionsMixin
from .utils import (
    file_serializer,
    serialize_options,
    snake_to_camel,
)

__all__ = ["NiiVue"]


class MeshLayer(anywidget.AnyWidget):
    """
    Represents a layer within a Mesh model.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the layer data file. Cannot be modified once set.
    opacity : float, optional
        Opacity between 0.0 (transparent) and 1.0 (opaque). Default is 0.5.
    colormap : str, optional
        Colormap name for rendering. Default is 'gray'.
    colormap_negative : str, optional
        Colormap for negative values if `use_negative_cmap` is True.
        Default is 'winter'.
    use_negative_cmap : bool, optional
        Use negative colormap for negative values. Default is False.
    cal_min : float or None, optional
        Minimum intensity value for brightness/contrast mapping.
    cal_max : float or None, optional
        Maximum intensity value for brightness/contrast mapping.
    outline_border : int, optional
        Outline border thickness. Default is 0.
    """

    path = t.Union([t.Instance(pathlib.Path), t.Unicode()]).tag(
        sync=True, to_json=file_serializer
    )
    id = t.Unicode(default_value="").tag(sync=True)
    opacity = t.Float(0.5).tag(sync=True)
    colormap = t.Unicode("gray").tag(sync=True)
    colormap_negative = t.Unicode("winter").tag(sync=True)
    use_negative_cmap = t.Bool(False).tag(sync=True)
    cal_min = t.Float(None, allow_none=True).tag(sync=True)
    cal_max = t.Float(None, allow_none=True).tag(sync=True)
    outline_border = t.Int(0).tag(sync=True)

    # other properties that aren't in init
    colormap_invert = t.Bool(False).tag(sync=True)
    frame4D = t.Int(0).tag(sync=True)
    colorbar_visible = t.Bool(True).tag(sync=True)

    def __init__(self, **kwargs):
        if "colormap_invert" in kwargs:
            kwargs.pop("colormap_invert")
        if "frame4D" in kwargs:
            kwargs.pop("frame4D")
        if "colorbar_visible" in kwargs:
            kwargs.pop("colorbar_visible")
        super().__init__(**kwargs)

    @t.validate("path")
    def _validate_path(self, proposal):
        if (
            "path" in self._trait_values
            and self.path
            and self.path != proposal["value"]
        ):
            raise t.TraitError("Cannot modify path once set.")
        return proposal["value"]

    @t.validate("id")
    def _validate_id(self, proposal):
        if "id" in self._trait_values and self.id and self.id != proposal["value"]:
            raise t.TraitError("Cannot modify id once set.")
        return proposal["value"]


class Mesh(anywidget.AnyWidget):
    """
    Represents a Mesh model.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the mesh file. Cannot be modified once set.
    name : str, optional
        Name of the mesh.
    rgba255 : list of int, optional
        RGBA color as a list of four integers (0 to 255).
    opacity : float, optional
        Opacity between 0.0 (transparent) and 1.0 (opaque). Default is 1.0.
    visible : bool, optional
        Mesh visibility. Default is True.
    layers : list of dict, optional
        List of layer data dictionaries.
        See :class:`MeshLayer` for attribute options.
    """

    path = t.Union([t.Instance(pathlib.Path), t.Unicode()]).tag(
        sync=True, to_json=file_serializer
    )
    id = t.Unicode(default_value="").tag(sync=True)
    name = t.Unicode(default_value="").tag(sync=True)
    rgba255 = t.List([0, 0, 0, 0]).tag(sync=True)
    opacity = t.Float(1.0).tag(sync=True)
    visible = t.Bool(True).tag(sync=True)
    layers = t.List(t.Instance(MeshLayer), default_value=[]).tag(
        sync=True, **ipywidgets.widget_serialization
    )

    # other properties that aren't in init
    colormap_invert = t.Bool(False).tag(sync=True)

    def __init__(self, **kwargs):
        if "colormap_invert" in kwargs:
            kwargs.pop("colormap_invert")
        layers_data = kwargs.pop("layers", [])
        super().__init__(**kwargs)
        self.layers = [MeshLayer(**layer_data) for layer_data in layers_data]

    @t.validate("path")
    def _validate_path(self, proposal):
        if (
            "path" in self._trait_values
            and self.path
            and self.path != proposal["value"]
        ):
            raise t.TraitError("Cannot modify path once set.")
        return proposal["value"]

    @t.validate("id")
    def _validate_id(self, proposal):
        if "id" in self._trait_values and self.id and self.id != proposal["value"]:
            raise t.TraitError("Cannot modify id once set.")
        return proposal["value"]


class Volume(anywidget.AnyWidget):
    """
    Represents a Volume model.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the volume data file; cannot be modified once set.
    name : str, optional
        Name of the volume.
    opacity : float, optional
        Opacity between 0.0 (transparent) and 1.0 (opaque). Default is 1.0.
    colormap : str, optional
        Colormap name for rendering. Default is 'gray'.
    colorbar_visible : bool, optional
        Show colorbar associated with the colormap. Default is True.
    cal_min : float or None, optional
        Minimum intensity value for brightness/contrast mapping.
    cal_max : float or None, optional
        Maximum intensity value for brightness/contrast mapping.
    frame4D : int, optional
        Frame index for 4D volume data. Default is 0.
    """

    path = t.Union([t.Instance(pathlib.Path), t.Unicode()]).tag(
        sync=True, to_json=file_serializer
    )
    id = t.Unicode(default_value="").tag(sync=True)
    name = t.Unicode(default_value="").tag(sync=True)
    opacity = t.Float(1.0).tag(sync=True)
    colormap = t.Unicode("gray").tag(sync=True)
    colorbar_visible = t.Bool(True).tag(sync=True)
    cal_min = t.Float(None, allow_none=True).tag(sync=True)
    cal_max = t.Float(None, allow_none=True).tag(sync=True)
    frame4D = t.Int(0).tag(sync=True)

    # other properties that aren't in init
    colormap_invert = t.Bool(False).tag(sync=True)

    def __init__(self, **kwargs):
        if "colormap_invert" in kwargs:
            kwargs.pop("colormap_invert")
        super().__init__(**kwargs)

    @t.validate("path")
    def _validate_path(self, proposal):
        if (
            "path" in self._trait_values
            and self.path
            and self.path != proposal["value"]
        ):
            raise t.TraitError("Cannot modify path once set.")
        return proposal["value"]

    @t.validate("id")
    def _validate_id(self, proposal):
        if "id" in self._trait_values and self.id and self.id != proposal["value"]:
            raise t.TraitError("Cannot modify id once set.")
        return proposal["value"]


class Drawing(anywidget.AnyWidget):
    """
    Represents a Drawing model.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the drawing data file; cannot be modified once set.
    opacity : float, optional
        Opacity between 0.0 (transparent) and 1.0 (opaque). Default is 1.0.
    colormap : list of int, optional
        RGBA color as a list of four integers (0 to 255). Default is [0, 0, 0, 0].
    colorbar_visible : bool, optional
        Show colorbar associated with the drawing. Default is True.
    """

    path = t.Union([t.Instance(pathlib.Path), t.Unicode()]).tag(
        sync=True, to_json=file_serializer
    )
    id = t.Unicode(default_value="").tag(sync=True)
    opacity = t.Float(1.0).tag(sync=True)
    colormap = t.List([0, 0, 0, 0]).tag(sync=True)
    colorbar_visible = t.Bool(True).tag(sync=True)

    @t.validate("path")
    def _validate_path(self, proposal):
        if (
            "path" in self._trait_values
            and self.path
            and self.path != proposal["value"]
        ):
            raise t.TraitError("Cannot modify path once set.")
        return proposal["value"]

    @t.validate("id")
    def _validate_id(self, proposal):
        if "id" in self._trait_values and self.id and self.id != proposal["value"]:
            raise t.TraitError("Cannot modify id once set.")
        return proposal["value"]


class NiiVue(OptionsMixin, anywidget.AnyWidget):
    """
    Represents a NiiVue widget instance.

    This class provides a Jupyter widget for visualizing neuroimaging data using
    NiiVue. It inherits from `OptionsMixin` for default options.
    """

    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"

    id = t.Unicode(default_value=str(uuid.uuid4()), read_only=True).tag(sync=True)

    height = t.Int().tag(sync=True)
    _opts = t.Dict({}).tag(sync=True, to_json=serialize_options)
    _volumes = t.List(t.Instance(Volume), default_value=[]).tag(
        sync=True, **ipywidgets.widget_serialization
    )
    _meshes = t.List(t.Instance(Mesh), default_value=[]).tag(
        sync=True, **ipywidgets.widget_serialization
    )

    # other props
    background_masks_overlays = t.Int(0).tag(sync=True)

    def __init__(self, height: int = 300, **options):  # noqa: D417
        r"""
        Initialize the NiiVue widget.

        Parameters
        ----------
        height : int, optional
            The height of the widget in pixels (default: 300).
        \*\*options : dict, optional
            Additional keyword arguments to configure the NiiVue widget.
            See :class:`ipyniivue.options_mixin.OptionsMixin` for all options.
        """
        # convert to JS camelCase options
        _opts = {
            _SNAKE_TO_CAMEL_OVERRIDES.get(k, snake_to_camel(k)): v
            for k, v in options.items()
        }
        super().__init__(height=height, _opts=_opts, _volumes=[], _meshes=[])

        # handle messages coming from frontend
        self._event_handlers = {}
        self.on_msg(self._handle_custom_msg)

        # extras
        self._added_colormaps = set()

    def _register_callback(self, event_name, callback, remove=False):
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = CallbackDispatcher()
        if remove:
            self._event_handlers[event_name].remove(callback)
        else:
            self._event_handlers[event_name].register_callback(callback)

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
        if event == "azimuth_elevation_change":
            handler(data["azimuth"], data["elevation"])
        elif event == "frame_change":
            idx = self.get_volume_index_by_id(data["id"])
            if idx != -1:
                handler(self._volumes[idx], data["frame_index"])
        elif event in {"image_loaded", "intensity_change"}:
            idx = self.get_volume_index_by_id(data["id"])
            if idx != -1:
                handler(self._volumes[idx])
            else:
                handler(data)
        elif event == "mesh_loaded":
            idx = self.get_mesh_index_by_id(data["id"])
            if idx != -1:
                handler(self._meshes[idx])
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

    def _add_volume_from_frontend(self, volume_data):
        index = volume_data.pop("index", None)
        volume = Volume(**volume_data)
        if index is not None and 0 <= index <= len(self._volumes):
            self._volumes = self._volumes[:index] + [volume] + self._volumes[index:]
        else:
            self._volumes = [*self._volumes, volume]

    def _add_mesh_from_frontend(self, mesh_data):
        index = mesh_data.pop("index", None)
        layers_data = mesh_data.pop("layers", [])
        mesh = Mesh(**mesh_data)
        mesh.layers = [MeshLayer(**layer_data) for layer_data in layers_data]
        if index is not None and 0 <= index <= len(self._meshes):
            self._meshes = self._meshes[:index] + [mesh] + self._meshes[index:]
        else:
            self._meshes = [*self._meshes, mesh]

    def get_volume_index_by_id(self, volume_id: str) -> int:
        """Return the index of the volume with the given id.

        Parameters
        ----------
        volume_id : str
            The id of the volume.
        """
        for idx, vol in enumerate(self._volumes):
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
        for idx, mesh in enumerate(self._meshes):
            if mesh.id == mesh_id:
                return idx
        return -1

    def load_volumes(self, volumes: list):
        """
        Load a list of volume objects.

        Parameters
        ----------
        volumes : list
            A list of dictionaries containing the volume information.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv = NiiVue()
            nv.load_volumes([{"path": "mni152.nii.gz"}])

        """
        volumes = [Volume(**item) for item in volumes]
        self._volumes = volumes

    def add_volume(self, volume: dict):
        """
        Add a new volume to the widget.

        Parameters
        ----------
        volume : dict
            A dictionary containing the volume information.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv = NiiVue()
            nv.add_volume({"path": "mni152.nii.gz"})

        """
        self._volumes = [*self._volumes, Volume(**volume)]

    @property
    def volumes(self):
        """
        Returns the list of volumes.

        Returns
        -------
        list
            A list of dictionairies containing the volume information.

        Examples
        --------
        ::

            print(nv.volumes)

        """
        return list(self._volumes)

    def load_drawings(self, drawings: list):
        """
        Load a list of drawings objects.

        Parameters
        ----------
        drawings : list
            A list of dictionaries containing the drawing information.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv = NiiVue()
            nv.load_drawings([{"path": "lesion.nii.gz"}])

        """
        drawings = [Drawing(**item) for item in drawings]
        self._drawings = drawings

    @property
    def drawings(self):
        """
        Returns the list of drawings.

        Returns
        -------
        list
            A list of dictionairies containing the drawing information.

        Examples
        --------
        ::

            print(nv.drawings)

        """
        return list(self._drawings)

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
        meshes = [Mesh(**item) for item in meshes]
        self._meshes = meshes

    def add_mesh(self, mesh: Mesh):
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
        self._meshes = [*self._meshes, mesh]

    @property
    def meshes(self):
        """
        Returns the list of meshes.

        Returns
        -------
        list
            A list of dictionairies containing the mesh information.

        Examples
        --------
        ::

            print(nv.meshes)

        """
        return list(self._meshes)

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
        save_drawing: bool = True,
        index_volume: int = 0,
    ):
        """
        Save the current image as a nii file.

        Parameters
        ----------
        file_name : str
            The file name to save the image as.
        save_drawing : bool
            A value representing if the drawings should be saved.
        index_volume : int
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
            {"type": "save_image", "data": [file_name, save_drawing, index_volume]}
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

        mesh = self._meshes[idx]
        if layer_index < 0 or layer_index >= len(mesh.layers):
            raise IndexError(f"Layer index {layer_index} out of range.")

        layer = mesh.layers[layer_index]
        setattr(layer, attribute, value)

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
        fallback_colormaps = [
            "actc",
            "afni_blues_inv",
            "afni_reds_inv",
            "batlow",
            "bcgwhw",
            "bcgwhw_dark",
            "blue",
            "blue2cyan",
            "blue2magenta",
            "blue2red",
            "bluegrn",
            "bone",
            "bronze",
            "cet_l17",
            "cividis",
            "cool",
            "copper",
            "copper2",
            "ct_airways",
            "ct_artery",
            "ct_bones",
            "ct_brain",
            "ct_brain_gray",
            "ct_cardiac",
            "ct_head",
            "ct_kidneys",
            "ct_liver",
            "ct_muscles",
            "ct_scalp",
            "ct_skull",
            "ct_soft",
            "ct_soft_tissue",
            "ct_surface",
            "ct_vessels",
            "ct_w_contrast",
            "cubehelix",
            "electric_blue",
            "freesurfer",
            "ge_color",
            "gold",
            "gray",
            "green",
            "green2cyan",
            "green2orange",
            "hot",
            "hotiron",
            "hsv",
            "inferno",
            "jet",
            "kry",
            "linspecer",
            "lipari",
            "magma",
            "mako",
            "navia",
            "nih",
            "plasma",
            "random",
            "red",
            "redyell",
            "rocket",
            "roi_i256",
            "surface",
            "thermal",
            "turbo",
            "violet",
            "viridis",
            "warm",
            "winter",
            "x_rain",
        ]
        colormaps_path = pathlib.Path(__file__).parent / "static" / "colormaps.txt"
        try:
            with open(colormaps_path) as f:
                colormaps_list = f.read().splitlines()
        except FileNotFoundError:
            return fallback_colormaps

        # add custom colormap names
        for key in self._added_colormaps:
            if key not in colormaps_list:
                colormaps_list.append(key)

        return colormaps_list

    def add_colormap(self, name: str, color_map: dict):
        """Add a colormap to the widget.

        Parameters
        ----------
        name : str
            The name of the colormap.
        color_map : dict
            A dictionary containing the colormap information.
            It must have the following keys:

            **Required keys**:
                - `'R'`: list of numbers
                - `'G'`: list of numbers
                - `'B'`: list of numbers
                - `'A'`: list of numbers
                - `'I'`: list of numbers

            **Optional keys**:
                - `'min'`: number
                - `'max'`: number
                - `'labels'`: list of strings

            All the `'R'`, `'G'`, `'B'`, `'A'`, `'I'` lists must have the same length.

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
        # Validate that required keys are present and are lists of numbers
        required_keys = ["R", "G", "B", "A", "I"]
        for key in required_keys:
            if key not in color_map:
                raise ValueError(f"ColorMap must include required key '{key}'")
            if not isinstance(color_map[key], list):
                raise TypeError(f"ColorMap key '{key}' must be a list")
            if not all(isinstance(x, (int, float)) for x in color_map[key]):
                raise TypeError(f"All elements in ColorMap key '{key}' must be numbers")

        # Check that all required lists have the same length
        lengths = [len(color_map[key]) for key in required_keys]
        if len(set(lengths)) != 1:
            raise ValueError(
                "All 'R', 'G', 'B', 'A', 'I' lists must have the same length"
            )

        # Validate optional keys
        if "min" in color_map and not isinstance(color_map["min"], (int, float)):
            raise TypeError("ColorMap 'min' must be a number")

        if "max" in color_map and not isinstance(color_map["max"], (int, float)):
            raise TypeError("ColorMap 'max' must be a number")

        if "labels" in color_map:
            if not isinstance(color_map["labels"], list):
                raise TypeError("ColorMap 'labels' must be a list of strings")
            if not all(isinstance(label, str) for label in color_map["labels"]):
                raise TypeError("All elements in ColorMap 'labels' must be strings")
            if len(color_map["labels"]) != lengths[0]:
                raise ValueError(
                    "ColorMap 'labels' must have the same length "
                    "as 'R', 'G', 'B', 'A', 'I' lists"
                )

        # Save the colormap name
        self._added_colormaps.add(name)

        # Send the colormap to the frontend
        self.send({"type": "add_colormap", "data": [name, color_map]})

    def set_colormap(self, imageID: str, colormap: str):
        """Set the colormap for a volume.

        Parameters
        ----------
        imageID : str
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
        idx = self.get_volume_index_by_id(imageID)
        if idx != -1:
            self._volumes[idx].colormap = colormap
        else:
            raise ValueError(f"Volume with ID '{imageID}' not found")

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

        self.selection_box_color = tuple(color)

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

        self.crosshair_color = tuple(color)

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
        self.crosshair_width = width

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
        if slice_type not in SliceType:
            raise TypeError("slice_type must be a valid SliceType")

        self.slice_type = slice_type

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

        self.send({"type": "set_clip_plane", "data": [depth, azimuth, elevation]})

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
        self.send(
            {"type": "set_render_azimuth_elevation", "data": [azimuth, elevation]}
        )

    def set_mesh_shader(self, mesh_id: str, mesh_shader: str):
        """Set the shader for a mesh.

        Parameters
        ----------
        mesh_id : str
            Identifier of the mesh to change (mesh id).
        mesh_shader : str
            The name of the shader to set.

        Raises
        ------
        ValueError
            If the mesh is not found.

        Examples
        --------
        ::

            nv.set_mesh_shader(nv.meshes[0].id, 'toon')
        """
        idx = self.get_mesh_index_by_id(mesh_id)
        if idx == -1:
            raise ValueError(f"Mesh with id '{mesh_id}' not found.")

        self.send({"type": "set_mesh_shader", "data": [mesh_id, mesh_shader]})

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

    """
    Custom event callbacks
    """

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
                - **frame4D** (int): Frame number for 4D images (default is 0).
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
