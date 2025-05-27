"""
Widgets representing NiiVue model instances as well as volume, mesh, and drawing models.

Aside from setting up the Mesh, Volume, Drawing, and NiiVue widgets, this module
contains many of the classes needed to make NiiVue instances work, such as classes
to load objects in, change attributes of this instance, and more.
"""

import pathlib
import uuid

import anywidget
import ipywidgets
import traitlets as t
from ipywidgets import CallbackDispatcher

from .constants import _SNAKE_TO_CAMEL_OVERRIDES
from .options_mixin import OptionsMixin
from .utils import (
    file_serializer,
    mesh_layers_serializer,
    serialize_options,
    snake_to_camel,
)

__all__ = ["NiiVue"]


class Mesh(ipywidgets.Widget):
    """
    Represents a Mesh model.

    Parameters
    ----------
    ipywidgets.Widget : A widget representing a mesh model and its data.
    """

    path = t.Union([t.Instance(pathlib.Path), t.Unicode()]).tag(
        sync=True, to_json=file_serializer
    )
    id = t.Unicode(default_value="").tag(sync=True)
    name = t.Unicode(default_value="").tag(sync=True)
    rgba255 = t.List([0, 0, 0, 0]).tag(sync=True)
    opacity = t.Float(1.0).tag(sync=True)
    visible = t.Bool(True).tag(sync=True)
    layers = t.List([]).tag(sync=True, to_json=mesh_layers_serializer)

    @t.validate("path")
    def _validate_path(self, proposal):
        if (
            "path" in self._trait_values
            and self.path
            and self.path != proposal["value"]
        ):
            raise t.TraitError("Cannot modify path once set.")
        return proposal["value"]

    @t.validate("id")
    def _validate_id(self, proposal):
        if "id" in self._trait_values and self.id and self.id != proposal["value"]:
            raise t.TraitError("Cannot modify id once set.")
        return proposal["value"]


class Volume(ipywidgets.Widget):
    """
    Represents a Volume model.

    Parameters
    ----------
    ipywidgets.Widget : A widget representing a volume model and its data.
    """

    path = t.Union([t.Instance(pathlib.Path), t.Unicode()]).tag(
        sync=True, to_json=file_serializer
    )
    id = t.Unicode(default_value="").tag(sync=True)
    name = t.Unicode(default_value="").tag(sync=True)
    opacity = t.Float(1.0).tag(sync=True)
    colormap = t.Unicode("gray").tag(sync=True)
    colorbar_visible = t.Bool(True).tag(sync=True)
    cal_min = t.Float(None, allow_none=True).tag(sync=True)
    cal_max = t.Float(None, allow_none=True).tag(sync=True)
    frame4D = t.Int(0).tag(sync=True)

    @t.validate("path")
    def _validate_path(self, proposal):
        if (
            "path" in self._trait_values
            and self.path
            and self.path != proposal["value"]
        ):
            raise t.TraitError("Cannot modify path once set.")
        return proposal["value"]

    @t.validate("id")
    def _validate_id(self, proposal):
        if "id" in self._trait_values and self.id and self.id != proposal["value"]:
            raise t.TraitError("Cannot modify id once set.")
        return proposal["value"]


class Drawing(ipywidgets.Widget):
    """
    Represents a Drawing model.

    Parameters
    ----------
    ipywidgets.Widget : A widget representing a drawing model and its data.
    """

    path = t.Union([t.Instance(pathlib.Path), t.Unicode()]).tag(
        sync=True, to_json=file_serializer
    )
    id = t.Unicode(default_value="").tag(sync=True)
    opacity = t.Float(1.0).tag(sync=True)
    colormap = t.List([0, 0, 0, 0]).tag(sync=True)
    colorbar_visible = t.Bool(True).tag(sync=True)

    @t.validate("path")
    def _validate_path(self, proposal):
        if (
            "path" in self._trait_values
            and self.path
            and self.path != proposal["value"]
        ):
            raise t.TraitError("Cannot modify path once set.")
        return proposal["value"]

    @t.validate("id")
    def _validate_id(self, proposal):
        if "id" in self._trait_values and self.id and self.id != proposal["value"]:
            raise t.TraitError("Cannot modify id once set.")
        return proposal["value"]


