#!/usr/bin/env python
# coding: utf-8

# Copyright (c) anthony.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget, ValueWidget, register
from traitlets import Unicode, Bool, validate, TraitError, Int

from ._frontend import module_name, module_version

@register
class Niivue(DOMWidget, ValueWidget):
    _model_name = Unicode('NiivueModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    _view_name = Unicode('NiivueView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    height = Int(480).tag(sync=True)
    #width = Int(640).tag(sync=True)
    #value = Unicode('example@example.com').tag(sync=True)
    #disabled = Bool(False, help="Enable or disable user changes.").tag(sync=True)
