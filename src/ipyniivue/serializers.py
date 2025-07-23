"""Serializers and deserializers."""

import enum
import math
import pathlib
import typing

import numpy as np

from .config_options import (
    CAMEL_TO_SNAKE,
    SNAKE_TO_CAMEL,
    ConfigOptions,
)
from .traits import (
    CAMEL_TO_SNAKE_GRAPH,
    LUT,
    SNAKE_TO_CAMEL_GRAPH,
    Graph,
    NIFTI1Hdr,
)
from .utils import is_negative_zero


def serialize_file(instance: typing.Union[pathlib.Path, str], widget: object):
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


def serialize_hdr(instance: NIFTI1Hdr, widget: object):
    """
    Serialize the NIFTI1Hdr instance to a dictionary.

    Parameters
    ----------
    instance : NIFTI1Hdr
        The NIFTI1Hdr instance to serialize.
    widget : object
        The NiiVue widget the instance is a part of.

    Returns
    -------
    dict
        A dictionary representation of the NIFTI1Hdr instance.
    """
    data = {}
    if instance:
        for name in instance.trait_names():
            value = getattr(instance, name)
            if value is not None:
                data[name] = value
    return data


def deserialize_hdr(serialized_hdr: dict, widget: object):
    """
    Deserialize a dictionary into a NIFTI1Hdr instance.

    Parameters
    ----------
    serialized_hdr : dict
        The serialized NIFTI1Hdr data from the frontend.
    widget : object
        The NiiVue widget the instance is a part of.

    Returns
    -------
    NIFTI1Hdr
        A reconstructed NIFTI1Hdr instance.
    """
    hdr_args = {}
    for name, value in serialized_hdr.items():
        if name in NIFTI1Hdr.class_traits():
            deserialized_value = value
            hdr_args[name] = deserialized_value
    return NIFTI1Hdr(**hdr_args)


def serialize_ndarray(instance: np.ndarray, widget: object):
    """
    Serialize an ndarray.

    Parameters
    ----------
    instance : np.ndarray
        The array to serialize.
    widget : object
        The widget the instance is a part of.

    Returns
    -------
    dict
        A dictionary representation of the ndarray.
    """
    if instance is None:
        return None
    data_bytes = instance.tobytes()
    dtype_str = str(instance.dtype)
    return {"type": dtype_str, "data": data_bytes}
