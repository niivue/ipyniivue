#!/usr/bin/env python
# coding: utf-8

# Copyright (c) NiiVue.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..example import Niivue


def test_example_creation_blank():
    w = Niivue()
    assert w.value == 'Hello World'
