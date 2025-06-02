"""A Jupyter widget for Niivue based on anywidget."""

import importlib.metadata

from .constants import DragMode, MultiplanarType, ShowRender, SliceType  # noqa: F401
from .download_dataset import download_dataset  # noqa: F401
from .widget import (  # noqa: F401
    Drawing,
    Mesh,
    MeshLayer,
    NiiVue,
    Volume,
    WidgetObserver,
)

__version__ = importlib.metadata.version("ipyniivue")
