import importlib.metadata
import pathlib

import anywidget
import traitlets

try:
    __version__ = importlib.metadata.version("ipyniivue_experimental")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


import anywidget 
import pathlib

class AnyNiivue(anywidget.AnyWidget):
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



class AnyNiivueOpacity(anywidget.AnyWidget):
  path_root = pathlib.Path(__file__).parent / "static" 
  _esm = path_root / "widget_traitlet.js"
  opacity = traitlets.Float(1.0).tag(sync=True)
