class NVMesh:
    #gl variable skipped because python
    def __init__(self, input_dict={}, **kwargs):
        kwargs.update(input_dict)
        self.pts = kwargs.get("pts", []) #arent pts and tris required?
        self.tris = kwargs.get("tris", [])
        self.name = kwargs.get("name", "")
        self.rgba255 = kwargs.get("rgba255", [255, 255, 255, 255])
        self.opacity = kwargs.get("opacity", 1.0)
        self.visible = kwargs.get("visible", True)
        self.connectome = kwargs.get("connectome", None)
        self.dpg = kwargs.get("dpg", None)
        self.dps = kwargs.get("dps", None)
        self.dpv = kwargs.get("dpv", None)
        self.colorbar_visible = kwargs.get("colorbar_visible", True)

        self.id = kwargs.get("id", "")

    def __iter__(self):
        yield 'pts', self.pts
        yield 'tris', self.tris
        yield 'name', self.name
        yield 'rgba255', self.rgba255
        yield 'opacity', self.opacity
        yield 'visible', self.visible
        yield 'connectome', self.connectome
        yield 'dpg', self.dpg
        yield 'dps', self.dps
        yield 'dpv', self.dpv
        yield 'colorbarVisible', self.colorbar_visible

    @staticmethod
    def load_from_base64(**kwargs):
        #to be implemented
        pass