"""
Important utilities needed to work data between Python and JavaScript code.

It includes a class to convert from snake to camel case as well as multiple
classes the serialize data to work with JS.
"""

import enum
import math
import pathlib
import typing

from .config_options import (
    CAMEL_TO_SNAKE,
    SNAKE_TO_CAMEL,
    ConfigOptions,
)
from .traits import (
    CAMEL_TO_SNAKE_GRAPH,
    LUT,
    SNAKE_TO_CAMEL_GRAPH,
    ColorMap,
    Graph,
)


def file_serializer(instance: typing.Union[pathlib.Path, str], widget: object):
    """
    Serialize a file to be transferred and read by the JS side.

    Parameters
    ----------
    instance : typing.Union[pathLib.Path, str]
        The path to a file to be serialized.
        Placeholder <fromfrontend> allowed for images added
        from the frontend.
    widget : object
        The NiiVue widget the instance is a part of.
    """
    if instance is None:
        return {"name": None, "data": None}
    if isinstance(instance, str):
        if instance == "<fromfrontend>":
            return {"name": "<fromfrontend>", "data": b""}
        # Make sure we have a pathlib.Path instance
        instance = pathlib.Path(instance)
    return {"name": instance.name, "data": instance.read_bytes()}


def serialize_colormap_label(instance: LUT, widget: object):
    """
    Serialize a LUT instance.

    Parameters
    ----------
    instance : dict
        The list of options to be serialized.
    widget : object
        The NiiVue widget the instance is a part of.
    """
    if isinstance(instance, LUT):
        data = {
            "lut": instance.lut,
            "min": instance.min,
            "max": instance.max,
        }
        if instance.labels:
            data["labels"] = instance.labels
        return data
    else:
        return None


def deserialize_colormap_label(instance: dict, widget: object):
    """
    Deserialize a dictionary into a LUT instance.

    Parameters
    ----------
    instance : dict
        The serialized LUT data.
    widget : object
        The NiiVue widget the instance is a part of.

    Returns
    -------
    LUT or None
        A reconstructed LUT instance or None if the input is None or invalid.
    """
    if instance is None:
        return None
    elif "lut" in instance:
        return LUT(**instance, parent=widget)
    else:
        return None


def clamp(value: float, min_value: int, max_value: int) -> int:
    """
    Clamp the integer part of a value between a minimum and maximum value.

    Parameters
    ----------
    value : float
        The value to be clamped.
    min_value : float
        The minimum value allowed.
    max_value : float
        The maximum value allowed.

    Returns
    -------
    int
        The clamped integer value within the specified range.
    """
    return max(min_value, min(int(value), max_value))


def make_label_lut(cm: ColorMap, alpha_fill: int = 255) -> LUT:
    """
    Convert Colormap into ColormapLabel (LUT).

    Parameters
    ----------
    cm: ColorMap
        The colormap.
    alpha_fill: int
        What to fill for alpha values if they aren't provided in the colormap.

    Examples
    --------
    ::

        lut = make_label_lut(ColorMap(**cmap_data))
    """
    n_labels = len(cm.R)
    if n_labels == 0 or n_labels != len(cm.G) or n_labels != len(cm.B):
        raise ValueError(f"Invalid colormap table: {cm}")

    # Collect indices
    idxs = cm.I if len(cm.I) > 0 else list(range(n_labels))

    if n_labels != len(idxs):
        raise ValueError(
            f"colormap does not make sense: {cm} "
            f"Rs {len(cm.R)} Gs {len(cm.G)} "
            f"Bs {len(cm.B)} Is {len(idxs)}"
        )

    # Ensure idxs are integers
    idxs = [int(idx) for idx in idxs]

    # Prepare alpha values
    if len(cm.A) > 0:
        As = [int(a) for a in cm.A]
    else:
        As = [alpha_fill] * n_labels
        As[0] = 0  # Ensure the first alpha value is 0

    R = [clamp(r, 0, 255) for r in cm.R]
    G = [clamp(g, 0, 255) for g in cm.G]
    B = [clamp(b, 0, 255) for b in cm.B]
    As = [clamp(a, 0, 255) for a in As]

    mn_idx = min(idxs)
    mx_idx = max(idxs)
    n_labels_dense = mx_idx - mn_idx + 1
    lut = [0] * (n_labels_dense * 4)

    for i in range(n_labels):
        k = (idxs[i] - mn_idx) * 4
        lut[k] = R[i]  # Red
        lut[k + 1] = G[i]  # Green
        lut[k + 2] = B[i]  # Blue
        lut[k + 3] = As[i]  # Alpha

    cmap = LUT(lut=lut, min=mn_idx, max=mx_idx)

    # Handle labels
    if cm.labels is not None:
        nL = len(cm.labels)
        if nL == n_labels_dense:
            cmap.labels = cm.labels
        elif nL == n_labels:
            cmap.labels = ["?"] * n_labels_dense
            for i in range(n_labels):
                idx = idxs[i] - mn_idx
                cmap.labels[idx] = cm.labels[i]

    return cmap


