"""Extra classes."""

import traitlets as t


class ColorMap(t.HasTraits):
    """
    Represents a ColorMap.

    Parameters
    ----------
    R : list of float
        The red channel values.
    G : list of float
        The green channel values.
    B : list of float
        The blue channel values.
    A : list of float or None, optional
        The alpha (transparency) channel values.
        Default is None.
    I : list of float or None, optional
        The intensity indices corresponding to the color values.
        Default is None.
    min : float or None, optional
        The minimum intensity value for the colormap. Default is None.
    max : float or None, optional
        The maximum intensity value for the colormap. Default is None.
    labels : list of str or None, optional
        Labels associated with each color entry in the colormap.
        Default is None.
    parent : object, optional
        The parent object that contains this `ColorMap`.
        Used for propagating changes to the parent widget.
        Default is None.
    """

    R = t.List(t.Float()).tag(sync=True)
    G = t.List(t.Float()).tag(sync=True)
    B = t.List(t.Float()).tag(sync=True)
    A = t.List(t.Float(), allow_none=True).tag(sync=True)
    I = t.List(t.Float(), allow_none=True).tag(sync=True)  # noqa: E741
    min = t.Float(allow_none=True).tag(sync=True)
    max = t.Float(allow_none=True).tag(sync=True)
    labels = t.List(t.Unicode(), allow_none=True).tag(sync=True)

    _parent = None

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent = parent

    @t.validate("R", "G", "B", "A", "labels")
    def _validate_color_lists(self, proposal):
        lengths = [len(self.R), len(self.G), len(self.B)]
        if self.A:
            lengths.append(len(self.A))
        if self.labels:
            lengths.append(len(self.labels))
        if len(set(lengths)) != 1:
            raise t.TraitError("R, G, B, A, and labels lists must be the same length.")
        return proposal["value"]

    @t.validate("I")
    def _validate_I_list(self, proposal):
        if self.I and len(self.I) not in (0, len(self.R)):
            raise t.TraitError(
                "I list must be either empty or match the length of R, G, and B."
            )
        return proposal["value"]

    @t.observe("R", "G", "B", "A", "I", "min", "max", "labels")
    def _propagate_parent_change(self, change):
        if self._parent and callable(self._parent._notify_colormap_label_changed):
            self._parent._notify_colormap_label_changed()


class LUT(t.HasTraits):
    """
    Represents a Lookup Table (LUT / Colormap Label).

    Parameters
    ----------
    lut : list of int
        A flat list representing the RGBA values of the lookup table.
    min : float or None, optional
        The minimum intensity value corresponding to the first entry in the LUT.
        Default is None.
    max : float or None, optional
        The maximum intensity value corresponding to the last entry in the LUT.
        Default is None.
    labels : list of str or None, optional
        Labels associated with each color entry in the LUT.
        Default is None.
    parent : object, optional
        The parent object that contains this `LUT`.
        Used for propagating changes to the parent widget.
        Default is None.
    """

    lut = t.List(t.Int()).tag(sync=True)
    min = t.Float(allow_none=True).tag(sync=True)
    max = t.Float(allow_none=True).tag(sync=True)
    labels = t.List(t.Unicode(), allow_none=True).tag(sync=True)

    _parent = None

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent = parent

    @t.observe("lut", "min", "max", "labels")
    def _propagate_parent_change(self, change):
        if self._parent and callable(self._parent._notify_colormap_label_changed):
            self._parent._notify_colormap_label_changed()


