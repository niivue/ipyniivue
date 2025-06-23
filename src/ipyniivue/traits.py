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
