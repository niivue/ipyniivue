import importlib.metadata

from ._constants import SliceType, DragMode, MuliplanarType # noqa
from ._widget import AnyNiivue # noqa

try:
    __version__ = importlib.metadata.version("ipyniivue_experimental")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