class Graph(t.HasTraits):
    """
    Represents a Graph in NiiVue.

    Parameters
    ----------
    ltwh : list of float, optional
        List of four floats representing left, top, width, height.
        Default is [0, 0, 640, 480].
    opacity : float, optional
        Opacity of the graph, between 0.0 (not visible) and 1.0 (visible).
        Default is 0.0.
    vols : list of int, optional
        List of volume indices to be plotted.
        Default is [0].
    auto_size_multiplanar : bool, optional
        Automatically size the graph in multiplanar views.
        Default is False.
    normalize_values : bool, optional
        Normalize the values when plotting.
        Default is False.
    is_range_cal_min_max : bool, optional
        Use the cal_min and cal_max of volumes for value range.
        Default is False.

    plot_ltwh : list of float, optional
        List of four floats specifying the plot area (left, top, width, height).
    back_color : list of float, optional
        RGBA color for the background of the graph.
    line_color : list of float, optional
        RGBA color for the lines in the graph.
    text_color : list of float, optional
        RGBA color for the text in the graph.
    line_thickness : float, optional
        Thickness of the lines in the graph.
    grid_line_thickness : float, optional
        Thickness of the grid lines.
    line_alpha : float, optional
        Alpha (transparency) value for the lines.
    lines : list of list of float, optional
        Data lines to be plotted.
    selected_column : int, optional
        Index of the selected column.
    line_rgb : list of list of float, optional
        List of RGB colors for the lines, each inner list must have exactly 3 floats.

    parent : object, optional
        The parent object that contains this `Graph`.
        Used for propagating changes to the parent widget.
        Default is None.
    """

    # Required fields
    ltwh = t.List(
        t.Float(), default_value=[0.0, 0.0, 640.0, 480.0], minlen=4, maxlen=4
    ).tag(sync=True)
    opacity = t.Float(0.0).tag(sync=True)
    vols = t.List(t.Int(), default_value=[0]).tag(sync=True)
    auto_size_multiplanar = t.Bool(False).tag(sync=True)
    normalize_values = t.Bool(False).tag(sync=True)
    is_range_cal_min_max = t.Bool(False).tag(sync=True)

    # Optional fields
    plot_ltwh = t.List(
        t.Float(), allow_none=True, minlen=4, maxlen=4, default_value=None
    ).tag(sync=True)
    back_color = t.List(
        t.Float(), allow_none=True, minlen=4, maxlen=4, default_value=None
    ).tag(sync=True)
    line_color = t.List(
        t.Float(), allow_none=True, minlen=4, maxlen=4, default_value=None
    ).tag(sync=True)
    text_color = t.List(
        t.Float(), allow_none=True, minlen=4, maxlen=4, default_value=None
    ).tag(sync=True)
    line_thickness = t.Float(None, allow_none=True).tag(sync=True)
    grid_line_thickness = t.Float(None, allow_none=True).tag(sync=True)
    line_alpha = t.Float(None, allow_none=True).tag(sync=True)
    lines = t.List(t.List(t.Float()), allow_none=True, default_value=None).tag(
        sync=True
    )
    selected_column = t.Int(None, allow_none=True).tag(sync=True)
    line_rgb = t.List(
        trait=t.List(t.Float(), minlen=3, maxlen=3),
        allow_none=True,
        default_value=None,
    ).tag(sync=True)

    _parent = None

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent = parent

    _OBSERVED_TRAITS = (
        "ltwh",
        "opacity",
        "vols",
        "auto_size_multiplanar",
        "normalize_values",
        "is_range_cal_min_max",
        "plot_ltwh",
        "back_color",
        "line_color",
        "text_color",
        "line_thickness",
        "grid_line_thickness",
        "line_alpha",
        "lines",
        "selected_column",
        "line_rgb",
    )

    @t.observe(*_OBSERVED_TRAITS)
    def _propagate_parent_change(self, change):
        if self._parent and callable(
            getattr(self._parent, "_notify_graph_changed", None)
        ):
            self._parent._notify_graph_changed()


