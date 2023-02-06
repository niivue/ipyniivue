#!/usr/bin/env python
# coding: utf-8

# Copyright (c) NiiVue.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..niivue import Niivue


def test_example_creation_blank():
    nv = Niivue()
    assert nv.thumbnail == ''
