import importlib.metadata
import pathlib

import anywidget
import traitlets

try:
    __version__ = importlib.metadata.version("ipyniivue_experimental")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"



from enum import Enum

class SLICE_TYPE(Enum):
    AXIAL = 1
    CORONAL = 2
    SAGITTAL = 3
    MULTIPLANAR = 4
    RENDER = 5


class DRAG_MODES(Enum):
   CONTRAST = 1
   MEASUREMENT = 2
   PAN = 3


import anywidget 
import traitlets
import pathlib

def file_serializer(instance: pathlib.Path, widget):
    return {
        "name": instance.name,
        "data": instance.read_bytes()
    }

class AnyNiivue(anywidget.AnyWidget):
  path_root = pathlib.Path.cwd()
  _esm = path_root / "src" / "ipyniivue_experimental"/ "static" / "widget_traitlet.js"

  volume_file = traitlets.Instance(pathlib.Path).tag(sync=True, to_json=file_serializer)

  def load_volume(self, value):
     self.volume_file = value

  opacity = traitlets.Float(1.0).tag(sync = True)
  
  def set_opacity(self, value):
    self.opacity = value
  def get_opacitiy(self):
    return self.opacity
  
  colormap = traitlets.Unicode("").tag(sync = True)
  
  def set_colormap(self, value):
    self.colormap = value

  def get_colormap(self):
    return self.colormap
  
  slice_type = traitlets.Integer(0).tag(sync = True)
  
  def set_slice_type(self, my_slice_type):
    self.slice_type = int(my_slice_type.value)

  drag_mode = traitlets.Unicode("").tag(sync = True)
  
  def set_drag_mode(self, value):
    self.drag_mode = str(value)


   





import anywidget 
import pathlib

class AnyNiivueOldSend(anywidget.AnyWidget):
  path_root = pathlib.Path(__file__).parent / "static" 
  _esm = path_root / "widget_send.js"

  def load_volumes(self, volume_list):
    self.send({ "type": "api", "func": "loadVolumes", "args": [volume_list] })

  def load_meshes(self, mesh_list):
    self.send({ "type": "api", "func": "loadMeshes", "args": [mesh_list] })


  def set_opacity(self, opacity=1):
      self.send(
          {"type": "api", "func": "setOpacity", "args": [[0], [opacity]]}
      )


  def set_crosshair_color(self, color):
        self.send(
          {"type": "api", "func": "setCrosshairColor", "args": [color]}
        )

  def set_crosshair_color(self, color):
        self.send(
          {"type": "api", "func": "setCrosshairColor", "args": [color]}
        )

  def set_crosshair_width(self, width):
        self.send(
          {"type": "api", "func": "setCrosshairWidth", "args": [width]}
        )