# ==============================================================================
# NIFTI1Hdr logic and formatting code was ported
# from https://github.com/rii-mango/NIFTI-Reader-JS.
#
# Copyright (c) 2015 RII-UTHSCSA
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ==============================================================================
class NIFTI1Hdr(t.HasTraits):
    """
    Represents a NIFTI1 header.

    Note: Logic and formatting was ported from NIFTI-Reader-JS.

    Properties
    ----------
    littleEndian : bool
        True if the data is in little endian byte order.
    dim_info : int
        MRI slice ordering.
    dims : list of int
        Image dimensions.
    intent_p1 : float
        1st intent parameter.
    intent_p2 : float
        2nd intent parameter.
    intent_p3 : float
        3rd intent parameter.
    intent_code : int
        NIFTI intent code.
    datatypeCode : int
        NIFTI data type code.
    numBitsPerVoxel : int
        Number of bits per voxel.
    slice_start : int
        First slice index.
    slice_end : int
        Last slice index.
    slice_code : int
        Slice timing order.
    pixDims : list of float
        Voxel dimensions.
    vox_offset : float
        Image data offset in bytes.
    scl_slope : float
        Data scaling slope.
    scl_inter : float
        Data scaling intercept.
    xyzt_units : int
        Units of measurement.
    cal_max : float
        Maximum display intensity value.
    cal_min : float
        Minimum display intensity value.
    slice_duration : float
        Time between individual slices.
    toffset : float
        Time axis shift.
    description : str
        Description of the data.
    aux_file : str
        Auxiliary filename.
    intent_name : str
        Name or meaning of the data.
    qform_code : int
        Code specifying the use of quaternion transformation.
    sform_code : int
        Code specifying the use of affine transformation.
    quatern_b : float
        Quaternion b parameter.
    quatern_c : float
        Quaternion c parameter.
    quatern_d : float
        Quaternion d parameter.
    qoffset_x : float
        Quaternion x translation parameter.
    qoffset_y : float
        Quaternion y translation parameter.
    qoffset_z : float
        Quaternion z translation parameter.
    affine : list of list of float
        Affine transformation matrix.
    magic : str
        Magic code indicating file type.
    extensionFlag : list of int
        Extensions flag.
    """

    littleEndian = t.Bool().tag(sync=False)
    dim_info = t.Int().tag(sync=False)
    dims = t.List(t.Int()).tag(sync=False)  # image dimensions
    intent_p1 = t.Float().tag(sync=False)
    intent_p2 = t.Float().tag(sync=False)
    intent_p3 = t.Float().tag(sync=False)
    intent_code = t.Int().tag(sync=False)
    datatypeCode = t.Int().tag(sync=False)
    numBitsPerVoxel = t.Int().tag(sync=False)
    slice_start = t.Int().tag(sync=False)
    slice_end = t.Int().tag(sync=False)
    slice_code = t.Int().tag(sync=False)
    pixDims = t.List(t.Float(allow_none=True)).tag(sync=False)
    vox_offset = t.Float().tag(sync=False)
    scl_slope = t.Float().tag(sync=False)
    scl_inter = t.Float().tag(sync=False)
    xyzt_units = t.Int().tag(sync=False)
    cal_max = t.Float().tag(sync=False)
    cal_min = t.Float().tag(sync=False)
    slice_duration = t.Float().tag(sync=False)
    toffset = t.Float().tag(sync=False)
    description = t.Unicode().tag(sync=False)
    aux_file = t.Unicode().tag(sync=False)
    intent_name = t.Unicode().tag(sync=False)
    qform_code = t.Int().tag(sync=False)
    sform_code = t.Int().tag(sync=False)
    quatern_b = t.Float().tag(sync=False)
    quatern_c = t.Float().tag(sync=False)
    quatern_d = t.Float().tag(sync=False)
    qoffset_x = t.Float().tag(sync=False)
    qoffset_y = t.Float().tag(sync=False)
    qoffset_z = t.Float().tag(sync=False)
    affine = t.List(t.List(t.Float())).tag(sync=False)
    magic = t.Unicode().tag(sync=False)
    extensionFlag = t.List(t.Int()).tag(sync=False)

    # Datatype codes
    TYPE_NONE = 0
    TYPE_BINARY = 1
    TYPE_UINT8 = 2
    TYPE_INT16 = 4
    TYPE_INT32 = 8
    TYPE_FLOAT32 = 16
    TYPE_COMPLEX64 = 32
    TYPE_FLOAT64 = 64
    TYPE_RGB24 = 128
    TYPE_INT8 = 256
    TYPE_UINT16 = 512
    TYPE_UINT32 = 768
    TYPE_INT64 = 1024
    TYPE_UINT64 = 1280
    TYPE_FLOAT128 = 1536
    TYPE_COMPLEX128 = 1792
    TYPE_COMPLEX256 = 2048

    # Unit codes
    SPATIAL_UNITS_MASK = 0x07
    TEMPORAL_UNITS_MASK = 0x38
    UNITS_UNKNOWN = 0
    UNITS_METER = 1
    UNITS_MM = 2
    UNITS_MICRON = 3
    UNITS_SEC = 8
    UNITS_MSEC = 16
    UNITS_USEC = 24
    UNITS_HZ = 32
    UNITS_PPM = 40
    UNITS_RADS = 48

    # Transform codes
    XFORM_UNKNOWN = 0
    XFORM_SCANNER_ANAT = 1
    XFORM_ALIGNED_ANAT = 2
    XFORM_TALAIRACH = 3
    XFORM_MNI_152 = 4

    @staticmethod
    def _format_number(num, short_format=False):
        """Format a number to specific precision, similar to JS toPrecision."""
        if num is None:
            return 0.0
        val = float(num)
        precision = 5 if short_format else 7
        formatted = f"{val:.{precision}g}"
        return float(formatted)

    def _get_datatype_code_string(self, code):
        """Return a human-readable string for datatype codes."""
        mapping = {
            self.TYPE_UINT8: "1-Byte Unsigned Integer",
            self.TYPE_INT16: "2-Byte Signed Integer",
            self.TYPE_INT32: "4-Byte Signed Integer",
            self.TYPE_FLOAT32: "4-Byte Float",
            self.TYPE_FLOAT64: "8-Byte Float",
            self.TYPE_RGB24: "RGB",
            self.TYPE_INT8: "1-Byte Signed Integer",
            self.TYPE_UINT16: "2-Byte Unsigned Integer",
            self.TYPE_UINT32: "4-Byte Unsigned Integer",
            self.TYPE_INT64: "8-Byte Signed Integer",
            self.TYPE_UINT64: "8-Byte Unsigned Integer",
        }
        return mapping.get(code, "Unknown")

    def _get_units_code_string(self, code):
        """Return a human-readable string for unit codes."""
        mapping = {
            self.UNITS_METER: "Meters",
            self.UNITS_MM: "Millimeters",
            self.UNITS_MICRON: "Microns",
            self.UNITS_SEC: "Seconds",
            self.UNITS_MSEC: "Milliseconds",
            self.UNITS_USEC: "Microseconds",
            self.UNITS_HZ: "Hz",
            self.UNITS_PPM: "PPM",
            self.UNITS_RADS: "Rads",
        }
        return mapping.get(code, "Unknown")

    def _get_transform_code_string(self, code):
        """Return a human-readable string for transform codes."""
        mapping = {
            self.XFORM_SCANNER_ANAT: "Scanner",
            self.XFORM_ALIGNED_ANAT: "Aligned",
            self.XFORM_TALAIRACH: "Talairach",
            self.XFORM_MNI_152: "MNI",
        }
        return mapping.get(code, "Unknown")

    def to_formatted_string(self):
        """Return a formatted string of header fields."""
        string = ""

        string += f"Dim Info = {self.dim_info}\n"

        d = self.dims + [0] * (8 - len(self.dims))
        string += (
            f"Image Dimensions (1-8): {d[0]}, {d[1]}, {d[2]}, {d[3]}, "
            f"{d[4]}, {d[5]}, {d[6]}, {d[7]}\n"
        )

        string += (
            f"Intent Parameters (1-3): {self.intent_p1}, "
            f"{self.intent_p2}, {self.intent_p3}\n"
        )
        string += f"Intent Code = {self.intent_code}\n"

        type_str = self._get_datatype_code_string(self.datatypeCode)
        string += f"Datatype = {self.datatypeCode} ({type_str})\n"

        string += f"Bits Per Voxel = {self.numBitsPerVoxel}\n"
        string += f"Slice Start = {self.slice_start}\n"

        pd = (self.pixDims or []) + [0.0] * 8
        string += (
            f"Voxel Dimensions (1-8): {self._format_number(pd[0])}, "
            f"{self._format_number(pd[1])}, {self._format_number(pd[2])}, "
            f"{self._format_number(pd[3])}, {self._format_number(pd[4])}, "
            f"{self._format_number(pd[5])}, {self._format_number(pd[6])}, "
            f"{self._format_number(pd[7])}\n"
        )

        string += f"Image Offset = {self.vox_offset}\n"
        string += (
            f"Data Scale:  Slope = {self._format_number(self.scl_slope)}  "
            f"Intercept = {self._format_number(self.scl_inter)}\n"
        )
        string += f"Slice End = {self.slice_end}\n"
        string += f"Slice Code = {self.slice_code}\n"

        spatial = self._get_units_code_string(self.SPATIAL_UNITS_MASK & self.xyzt_units)
        temporal = self._get_units_code_string(
            self.TEMPORAL_UNITS_MASK & self.xyzt_units
        )
        string += f"Units Code = {self.xyzt_units} ({spatial}, {temporal})\n"

        string += (
            f"Display Range:  Max = {self._format_number(self.cal_max)}  "
            f"Min = {self._format_number(self.cal_min)}\n"
        )
        string += f"Slice Duration = {self.slice_duration}\n"
        string += f"Time Axis Shift = {self.toffset}\n"
        string += f'Description: "{self.description}"\n'
        string += f'Auxiliary File: "{self.aux_file}"\n'

        q_str = self._get_transform_code_string(self.qform_code)
        string += f"Q-Form Code = {self.qform_code} ({q_str})\n"

        s_str = self._get_transform_code_string(self.sform_code)
        string += f"S-Form Code = {self.sform_code} ({s_str})\n"

        string += (
            f"Quaternion Parameters:  "
            f"b = {self._format_number(self.quatern_b)}  "
            f"c = {self._format_number(self.quatern_c)}  "
            f"d = {self._format_number(self.quatern_d)}\n"
        )

        string += (
            f"Quaternion Offsets:  "
            f"x = {self.qoffset_x}  "
            f"y = {self.qoffset_y}  "
            f"z = {self.qoffset_z}\n"
        )

        af = (
            self.affine
            if self.affine and len(self.affine) >= 3
            else [[0] * 4, [0] * 4, [0] * 4]
        )

        string += (
            f"S-Form Parameters X: {self._format_number(af[0][0])}, "
            f"{self._format_number(af[0][1])}, {self._format_number(af[0][2])}, "
            f"{self._format_number(af[0][3])}\n"
        )

        string += (
            f"S-Form Parameters Y: {self._format_number(af[1][0])}, "
            f"{self._format_number(af[1][1])}, {self._format_number(af[1][2])}, "
            f"{self._format_number(af[1][3])}\n"
        )

        string += (
            f"S-Form Parameters Z: {self._format_number(af[2][0])}, "
            f"{self._format_number(af[2][1])}, {self._format_number(af[2][2])}, "
            f"{self._format_number(af[2][3])}\n"
        )

        string += f'Intent Name: "{self.intent_name}"\n'

        return string

    def __str__(self):
        """Return the formatted string representation of the header."""
        return self.to_formatted_string()


