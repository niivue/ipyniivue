"""
Important utilities needed to work data between Python and JavaScript code.

It includes a class to convert from snake to camel case as well as multiple
classes the serialize data to work with JS.
"""

import math

from .traits import (
    LUT,
    ColorMap,
)


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


class ChunkedDataHandler:
    """For incoming chuned data."""

    def __init__(self, total_chunks):
        self.total_chunks = total_chunks
        self.chunks = {}

    def add_chunk(self, chunk_index, chunk_data):
        """Add chunk."""
        self.chunks[chunk_index] = chunk_data

    def is_complete(self):
        """Boolean is complete check."""
        return len(self.chunks) == self.total_chunks

    def get_data(self):
        """Get full data bytes."""
        data = b"".join(self.chunks[i] for i in range(self.total_chunks))
        return data
