#!/usr/bin/env python
# coding: utf-8

# Copyright (c) NiiVue.
# Distributed under the terms of the Modified BSD License.

#Much of the structure and many of the functions/classes in this file
#are from https://github.com/martinRenou/ipycanvas. The Niivue class comes from Canvas class.

"""
TODO: Add module docstring
"""

from traitlets import (
    Unicode, 
    Instance,
    CInt
)
from ._frontend import module_name, module_version
from ipywidgets import (
    DOMWidget,
    Widget,
    widget_serialization
)

class _CanvasManager(Widget):
    """Private Canvas manager."""

    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    _model_name = Unicode("CanvasManagerModel").tag(sync=True)

    def __init__(self, *args, **kwargs):
        self._caching = kwargs.get("caching", False)
        self._commands_cache = []
        self._buffers_cache = []

        super(_CanvasManager, self).__init__()

    def send_draw_command(self, name, args=[], buffers=[]):
        while len(args) and args[len(args) - 1] is None:
            args.pop()
        self.send_command([name, args, len(buffers)], buffers)

    def send_command(self, command, buffers=[]):
        if self._caching:
            self._commands_cache.append(command)
            self._buffers_cache += buffers
            return
        self._send_custom(command, buffers)

    def flush(self):
        """Flush all the cached commands and clear the cache."""
        if not self._caching or not len(self._commands_cache):
            return

        self._send_custom(self._commands_cache, self._buffers_cache)

        self._commands_cache = []
        self._buffers_cache = []

    def _send_custom(self, command, buffers=[]):
        metadata, command_buffer = commands_to_buffer(command)
        self.send(metadata, buffers=[command_buffer] + buffers)

# Main canvas manager
_CANVAS_MANAGER = _CanvasManager()

class _CanvasBase(DOMWidget):
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    _canvas_manager = Instance(_CanvasManager, default_value=_CANVAS_MANAGER).tag(
        sync=True, **widget_serialization
    )

    height = CInt(480).tag(sync=True)
    width = CInt(640).tag(sync=True)

class Niivue(_CanvasBase):
    """
    Args:
        height (int): The height (in pixels) of the canvas
        width (int): The width (in pixels) of the canvas
    """

    _model_name = Unicode('NiivueModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('NiivueView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode('Hello World').tag(sync=True)

    def __init__(self, *args, **kwargs):
        """Create an Niivue widget."""
        super(Niivue, self).__init__(*args, **kwargs)

        if "caching" in kwargs:
            self._canvas_manager._caching = kwargs["caching"]

        self.on_msg(self._handle_frontend_event)

    def _handle_frontend_event(self, _, content, buffers):
        print('_handle_frontend_event:', content, buffers)

    def setVolume(self, url):
        self.value = url