class Scene(t.HasTraits):
    """
    Represents the scene configuration for NiiVue.

    Parameters
    ----------
    render_azimuth : float
        The azimuth angle in degrees around the object.
    render_elevation : float
        The elevation angle in degrees.
    vol_scale_multiplier : float
        Scale multiplier for volume rendering.
    crosshair_pos : list of float
        The crosshair position as a list of 3 floats.
    clip_planes : list of list of float
        A list of clipping planes, where each plane is defined
        by four floats `[x, y, z, w]` representing the plane equation.
    clip_plane_depth_azi_elevs : list of list of float
        A list of lists of `[depth, azimuth, elevation]`.
    pan2d_xyzmm : list of float
        The 2D pan in 3D mm as a list of 4 floats.
    gamma : float
        The gamma value for rendering.
    """

    render_azimuth = t.Float(110.0).tag(sync=True)
    render_elevation = t.Float(10.0).tag(sync=True)
    vol_scale_multiplier = t.Float(1.0).tag(sync=True)
    crosshair_pos = t.List(
        t.Float(), default_value=[0.5, 0.5, 0.5], minlen=3, maxlen=3
    ).tag(sync=True)
    # [0.0, 0.0, 0.0, 0.0]
    clip_planes = t.List(t.List(t.Float()), default_value=[[0.0, 0.0, 0.0, 0.0]]).tag(
        sync=True
    )
    # [2.0, 0.0, 0.0]
    clip_plane_depth_azi_elevs = t.List(
        t.List(t.Float()), default_value=[[2.0, 0.0, 0.0]]
    ).tag(sync=True)
    pan2d_xyzmm = t.List(
        t.Float(), default_value=[0.0, 0.0, 0.0, 1.0], minlen=4, maxlen=4
    ).tag(sync=True)
    gamma = t.Float(1.0).tag(sync=True)

    # parent
    _parent = None

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent = parent

    @property
    def scene_data(self):
        """Return the scene data as a dict with properties in snake_case."""
        data = {
            "gamma": self.gamma,
            "azimuth": self.render_azimuth,
            "elevation": self.render_elevation,
            "crosshair_pos": self.crosshair_pos,
            "clip_planes": self.clip_planes,
            "clip_plane_depth_azi_elevs": self.clip_plane_depth_azi_elevs,
            "vol_scale_multiplier": self.vol_scale_multiplier,
            "pan2d_xyzmm": self.pan2d_xyzmm,
        }
        return data

    _OBSERVED_TRAITS = (
        "render_azimuth",
        "render_elevation",
        "vol_scale_multiplier",
        "crosshair_pos",
        "clip_planes",
        "clip_plane_depth_azi_elevs",
        "pan2d_xyzmm",
        "gamma",
    )

    @t.observe(*_OBSERVED_TRAITS)
    def _propagate_parent_change(self, change):
        if self._parent and callable(
            getattr(self._parent, "_notify_scene_changed", None)
        ):
            self._parent._notify_scene_changed()


