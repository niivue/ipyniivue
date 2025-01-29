"""A Jupyter widget for Niivue based on anywidget."""

import importlib.metadata

from .constants import DragMode, MuliplanarType, SliceType  # noqa: F401
from .download_dataset import download_dataset  # noqa: F401
from .widget import NiiVue, WidgetObserver  # noqa: F401

__version__ = importlib.metadata.version("ipyniivue")
