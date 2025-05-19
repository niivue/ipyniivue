"""
Widgets representing NiiVue model instances as well as volume, mesh, and drawing models.

Aside from setting up the Mesh, Volume, Drawing, and NiiVue widgets, this module
contains many of the classes needed to make NiiVue instances work, such as classes
to load objects in, change attributes of this instance, and more.
"""

import pathlib

import anywidget
import ipywidgets
import traitlets as t

from .constants import _SNAKE_TO_CAMEL_OVERRIDES
from .options_mixin import OptionsMixin
from .utils import (
    file_serializer,
    mesh_layers_serializer,
    serialize_options,
    snake_to_camel,
)

__all__ = ["NiiVue"]


class Mesh(ipywidgets.Widget):
    """
    Represents a Mesh model.

    Parameters
    ----------
    ipywidgets.Widget : A widget representing a mesh model and its data.
    """

    path = t.Union([t.Instance(pathlib.Path), t.Unicode()]).tag(
        sync=True, to_json=file_serializer
    )
    id = t.Unicode(default_value="").tag(sync=True)
    name = t.Unicode(default_value="").tag(sync=True)
    rgba255 = t.List([0, 0, 0, 0]).tag(sync=True)
    opacity = t.Float(1.0).tag(sync=True)
    visible = t.Bool(True).tag(sync=True)
    layers = t.List([]).tag(sync=True, to_json=mesh_layers_serializer)

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


class Volume(ipywidgets.Widget):
    """
    Represents a Volume model.

    Parameters
    ----------
    ipywidgets.Widget : A widget representing a volume model and its data.
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


class Drawing(ipywidgets.Widget):
    """
    Represents a Drawing model.

    Parameters
    ----------
    ipywidgets.Widget : A widget representing a drawing model and its data.
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
    Represents a Niivue instance.

    Parameters
    ----------
    OptionsMixin : The list of default options for a NiiVue instance.
    anywidget.Anywidget : An AnyWidget model representing a NiiVue
        instance and its data.
    """

    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"

    height = t.Int().tag(sync=True)
    _opts = t.Dict({}).tag(sync=True, to_json=serialize_options)
    _volumes = t.List(t.Instance(Volume), default_value=[]).tag(
        sync=True, **ipywidgets.widget_serialization
    )
    _meshes = t.List(t.Instance(Mesh), default_value=[]).tag(
        sync=True, **ipywidgets.widget_serialization
    )

    def __init__(self, height: int = 300, **options):
        # convert to JS camelCase options
        _opts = {
            _SNAKE_TO_CAMEL_OVERRIDES.get(k, snake_to_camel(k)): v
            for k, v in options.items()
        }
        super().__init__(height=height, _opts=_opts, _volumes=[], _meshes=[])

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


class WidgetObserver:
    """Creates an observer on the `attribute` of `object` for a `widget`."""

    def __init__(self, widget, obj, attribute):
        self.widget = widget
        self.object = obj
        self.attribute = attribute
        self._observe()

    def _widget_change(self, change):
        # Converts string to float because negative 0 as a float
        # with ipywidgets does not work as expected.
        setattr(self.object, self.attribute, float(change["new"]))

    def _observe(self):
        self.widget.observe(self._widget_change, names=["value"])