class VolumeObject3DData(t.HasTraits):
    """
    Represents data from a 3D volume object, partial of niivue's NiivueObject3D.

    Properties
    ----------
    id : int
        Unique identifier for the object.
    extents_min : list of float
        Minimum extents of the object in each dimension.
    extents_max : list of float
        Maximum extents of the object in each dimension.
    scale : list of float
        Scale factors for each dimension.
    furthest_vertex_from_origin : float or None
        Distance to the furthest vertex from the origin.
    field_of_view_de_oblique_mm : list of float or None
        Field of view in de-oblique millimeters.
    """

    id = t.Int().tag(sync=False)
    extents_min = t.List(t.Float()).tag(sync=False)
    extents_max = t.List(t.Float()).tag(sync=False)
    scale = t.List(t.Float()).tag(sync=False)
    furthest_vertex_from_origin = t.Float(allow_none=True, default_value=None).tag(
        sync=False
    )
    field_of_view_de_oblique_mm = t.List(
        t.Float(), allow_none=True, default_value=None
    ).tag(sync=False)

    @t.validate(
        "id",
        "extents_min",
        "extents_max",
        "scale",
        "furthest_vertex_from_origin",
        "field_of_view_de_oblique_mm",
    )
    def _validate_no_change(self, proposal):
        trait_name = proposal["trait"].name
        if (
            trait_name in self._trait_values
            and (
                self._trait_values[trait_name] or self._trait_values[trait_name] == 0.0
            )
            and self._trait_values[trait_name] != proposal["value"]
        ):
            raise t.TraitError(f"Cannot modify '{trait_name}' once set.")
        return proposal["value"]


