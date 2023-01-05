#!/usr/bin/env python
# coding: utf-8

# Copyright (c) NiiVue.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import Bool, CInt, Unicode
from ._frontend import module_name, module_version


class NiiVue(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('NiiVueModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('NiiVueView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    width = CInt(350).tag(sync=True)
    height = CInt(250).tag(sync=True)
    _send_client_ready_event = Bool(True).tag(sync=True)

    def __init__(self, **kwargs):
        super(NiiVue, self).__init__(**kwargs)
