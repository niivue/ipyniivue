"""
Important utilities needed to work data between Python and JavaScript code.

It includes a class to convert from snake to camel case as well as multiple
classes the serialize data to work with JS.
"""

import math

import numpy as np

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
    """For incoming chunked data."""

    def __init__(self, total_chunks, data_type):
        self.total_chunks = total_chunks
        self.chunks = {}
        self.data_type = data_type

    def add_chunk(self, chunk_index, chunk_data):
        """Add chunk."""
        self.chunks[chunk_index] = chunk_data

    def is_complete(self):
        """Is complete check."""
        return len(self.chunks) == self.total_chunks

    def get_data(self):
        """Get full data bytes."""
        data = b"".join(self.chunks[i] for i in range(self.total_chunks))
        return data

    def get_numpy_array(self):
        """Convert the assembled data into a NumPy array based on data type."""
        data = self.get_data()

        dtype_map = {
            "float32": np.float32,
            "uint32": np.uint32,
            "uint8": np.uint8,
            "int16": np.int16,
            "int32": np.int32,
            "float64": np.float64,
            "uint16": np.uint16,
        }

        if self.data_type not in dtype_map:
            raise ValueError(f"Unsupported data type: {self.data_type}")

        np_dtype = dtype_map[self.data_type]

        numpy_array = np.frombuffer(data, dtype=np_dtype)

        return numpy_array


def find_otsu(volume, mlevel=2):
    """
    Find Otsu thresholds for the given volume.

    Parameters
    ----------
    volume : Volume
        The volume object containing image data and calibration parameters.
    mlevel : int, optional
        The number of levels for multi-level Otsu thresholding (default is 2).

    Returns
    -------
    list of float
        The computed threshold values.
    """
    if mlevel < 2:
        raise ValueError("mlevel must be at least 2 for thresholding.")
    elif mlevel > 4:
        raise NotImplementedError("mlevel greater than 4 is not supported.")

    if volume is None:
        return []

    img = volume.img
    nvox = img.size
    if nvox < 1:
        return []
    nBin = 256
    maxBin = nBin - 1  # bins from 0 to 255
    h = np.zeros(nBin, dtype=int)  # histogram

    # Build 1D histogram
    mn = volume.cal_min
    mx = volume.cal_max
    if mx <= mn:
        return []

    scale2raw = (mx - mn) / nBin

    def bin2raw(bin):
        return bin * scale2raw + mn

    scale2bin = (nBin - 1) / abs(mx - mn)
    inter = volume.hdr.scl_inter
    slope = volume.hdr.scl_slope

    img_scaled = img * slope + inter
    img_clipped = np.clip(img_scaled, mn, mx)
    img_bins = np.round((img_clipped - mn) * scale2bin).astype(int)
    for val in img_bins.flat:
        h[val] += 1

    P = np.zeros((nBin, nBin), dtype=float)
    S = np.zeros((nBin, nBin), dtype=float)

    # diagonal
    for i in range(1, nBin):
        P[i, i] = h[i]
        S[i, i] = i * h[i]

    # calculate first row (row 1)
    for i in range(1, nBin - 1):
        P[1, i + 1] = P[1, i] + h[i + 1]
        S[1, i + 1] = S[1, i] + (i + 1) * h[i + 1]

    # use row 1 to calculate others
    for i in range(2, nBin):
        for j in range(i + 1, nBin):
            P[i, j] = P[1, j] - P[1, i - 1]
            S[i, j] = S[1, j] - S[1, i - 1]

    # calculate H[i][j]
    for i in range(1, nBin):
        for j in range(i + 1, nBin):
            if P[i, j] != 0:
                P[i, j] = (S[i, j] * S[i, j]) / P[i, j]

    num_thresh = mlevel - 1
    t = [0] * num_thresh
    max_val = 0

    if num_thresh == 1:
        for i in range(0, nBin - 1):
            v = P[0, i] + P[i + 1, maxBin]
            if v > max_val:
                t[0] = i
                max_val = v
    elif num_thresh == 2:
        for i in range(0, nBin - 2):
            for h_idx in range(i + 1, nBin - 1):
                v = P[0, i] + P[i + 1, h_idx] + P[h_idx + 1, maxBin]
                if v > max_val:
                    t[0] = i
                    t[1] = h_idx
                    max_val = v
    elif num_thresh == 3:
        for i in range(0, nBin - 3):
            for m in range(i + 1, nBin - 2):
                for h_idx in range(m + 1, nBin - 1):
                    v = P[0, i] + P[i + 1, m] + P[m + 1, h_idx] + P[h_idx + 1, maxBin]
                    if v > max_val:
                        t[0] = i
                        t[1] = m
                        t[2] = h_idx
                        max_val = v

    thresholds = [bin2raw(ti) for ti in t]

    missing = 3 - len(thresholds)
    if missing > 0:
        thresholds.extend([float("inf")] * missing)

    return thresholds


def lerp(x: float, y: float, a: float) -> float:
    """Linear interpolation between x and y by amount a."""
    return x * (1 - a) + y * a


def sph2cart_deg(azimuth: float, elevation: float) -> list[float]:
    """
    Convert spherical coordinates to normalized Cartesian coordinates.

    Parameters
    ----------
    azimuth : float
        Horizontal rotation angle in degrees.
    elevation : float
        Vertical angle from horizontal plane in degrees.

    Returns
    -------
    list[float]
        Normalized 3D Cartesian vector [x, y, z] with unit length.
    """
    phi = -elevation * (math.pi / 180.0)
    theta = ((azimuth - 90.0) % 360.0) * (math.pi / 180.0)
    ret = [
        math.cos(phi) * math.cos(theta),
        math.cos(phi) * math.sin(theta),
        math.sin(phi),
    ]
    length = math.sqrt(ret[0] ** 2 + ret[1] ** 2 + ret[2] ** 2)
    if length > 0.0:
        ret = [x / length for x in ret]
    return ret


def requires_canvas(func):
    """Ensure canvas is attached before method execution."""

    def wrapper(self, *args, **kwargs):
        if not self._canvas_attached:
            operation = func.__name__
            raise RuntimeError(
                f"{operation} needs the canvas to be attached. "
                "Display this widget to attach it to a canvas. "
                "Alternatively, use on_canvas_attached() to defer execution."
            )
        return func(self, *args, **kwargs)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper
