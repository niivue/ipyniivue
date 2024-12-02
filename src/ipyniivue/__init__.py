"""A Jupyter widget for Niivue based on anywidget."""

import importlib.metadata

from ._constants import DragMode, MuliplanarType, SliceType  # noqa: F401
from ._widget import NiiVue, WidgetObserver  # noqa: F401

__version__ = importlib.metadata.version("ipyniivue")
