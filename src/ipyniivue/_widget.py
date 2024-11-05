import pathlib

import anywidget
import ipywidgets
import traitlets as t

from ._constants import _SNAKE_TO_CAMEL_OVERRIDES
from ._options_mixin import OptionsMixin
from ._utils import (
    file_serializer,
    mesh_layers_serializer,
    serialize_options,
    snake_to_camel,
)

__all__ = ["NiiVue"]


class Mesh(ipywidgets.Widget):
    path = t.Union([t.Instance(pathlib.Path), t.Unicode()]).tag(
        sync=True, to_json=file_serializer
    )
    rgba255 = t.List([0, 0, 0, 0]).tag(sync=True)
    opacity = t.Float(1.0).tag(sync=True)
    visible = t.Bool(True).tag(sync=True)
    layers = t.List([]).tag(sync=True, to_json=mesh_layers_serializer)


class Volume(ipywidgets.Widget):
    path = t.Union([t.Instance(pathlib.Path), t.Unicode()]).tag(
        sync=True, to_json=file_serializer
    )
    opacity = t.Float(1.0).tag(sync=True)
    colormap = t.Unicode("gray").tag(sync=True)
    colorbar_visible = t.Bool(True).tag(sync=True)
    cal_min = t.Float(None, allow_none=True).tag(sync=True)
    cal_max = t.Float(None, allow_none=True).tag(sync=True)


class NiiVue(OptionsMixin, anywidget.AnyWidget):
    """Represents a Niivue instance."""

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
        """Load a list of volumes into the widget.

        Parameters
        ----------
        volumes : list
            A list of dictionaries containing the volume information.
        """
        volumes = [Volume(**item) for item in volumes]
        self._volumes = volumes

    def add_volume(self, volume: dict):
        """Add a single volume to the widget.

        Parameters
        ----------
        volume : dict
            A dictionary containing the volume information.
        """
        self._volumes = [*self._volumes, Volume(**volume)]

    @property
    def volumes(self):
        """Returns the list of volumes."""
        return list(self._volumes)

    def load_meshes(self, meshes: list):
        """Load a list of meshes into the widget.

        Parameters
        ----------
        meshes : list
            A list of dictionaries containing the mesh information.
        """
        meshes = [Mesh(**item) for item in meshes]
        self._meshes = meshes

    def add_mesh(self, mesh: Mesh):
        """Add a single mesh to the widget.

        Parameters
        ----------
        mesh : dict
            A dictionary containing the mesh information.
        """
        self._meshes = [*self._meshes, mesh]

    @property
    def meshes(self):
        """Returns the list of meshes."""
        return list(self._meshes)

class WidgetObserver:
    """Sets an observed for `widget` on the `attribute` of `object`."""

    def __init__(self, widget, object, attribute):
        self.widget = widget
        self.object = object
        self.attribute = attribute
        self._observe()

    def _widget_change(self, change):
        setattr(self.object, self.attribute, change["new"])

    def _observe(self):
        self.widget.observe(self._widget_change, names=["value"])
