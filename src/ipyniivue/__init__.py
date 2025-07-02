"""A Jupyter widget for Niivue based on anywidget."""

import importlib.metadata

from .constants import DragMode, MultiplanarType, ShowRender, SliceType  # noqa: F401
from .download_dataset import download_dataset  # noqa: F401
from .traits import (  # noqa: F401
    LUT,
    ColorMap,
    Graph,
)
from .widget import (  # noqa: F401
    Mesh,
    MeshLayer,
    NiiVue,
    Volume,
    WidgetObserver,
)

__version__ = importlib.metadata.version("ipyniivue")