CAMEL_TO_SNAKE_SCENE = {
    "renderAzimuth": "render_azimuth",
    "renderElevation": "render_elevation",
    "volScaleMultiplier": "vol_scale_multiplier",
    "crosshairPos": "crosshair_pos",
    "clipPlanes": "clip_planes",
    "clipPlaneDepthAziElevs": "clip_plane_depth_azi_elevs",
    "pan2Dxyzmm": "pan2d_xyzmm",
    "gamma": "gamma",
}

SNAKE_TO_CAMEL_SCENE = {v: k for k, v in CAMEL_TO_SNAKE_SCENE.items()}

CAMEL_TO_SNAKE_GRAPH = {
    "LTWH": "ltwh",
    "opacity": "opacity",
    "vols": "vols",
    "autoSizeMultiplanar": "auto_size_multiplanar",
    "normalizeValues": "normalize_values",
    "isRangeCalMinMax": "is_range_cal_min_max",
    "plotLTWH": "plot_ltwh",
    "backColor": "back_color",
    "lineColor": "line_color",
    "textColor": "text_color",
    "lineThickness": "line_thickness",
    "gridLineThickness": "grid_line_thickness",
    "lineAlpha": "line_alpha",
    "lines": "lines",
    "selectedColumn": "selected_column",
    "lineRGB": "line_rgb",
}

SNAKE_TO_CAMEL_GRAPH = {v: k for k, v in CAMEL_TO_SNAKE_GRAPH.items()}