class NiiVue(OptionsMixin, anywidget.AnyWidget):
    """
    Represents a NiiVue widget instance.

    This class provides a Jupyter widget for visualizing neuroimaging data using
    NiiVue. It inherits from `OptionsMixin` for default options.
    """

    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"

    id = t.Unicode(default_value=str(uuid.uuid4()), read_only=True).tag(sync=True)

    height = t.Int().tag(sync=True)
    _opts = t.Dict({}).tag(sync=True, to_json=serialize_options)
    _volumes = t.List(t.Instance(Volume), default_value=[]).tag(
        sync=True, **ipywidgets.widget_serialization
    )
    _meshes = t.List(t.Instance(Mesh), default_value=[]).tag(
        sync=True, **ipywidgets.widget_serialization
    )

    def __init__(self, height: int = 300, **options):
        """
        Initialize the NiiVue widget.

        Parameters
        ----------
        height : int, optional
            The height of the widget in pixels (default: 300).
        options : dict, optional
            Additional keyword arguments to configure the NiiVue widget.
            See :class:`ipyniivue.options_mixin.OptionsMixin` for all options.
        """
        # convert to JS camelCase options
        _opts = {
            _SNAKE_TO_CAMEL_OVERRIDES.get(k, snake_to_camel(k)): v
            for k, v in options.items()
        }
        super().__init__(height=height, _opts=_opts, _volumes=[], _meshes=[])

        # handle messages coming from frontend
        self._event_handlers = {}
        self.on_msg(self._handle_custom_msg)

    def _register_callback(self, event_name, callback, remove=False):
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = CallbackDispatcher()
        if remove:
            self._event_handlers[event_name].remove(callback)
        else:
            self._event_handlers[event_name].register_callback(callback)

    def _handle_custom_msg(self, content, buffers):
        event = content.get("event", "")
        data = content.get("data", {})

        # handle add_volume and add_mesh events separately
        if event == "add_volume":
            self._add_volume_from_frontend(data)
            return
        elif event == "add_mesh":
            self._add_mesh_from_frontend(data)
            return

        # check if the event has a registered handler
        handler = self._event_handlers.get(event)
        if not handler:
            return

        # handle events that require specific processing
        if event == "azimuth_elevation_change":
            handler(data["azimuth"], data["elevation"])
        elif event == "frame_change":
            idx = self.get_volume_index_by_id(data["id"])
            if idx != -1:
                handler(self._volumes[idx], data["frame_index"])
        elif event in {"image_loaded", "intensity_change"}:
            idx = self.get_volume_index_by_id(data["id"])
            if idx != -1:
                handler(self._volumes[idx])
            else:
                handler(data)
        elif event == "mesh_loaded":
            idx = self.get_mesh_index_by_id(data["id"])
            if idx != -1:
                handler(self._meshes[idx])
            else:
                handler(data)
        elif event == "mesh_added_from_url":
            mesh_options = {"url": data["url"], "headers": data["headers"]}
            handler(mesh_options, data["mesh"])
        elif event == "volume_added_from_url":
            image_options = {"url": data["url"], "headers": data["headers"]}
            handler(image_options, data["volume"])
        else:
            handler(data)

    def _add_volume_from_frontend(self, volume_data):
        index = volume_data.pop("index", None)
        volume = Volume(**volume_data)
        if index is not None and 0 <= index <= len(self._volumes):
            self._volumes = self._volumes[:index] + [volume] + self._volumes[index:]
        else:
            self._volumes = [*self._volumes, volume]

    def _add_mesh_from_frontend(self, mesh_data):
        index = mesh_data.pop("index", None)
        mesh = Mesh(**mesh_data)
        if index is not None and 0 <= index <= len(self._meshes):
            self._meshes = self._meshes[:index] + [mesh] + self._meshes[index:]
        else:
            self._meshes = [*self._meshes, mesh]

    def get_volume_index_by_id(self, volume_id: str) -> int:
        """Return the index of the volume with the given id.

        Parameters
        ----------
        volume_id : str
            The id of the volume.
        """
        for idx, vol in enumerate(self._volumes):
            if vol.id == volume_id:
                return idx
        return -1

    def get_mesh_index_by_id(self, mesh_id: str) -> int:
        """Return the index of the mesh with the given id.

        Parameters
        ----------
        mesh_id : str
            The id of the mesh.
        """
        for idx, mesh in enumerate(self._meshes):
            if mesh.id == mesh_id:
                return idx
        return -1

    def load_volumes(self, volumes: list):
        """
        Load a list of volume objects.

        Parameters
        ----------
        volumes : list
            A list of dictionaries containing the volume information.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv = NiiVue()
            nv.load_volumes([{"path": "mni152.nii.gz"}])

        """
        volumes = [Volume(**item) for item in volumes]
        self._volumes = volumes

    def add_volume(self, volume: dict):
        """
        Add a new volume to the widget.

        Parameters
        ----------
        volume : dict
            A dictionary containing the volume information.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv = NiiVue()
            nv.add_volume({"path": "mni152.nii.gz"})

        """
        self._volumes = [*self._volumes, Volume(**volume)]

    @property
    def volumes(self):
        """
        Returns the list of volumes.

        Returns
        -------
        list
            A list of dictionairies containing the volume information.

        Examples
        --------
        ::

            print(nv.volumes)

        """
        return list(self._volumes)

    def load_drawings(self, drawings: list):
        """
        Load a list of drawings objects.

        Parameters
        ----------
        drawings : list
            A list of dictionaries containing the drawing information.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv = NiiVue()
            nv.load_drawings([{"path": "lesion.nii.gz"}])

        """
        drawings = [Drawing(**item) for item in drawings]
        self._drawings = drawings

    @property
    def drawings(self):
        """
        Returns the list of drawings.

        Returns
        -------
        list
            A list of dictionairies containing the drawing information.

        Examples
        --------
        ::

            print(nv.drawings)

        """
        return list(self._drawings)

    def load_meshes(self, meshes: list):
        """
        Load a list of meshes objects.

        Parameters
        ----------
        meshes : list
            A list of dictionaries containing the mesh information.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv = NiiVue()
            nv.load_meshes([{"path": "BrainMesh_ICBM152.lh.mz3"}])

        """
        meshes = [Mesh(**item) for item in meshes]
        self._meshes = meshes

    def add_mesh(self, mesh: Mesh):
        """
        Add a single mesh to the widget.

        Parameters
        ----------
        mesh : dict
            A dictionary containing the mesh information.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv = NiiVue()
            nv.add_mesh({"path": "BrainMesh_ICBM152.lh.mz3"})

        """
        self._meshes = [*self._meshes, mesh]

    @property
    def meshes(self):
        """
        Returns the list of meshes.

        Returns
        -------
        list
            A list of dictionairies containing the mesh information.

        Examples
        --------
        ::

            print(nv.meshes)

        """
        return list(self._meshes)

    def save_document(self, file_name: str = "document.nvd", compress: bool = True):
        """
        Save the entire scene with settings as a document.

        Parameters
        ----------
        file_name : str
            The file name to save the document as.
        compress : bool
            A value represneing if the file should be compressed.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv.save_document("mydoc.nvd", False)

        """
        self.send({"type": "save_document", "data": [file_name, compress]})

    def save_html(self, file_name: str = "untitled.html", canvas_id: str = "gl1"):
        """
        Save the current instance as an html page.

        Parameters
        ----------
        file_name : str
            The file name to save the page as.
        canvas_id : str
            The id of the canvas that NiiVue will be attached to.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv.save_html("mypage.html")

        """
        self.send({"type": "save_html", "data": [file_name, canvas_id]})

    def save_image(
        self,
        file_name: str = "image.nii.gz",
        save_drawing: bool = True,
        index_volume: int = 0,
    ):
        """
        Save the current image as a nii file.

        Parameters
        ----------
        file_name : str
            The file name to save the image as.
        save_drawing : bool
            A value representing if the drawings should be saved.
        index_volume : int
            The volume layer which should be saved (0 for background)

        Returns
        -------
        None

        Examples
        --------
        ::

            nv.save_image("myimage.nii.gz", True, 2)

        """
        self.send(
            {"type": "save_image", "data": [file_name, save_drawing, index_volume]}
        )

    def save_scene(self, file_name: str = "scene.png"):
        """
        Save the current scene with the provided file name.

        Parameters
        ----------
        file_name : str
            The file name to save the scene as.

        Returns
        -------
        None

        Examples
        --------
        ::

            nv.save_scene("myscene.png")

        """
        self.send({"type": "save_scene", "data": [file_name]})

    """
    Custom event callbacks
    """

    def on_azimuth_elevation_change(self, callback, remove=False):
        """
        Register a callback for the 'azimuth_elevation_change' event.

        Set a callback function to run when the user changes the rotation of the 3D
        rendering.

        Parameters
        ----------
        callback : callable
            A function that takes two arguments:

            - **azimuth** (float): The azimuth angle in degrees.
            - **elevation** (float): The elevation angle in degrees.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(azimuth, elevation):
                with out:
                    print('Azimuth:', azimuth)
                    print('Elevation:', elevation)

            nv.on_azimuth_elevation_change(my_callback)

        """
        self._register_callback("azimuth_elevation_change", callback, remove=remove)

    def on_click_to_segment(self, callback, remove=False):
        """
        Register a callback for the 'click_to_segment' event.

        Set a callback function when ``clickToSegment`` is enabled and the user clicks
        on the image.

        Parameters
        ----------
        callback : callable
            A function that takes one argument—a ``dict`` with the following keys:

            - **mm3** (float): The segmented volume in cubic millimeters.
            - **mL** (float): The segmented volume in milliliters.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(data):
                with out:
                    print('Clicked to segment')
                    print('Volume mm3:', data['mm3'])
                    print('Volume mL:', data['mL'])

            nv.on_click_to_segment(my_callback)

        """
        self._register_callback("click_to_segment", callback, remove=remove)

    def on_clip_plane_change(self, callback, remove=False):
        """
        Register a callback for the 'clip_plane_change' event.

        Set a callback function to run when the user changes the clip plane.

        Parameters
        ----------
        callback : callable
            A function that takes one argument—a list of numbers representing the
            clip plane.
        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(clip_plane):
                with out:
                    print('Clip plane changed:', clip_plane)

            nv.on_clip_plane_change(my_callback)

        """
        self._register_callback("clip_plane_change", callback, remove=remove)

    # todo: make volumes be a list of Volumes and meshes be a list of Meshes
    def on_document_loaded(self, callback, remove=False):
        """
        Register a callback for the 'document_loaded' event.

        Set a callback function to run when the user loads a new NiiVue document.

        Parameters
        ----------
        callback : callable
            A function that takes one argument—a ``dict`` representing the loaded
            document with the following keys:

            - **title** (str): The title of the loaded document.
            - **opts** (dict): Options associated with the document.
            - **volumes** (list of str): A list of volume IDs loaded in the document.
            - **meshes** (list of str): A list of mesh IDs loaded in the document.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(document):
                with out:
                    print('Document loaded:')
                    print('Title:', document['title'])
                    print('Options:', document['opts'])
                    print('Volumes:', document['volumes'])
                    print('Meshes:', document['meshes'])

            nv.on_document_loaded(my_callback)

        """
        self._register_callback("document_loaded", callback, remove=remove)

    def on_image_loaded(self, callback, remove=False):
        """
        Register a callback for the 'image_loaded' event.

        Set a callback function to run when a new volume is loaded.

        Parameters
        ----------
        callback : callable
            A function that takes one argument—a ``Volume`` object.
        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(volume):
                with out:
                    print('Image loaded:', volume.id)

            nv.on_image_loaded(my_callback)

        """
        self._register_callback("image_loaded", callback, remove=remove)

    def on_drag_release(self, callback, remove=False):
        """
        Register a callback for the 'drag_release' event.

        Set a callback function to run when the right mouse button is released
        after dragging.

        Parameters
        ----------
        callback : callable
            A function that takes one argument—a ``dict`` containing drag release
            parameters with the following keys:

            - **frac_start** (list of float): Starting fractional coordinates
                ``[X, Y, Z]`` before the drag.
            - **frac_end** (list of float): Ending fractional coordinates
                ``[X, Y, Z]`` after the drag.
            - **vox_start** (list of float): Starting voxel coordinates ``[X, Y, Z]``
                before the drag.
            - **vox_end** (list of float): Ending voxel coordinates ``[X, Y, Z]``
                after the drag.
            - **mm_start** (list of float): Starting coordinates in millimeters
                ``[X, Y, Z]`` before the drag.
            - **mm_end** (list of float): Ending coordinates in millimeters
                ``[X, Y, Z]`` after the drag.
            - **mm_length** (float): Length of the drag in millimeters.
            - **tile_idx** (int): Index of the image tile where the drag occurred.
            - **ax_cor_sag** (int): View index (axial=0, coronal=1, sagittal=2) where
                the drag occurred.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(params):
                with out:
                    print('Drag release event:', params)

            nv.on_drag_release(my_callback)

        """
        self._register_callback("drag_release", callback, remove=remove)

    def on_frame_change(self, callback, remove=False):
        """
        Register a callback for the 'frame_change' event.

        Set a callback function to run whenever the current frame (timepoint) of a
        4D image volume changes.

        Parameters
        ----------
        callback : callable
            A function that takes two arguments:

            - **volume** (``Volume``): The image volume object that has changed frame.
            - **frame_index** (int): The index of the new frame.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(volume, frame_index):
                with out:
                    print('Frame changed')
                    print('Volume:', volume)
                    print('Frame index:', frame_index)

            nv.on_frame_change(my_callback)

        """
        self._register_callback("frame_change", callback, remove=remove)

    def on_intensity_change(self, callback, remove=False):
        """
        Register a callback for the 'intensity_change' event.

        Set a callback function to run when the user changes the intensity range
        with the selection-box action (right click).

        Parameters
        ----------
        callback : callable
            A function that takes one argument—a ``Volume`` object.
        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(volume):
                with out:
                    print('Intensity changed for volume:', volume)

            nv.on_intensity_change(my_callback)

        """
        self._register_callback("intensity_change", callback, remove=remove)

    # todo: maybe create NiiVueLocation and NiiVueLocationValue classes?
    def on_location_change(self, callback, remove=False):
        """
        Register a callback for the 'location_change' event.

        Set a callback function to run when the crosshair location changes.

        Parameters
        ----------
        callback : callable
            A function that takes one argument—a ``dict`` containing the new
            location data—with the following keys:

            - **ax_cor_sag** (int): The view index where the location changed.
            - **frac** (list of float): The fractional coordinates ``[X, Y, Z]``
                in the volume.
            - **mm** (list of float): The coordinates ``[X, Y, Z]`` in millimeters.
            - **vox** (list of int): The voxel coordinates ``[X, Y, Z]``.
            - **values** (list of float): Intensity values at the current location
                for each volume.
            - **string** (str): Formatted string representing the location and
                intensity values.
            - **xy** (list of float): The canvas coordinates ``[X, Y]``.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(location):
                with out:
                    print('Location changed', location)

            nv.on_location_change(my_callback)

        """
        self._register_callback("location_change", callback, remove=remove)

    def on_mesh_added_from_url(self, callback, remove=False):
        """
        Register a callback for the 'mesh_added_from_url' event.

        Set a callback function to run when a mesh is added from a URL.

        **Note:** This is called before the ``mesh_loaded`` event is emitted, so
        the mesh object will **not** be available in the callback.

        Parameters
        ----------
        callback : callable
            A function that takes two arguments:

            - **mesh_options** (dict): Dictionary containing:
                - **url** (str): The URL from which the mesh was loaded.
                - **headers** (dict): HTTP headers used when loading the mesh.

            - **mesh** (dict): Dictionary containing:
                - **id** (str): The ID of the mesh.
                - **name** (str): The name of the mesh.
                - **rgba255** (list of int): RGBA color values (0-255) of the mesh.
                - **opacity** (float): The opacity of the mesh.
                - **visible** (bool): Whether the mesh is visible.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(mesh_options, mesh):
                with out:
                    print('Mesh added from URL')
                    print('URL:', mesh_options['url'])
                    print('Headers:', mesh_options['headers'])
                    print('Mesh ID:', mesh['id'])

            nv.on_mesh_added_from_url(my_callback)

        """
        self._register_callback("mesh_added_from_url", callback, remove=remove)

    def on_mesh_loaded(self, callback, remove=False):
        """
        Register a callback for the 'mesh_loaded' event.

        Set a callback function to run when a new mesh is loaded.

        Parameters
        ----------
        callback : callable
            A function that takes one argument—the loaded mesh (``Mesh`` object).
        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(mesh):
                with out:
                    print('Mesh loaded', mesh)

            nv.on_mesh_loaded(my_callback)

        """
        self._register_callback("mesh_loaded", callback, remove=remove)

    def on_mouse_up(self, callback, remove=False):
        """
        Register a callback for the 'mouse_up' event.

        Set a callback function to run when the left mouse button is released.

        Parameters
        ----------
        callback : callable
            A function that takes one argument—a ``dict`` containing mouse event data
            with the following keys:

            - **is_dragging** (bool): Indicates if a drag action is in progress
                (``True``) or not (``False``).
            - **mouse_pos** (tuple of int): The ``(x, y)`` pixel coordinates of the
                mouse on the canvas when the button was released.
            - **frac_pos** (tuple of float): The fractional position ``(X, Y, Z)``
                within the volume, with each coordinate ranging from ``0.0`` to ``1.0``.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(data):
                with out:
                    print('Mouse button released', data)

            nv.on_mouse_up(my_callback)

        """
        self._register_callback("mouse_up", callback, remove=remove)

    def on_volume_added_from_url(self, callback, remove=False):
        """
        Register a callback for the 'volume_added_from_url' event.

        Set a callback function to run when a volume is added from a URL.

        **Note:** This is called before the ``image_loaded`` event is emitted, so
        the volume object will **not** be available in the callback.

        Parameters
        ----------
        callback : callable
            A function that takes two arguments:

            - **image_options** (dict): Dictionary containing:

                - **url** (str): The URL from which the volume was loaded.
                - **url_image_data** (str): The URL to the image data associated with
                    the volume (if separate from header).
                - **headers** (dict): HTTP headers used when loading the volume.
                - **name** (str): A name for this image (default is an empty string).
                - **colormap** (str): A colormap to use (default is 'gray').
                - **opacity** (float): The opacity for this image (default is 1).
                - **cal_min** (float): Minimum intensity for color brightness/contrast.
                - **cal_max** (float): Maximum intensity for color brightness/contrast.
                - **trust_cal_min_max** (bool): Whether to trust `cal_min` and `cal_max`
                    from the NIfTI header (default is True).
                - **percentile_frac** (float): The percentile to use for setting the
                    robust range of the display values (default is 0.02).
                - **use_qform_not_sform** (bool): Whether to use QForm instead of SForm
                    during construction (default is False).
                - **alpha_threshold** (bool): Whether to use alpha thresholding
                    (default is False).
                - **colormap_negative** (str): Colormap for negative values.
                - **cal_min_neg** (float): Minimum intensity for negative color
                    brightness/contrast.
                - **cal_max_neg** (float): Maximum intensity for negative color
                    brightness/contrast.
                - **colorbar_visible** (bool): Visibility of the colorbar
                    (default is True).
                - **ignore_zero_voxels** (bool): Whether to ignore zero voxels when
                    setting the display range (default is False).
                - **image_type** (int): The image type (default is 0).
                - **frame4D** (int): Frame number for 4D images (default is 0).
                - **colormap_label** (str or None): Label for the colormap.
                - **limit_frames4D** (int): Limit the number of frames for 4D images.
                - **is_manifest** (bool): Whether the image is loaded from a manifest
                    (default is False).

            - **volume** (dict): Dictionary containing:

                - **id** (str): The ID of the volume.
                - **name** (str): The name of the volume.
                - **colormap** (str): The colormap used for the volume.
                - **opacity** (float): The opacity of the volume.
                - **colorbar_visible** (bool): Visibility of the colorbar.
                - **cal_min** (float or None): Minimum calibration value.
                - **cal_max** (float or None): Maximum calibration value.

        remove : bool, optional
            If ``True``, remove the callback. Defaults to ``False``.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display
            out = Output()
            display(out)

            def my_callback(image_options, volume):
                with out:
                    print('Volume added from URL')
                    print('URL:', image_options['url'])
                    print('Headers:', image_options['headers'])
                    print('Volume ID:', volume['id'])

            nv.on_volume_added_from_url(my_callback)

        """
        self._register_callback("volume_added_from_url", callback, remove=remove)

    def on_volume_updated(self, callback, remove=False):
        """
        Register a callback for the 'volume_updated' event.

        Sets a callback function to run when `updateGLVolume` is called.
        Most users will not need to use this directly.

        Parameters
        ----------
        callback : callable
            A function that takes no arguments.
        remove : bool, optional
            If True, remove the callback. Defaults to False.

        Examples
        --------
        ::

            from ipywidgets import Output
            from IPython.display import display

            out = Output()
            display(out)

            def my_callback():
                with out:
                    print('Volumes updated')

            nv.on_volume_updated(my_callback)

        """
        self._register_callback("volume_updated", callback, remove=remove)


class WidgetObserver:
    """Creates an observer on the `attribute` of `object` for a `widget`."""

    def __init__(self, widget, obj, attribute):
        self.widget = widget
        self.object = obj
        self.attribute = attribute
        self._observe()

    def _widget_change(self, change):
        # Converts string to float because negative 0 as a float
        # with ipywidgets does not work as expected.
        setattr(self.object, self.attribute, float(change["new"]))

    def _observe(self):
        self.widget.observe(self._widget_change, names=["value"])
