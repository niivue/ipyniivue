"""A Jupyter widget for Niivue based on anywidget."""

import importlib.metadata

from .constants import (  # noqa: F401
    ColormapType,
    DragMode,
    MultiplanarType,
    PenType,
    ShowRender,
    SliceType,
)
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
