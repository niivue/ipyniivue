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


class NIFTI1Hdr(t.HasTraits):
    """
    Represents a NIFTI1 header.

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
    pixDims = t.List(t.Float()).tag(sync=False)  # voxel dimensions
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
