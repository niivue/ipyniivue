import pathlib

import anywidget
import ipywidgets
import traitlets as t

from ._constants import _SNAKE_TO_CAMEL_OVERRIDES
from ._options_mixin import OptionsMixin
from ._utils import file_serializer, serialize_options, snake_to_camel

__all__ = ["AnyNiivue"]


class Volume(ipywidgets.Widget):
    path = t.Union([t.Instance(pathlib.Path), t.Unicode()]).tag(
        sync=True, to_json=file_serializer
    )
    opacity = t.Float(1.0).tag(sync=True)
    colormap = t.Unicode("gray").tag(sync=True)
    colorbar_visible = t.Bool(True).tag(sync=True)
    cal_min = t.Float(None, allow_none=True).tag(sync=True)
    cal_max = t.Float(None, allow_none=True).tag(sync=True)


class AnyNiivue(OptionsMixin, anywidget.AnyWidget):
    """Represents a Niivue instance."""

    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _opts = t.Dict({}).tag(sync=True, to_json=serialize_options)
    _volumes = t.List(t.Instance(Volume), default_value=[]).tag(
        sync=True, **ipywidgets.widget_serialization
    )

    def __init__(self, **opts):
        # convert to JS camelCase options
        _opts = {
            _SNAKE_TO_CAMEL_OVERRIDES.get(k, snake_to_camel(k)): v
            for k, v in opts.items()
        }
        super().__init__(_opts=_opts, _volumes=[])

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
        return self._volumes