def make_draw_lut(cmap: ColorMap) -> LUT:
    """
    Create a draw LUT based on the provided ColorMap.

    Parameters
    ----------
    cmap: ColorMap
        The colormap used to create the LUT.

    Returns
    -------
    LUT
        The resulting LUT object, including labels.
    """
    cm = make_label_lut(cmap, alpha_fill=255)

    # Ensure labels exist and fill up to 256 entries
    if cm.labels is None:
        cm.labels = []
    if len(cm.labels) < 256:
        j = len(cm.labels)
        for i in range(j, 256):
            cm.labels.append(str(i))  # default label

    # Initialize the LUT with default values (opaque red)
    lut = [255, 0, 0, 255] * 256
    lut[3] = 0  # Make the first alpha value transparent

    # Copy the generated LUT values into the initial LUT, up to 256*4 bytes
    explicit_lut_bytes = min(len(cm.lut), 256 * 4)
    if explicit_lut_bytes > 0:
        lut[:explicit_lut_bytes] = cm.lut[:explicit_lut_bytes]

    return LUT(lut=lut, labels=cm.labels)


def is_negative_zero(x):
    """
    Check if float is -0.0.

    Parameters
    ----------
    x : float
        The number to check.

    Returns
    -------
    bool
        The result of the check.
    """
    return x == 0.0 and math.copysign(1.0, x) == -1.0


def serialize_options(instance: ConfigOptions, widget: object):
    """
    Serialize the options for a NiiVue instance, handling infinities and NaN.

    Parameters
    ----------
    instance : ConfigOptions
        The options to be serialized.
    widget : object
        The NiiVue widget the instance is a part of.
    """

    def serialize_value(v):
        if isinstance(v, enum.Enum):
            return v.value
        elif isinstance(v, float):
            if math.isinf(v):
                return "Infinity" if v > 0 else "-Infinity"
            elif math.isnan(v):
                return "NaN"
            elif is_negative_zero(v):
                return "-0"
            else:
                return v
        else:
            return v

    data = {}
    for name in instance.trait_names():
        value = getattr(instance, name)
        camel_name = SNAKE_TO_CAMEL.get(name)
        data[camel_name] = serialize_value(value)
    return data


def deserialize_options(serialized_options: dict, widget: object):
    """
    Deserialize the serialized options, converting special strings back to floats.

    Parameters
    ----------
    serialized_options : dict
        The serialized options dictionary from the frontend.
    widget : object
        The NiiVue widget the instance is a part of.

    Returns
    -------
    dict
        The deserialized options dictionary with proper float values.
    """

    def deserialize_value(v):
        if isinstance(v, str):
            if v == "Infinity":
                return float("inf")
            elif v == "-Infinity":
                return float("-inf")
            elif v == "NaN":
                return float("nan")
            elif v == "-0":
                return -0.0
            else:
                return v
        else:
            return v

    opts = {}
    for camel_name, value in serialized_options.items():
        snake_name = CAMEL_TO_SNAKE.get(camel_name)
        deserialized_value = deserialize_value(value)
        opts[snake_name] = deserialized_value

    return ConfigOptions(**opts)


def serialize_graph(instance: Graph, widget: object):
    """
    Serialize the Graph instance, handling conversion to camelCase as needed.

    Parameters
    ----------
    instance : Graph
        The Graph instance to serialize.
    widget : object
        The NiiVue widget the instance is a part of.
    """
    data = {}
    if instance:
        for name in instance.trait_names():
            value = getattr(instance, name)
            if value is not None:
                camel_name = SNAKE_TO_CAMEL_GRAPH.get(name, name)
                data[camel_name] = value
    return data


def deserialize_graph(serialized_graph: dict, widget: object):
    """
    Deserialize serialized graph data, converting camelCase back to snake_case.

    Parameters
    ----------
    serialized_graph : dict
        The serialized graph dictionary from the frontend.
    widget : object
        The NiiVue widget the instance is a part of.

    Returns
    -------
    Graph
        The deserialized Graph instance.
    """
    graph_args = {}
    for camel_name, value in serialized_graph.items():
        snake_name = CAMEL_TO_SNAKE_GRAPH.get(camel_name, camel_name)
        if snake_name in Graph.class_traits():
            deserialized_value = value
            graph_args[snake_name] = deserialized_value
    return Graph(**graph_args)
