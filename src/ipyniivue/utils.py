"""
Important utilities needed to work data between Python and JavaScript code.

It includes a class to convert from snake to camel case as well as multiple
classes the serialize data to work with JS.
"""

import enum
import pathlib
import typing

from .traits import LUT, ColorMap


def snake_to_camel(snake_str: str):
    """
    Convert the Python typical snake case to JS typical camel case.

    Parameters
    ----------
    snake_str : str
        The snake case string to be converted.

    Returns
    -------
    camel_string : str
        The parameter string converted to camel case.
    """
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


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
    if isinstance(instance, str):
        if instance == "<fromfrontend>":
            return {"name": "<fromfrontend>", "data": b""}
        # Make sure we have a pathlib.Path instance
        instance = pathlib.Path(instance)
    return {"name": instance.name, "data": instance.read_bytes()}


def serialize_options(instance: dict, widget: object):
    """
    Serialize the options for a NiiVue instance.

    Parameters
    ----------
    instance : dict
        The list of options to be serialized.
    widget : object
        The NiiVue widget the instance is a part of.
    """
    # Serialize enums as their value
    return {k: v.value if isinstance(v, enum.Enum) else v for k, v in instance.items()}


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
