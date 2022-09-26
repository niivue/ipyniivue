#!/usr/bin/env python
# coding: utf-8

# Copyright (c) anthony.
# Distributed under the terms of the Modified BSD License.

import pytest

from ipyniivue import Niivue


def test_example_creation_blank():
    w = Niivue()
    assert w.value == None
