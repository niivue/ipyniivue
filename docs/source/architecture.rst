Architecture
============

IpyNiiVue is a Jupyter Widget for Niivue based on anywidget. This document details the internal structure, frontend-backend synchronization patterns, and communication protocols in IPyNiiVue.

System Overview
---------------

* **Python Side**: Users interact with the ``NiiVue`` class to load and manipulate neuroimaging data.
* **JavaScript Side**: Handles WebGL rendering and user interactions in the browser.
* **Communication Layer**: Traitlets synchronize state between Python and JavaScript via WebSocket (ex: JupyterLab) or HTTP (ex: Marimo).

Architecture Layers
-------------------

1. Python Backend (Kernel)
^^^^^^^^^^^^^^^^^^^^^^^^^^

Runs in the notebook kernel process and contains:

* ``NiiVue``, ``Volume``, ``Mesh``, and ``MeshLayer`` classes.
* State management through traitlets.
* Data processing and computational logic.
* Chunked data handling for large data from the frontend (to overcome Tornado's 10MB limit).

2. Communication Layer
^^^^^^^^^^^^^^^^^^^^^^

Provided by the `anywidget <https://github.com/manzt/anywidget>`_ framework:

* Maintains synchronized widget models between kernel and browser.
* Handles state synchronization via traitlets.
* Manages WebSocket/HTTP communication.
* Serializes/deserializes data between Python and JavaScript.

3. JavaScript Frontend (Browser)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Runs in the browser and includes:

* WebGL rendering via the `NiiVue <https://github.com/niivue/niivue>`_ library.
* UI event handling (mouse, keyboard interactions).
* Visual output in notebook cells.

High-Level Data Flow
--------------------

.. mermaid::

   flowchart LR
       subgraph "Kernel"
           A[Python Backend<br/>NiiVue class]
       end
       
       subgraph "Communication Layer"
           B[Widget Bridge<br/>Traitlets sync<br/>WebSocket/HTTP]
       end
       
       subgraph "Browser"
           C[JavaScript Frontend<br/>WebGL rendering<br/>User interactions]
           D[Notebook Output Cell<br/>Visual display]
       end
       
       A <--> B
       B <--> C
       C <--> D

----

Implementation Details
----------------------

The following sections detail the specific class structures, binary optimization strategies, and synchronization logic used to implement the architecture described above.

1. Class Hierarchy
^^^^^^^^^^^^^^^^^^

The project extends ``anywidget`` to bridge Python and JavaScript. The hierarchy isolates binary handling logic in a base class, separating it from specific widget implementations.

.. code-block:: text

    anywidget.AnyWidget
    └── BaseAnyWidget (src/ipyniivue/widget.py)
        ├── NiiVue
        ├── Volume
        ├── Mesh
        └── MeshLayer

    traitlets.HasTraits
    ├── ConfigOptions (src/ipyniivue/config_options.py)
    ├── Scene (src/ipyniivue/traits.py)
    ├── Graph (src/ipyniivue/traits.py)
    ├── ColorMap (src/ipyniivue/traits.py)
    ├── LUT (src/ipyniivue/traits.py)
    └── NIFTI1Hdr (src/ipyniivue/traits.py)

2. BaseAnyWidget
^^^^^^^^^^^^^^^^

Located in ``src/ipyniivue/widget.py``, ``BaseAnyWidget`` overrides some methods in AnyWidget and defines new methods and attributes used in data transfers.

.. list-table::
   :widths: 25 15 60
   :header-rows: 1

   * - Method / Attribute
     - Purpose
     - Description
   * - ``set_state(self, state)``
     - **Override**
     - Intercepts state keys starting with ``chunk_``. Uses ``ChunkedDataHandler`` to reassemble binary data (sent from frontend JS) into numpy arrays before setting the actual widget trait.
   * - ``_get_binary_traits(self)``
     - **Hook**
     - Subclasses must override this to list synced binary traits (e.g., ``["img"]`` for ``Volume``, ``["pts", "tris"]`` for ``Mesh``).
   * - ``_binary_trait_to_js_names``
     - **Mapping**
     - Subclasses can override this to map Python trait names to JS property names for binary attributes (e.g., ``draw_bitmap`` -> ``drawBitmap``). Only needed IF the JS name differs from the Python name.
   * - ``_handle_binary_trait_change``
     - **Observer**
     - Automatically attached to traits in ``_get_binary_traits``. Calculates the difference between old and new arrays. Sends a ``buffer_update`` message containing only changed indices and values, or a ``buffer_change`` if the data type differs.

3. Binary Data Transfer Protocol
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Logic in ``js/lib.ts`` and ``src/ipyniivue/utils.py`` handles binary payloads that exceed standard limits (> 10MB).

* **Chunking:** ``lib.sendChunkedData`` (JS) splits buffers into 5MB chunks. On the Python side, ``set_state`` (via ``ChunkedDataHandler``) reassembles them.
* **Diffing (Py → JS):** ``_handle_binary_trait_change`` sends ``buffer_update`` messages containing ``indices`` and ``values`` arrays if the type is the same (if the type is different, a ``buffer_change`` message is sent with the full data buffer). The frontend ``handleBufferMsg`` utilizes ``applyDifferencesToTypedArray`` to patch the existing buffer rather than reloading it.

4. Frontend/Backend Sync
^^^^^^^^^^^^^^^^^^^^^^^^

The Render Loop
~~~~~~~~~~~~~~~

When the ``volumes`` or ``meshes`` list changes in Python, the frontend executes ``render_volumes`` or ``render_meshes``.

**Logic Flow:**

(``js/volume.ts`` & ``js/mesh.ts``)

1. **Gather Models:** The frontend resolves the list of Model IDs provided by Python into actual ``AnyModel`` objects.

2. **Generate Maps:** Two maps are created: ``backend_map`` (ID → Model) and ``frontend_map`` (ID → NVObject).

3. **Update:**
    * **Create:** If an ID exists in the Backend but not the Frontend → Call ``create_volume``.
    * **Dispose:** If an ID exists in the Frontend but not the Backend → Call ``nv.removeVolume`` and trigger ``disposer.dispose(id)``.
    * **Reorder:** The ``nv.volumes`` array is sorted to match the order of the Python list.

5. Communication Flows
^^^^^^^^^^^^^^^^^^^^^^

The system handles object creation differently depending on where the volume / mesh / mesh layer is added.

**ID Gen:**

* **Backend:** When a volume is created in Python, the ``Volume`` constructor generates a UUID suffixed with ``_py`` to serve as the identifier.
* **Frontend:** When a volume is loaded via the browser (e.g., drag-and-drop), the ID is generated internally by the Niivue JavaScript library.

Flow A: Backend-Initiated Creation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*User adds a volume via Python code (e.g., `nv.add_volume()`).*

.. list-table::
   :widths: 10 20 50 20
   :header-rows: 1

   * - Step
     - Layer
     - Action
     - Source Ref
   * - 1
     - **Python**
     - User calls ``nv.add_volume()``. A new ``Volume`` widget is instantiated. The Python constructor generates a UUID suffixed with ``_py``.
     - ``src/ipyniivue/widget.py``
   * - 2
     - **Bridge**
     - ``anywidget`` syncs the updated list of Model IDs to the browser.
     - N/A
   * - 3
     - **JS**
     - ``model.on("change:volumes")`` triggers ``render_volumes``.
     - ``js/widget.ts``
   * - 4
     - **JS**
     - ``render_volumes`` detects the new ID, calls ``create_volume``, and loads the data (via URL or buffer) into WebGL.
     - ``js/volume.ts``
   * - 5
     - **JS**
     - Listeners are attached to the new volume's properties (opacity, colormap) to handle future updates.
     - ``js/volume.ts``

Flow B: Frontend-Initiated Creation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*User drags a file directly onto the canvas in the browser.*

.. list-table::
   :widths: 10 20 50 20
   :header-rows: 1

   * - Step
     - Layer
     - Action
     - Source Ref
   * - 1
     - **JS**
     - ``Niivue`` loads the file and generates its own ID. ``nv.onImageLoaded`` is triggered.
     - ``js/widget.ts``
   * - 2
     - **JS**
     - ``attachNiivueEventHandlers`` checks if the volume ID already exists in the backend list.
     - ``js/widget.ts``
   * - 3
     - **JS**
     - If new, ``pendingVolumeIds`` tracks the ID to prevent duplicate rendering. A Custom Message (``add_volume``) is sent to Python containing metadata (name, colormap, etc.).
     - ``js/widget.ts``
   * - 4
     - **Bridge**
     - Message travels over Bridge to Kernel.
     - N/A
   * - 5
     - **Python**
     - ``_handle_custom_msg`` receives ``add_volume``. Calls ``_add_volume_from_frontend``.
     - ``src/ipyniivue/widget.py``
   * - 6
     - **Python**
     - A new ``Volume`` instance is created using the ID provided by the frontend and appended to ``self.volumes``. This triggers a traitlet update.
     - ``src/ipyniivue/widget.py``
   * - 7
     - **JS**
     - ``model.on("change:volumes")`` triggers ``render_volumes`` due to the Python state update.
     - ``js/widget.ts``
   * - 8
     - **JS**
     - ``render_volumes`` detects the ID. Since the ID now exists in the ``frontend_volume_map``, ``nv.addVolume`` is skipped. ``pendingVolumeIds`` is cleared.
     - ``js/volume.ts``

6. Event & Message Routing
^^^^^^^^^^^^^^^^^^^^^^^^^^

Standard attributes sync via Traitlets. Specific actions use custom messages.

Custom Message Protocol (``msg:custom``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Python:**

uses ``_handle_custom_msg``

.. code-block:: python

   # Logic Flow in _handle_custom_msg
   if event == "add_volume":
       _add_volume_from_frontend(data)
   elif event == "hover_idx_change":
       callback(data) # Triggers user-defined Python callbacks
   elif event == "image_loaded":
       # Waits for traits (img, hdr) to be fully synced before firing callback
       handler(volume)

**JS:**

uses ``model.on("msg:custom")``

Some example use-cases:

.. list-table::
   :widths: 30 30 40
   :header-rows: 1

   * - Message Type
     - Action
     - Data Payload
   * - ``save_scene``
     - Calls ``nv.saveScene()``
     - Filename string
   * - ``set_gamma``
     - Updates gamma levels
     - Float value
   * - ``draw_otsu``
     - Runs segmentation
     - Integer levels
   * - ``load_drawing_from_url``
     - Loads binary drawing
     - URL string or Binary Buffer

Nested State Synchronization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nested objects do not automatically trigger Traitlet updates when their internal keys change.

To address this limitation while keeping the ipyniivue API intuitive, ipyniivue implements a propagation mechanism that forwards updates to the parent class.

For example, executing ``nv.scene.gamma = 1`` triggers the internal observer ``_propagate_parent_change`` within the ``Scene`` class. This observer invokes ``_notify_scene_changed`` on the parent ``NiiVue`` instance, ensuring the update is properly serialized and synchronized with the frontend.

----

Appendix: File Organization
---------------------------

Python Components (src/ipyniivue/)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``__init__.py``: Package initialization and exports
* ``widget.py``: Core ``NiiVue``, ``Volume``, ``Mesh`` classes
* ``traits.py``: Custom traitlet classes (``Scene``, ``Graph``, ``ColorMap``)
* ``serializers.py``: Custom serializers and deserializers for complex types and Enums
* ``config_options.py``: Auto-generated mappings for NiiVue configuration options
* ``constants.py``: Enumerations for slice types, drag modes, render settings
* ``utils.py``: General utilities
* ``download_dataset.py``: Utility for fetching data

JavaScript Bundle (js/)
^^^^^^^^^^^^^^^^^^^^^^^

* ``widget.ts``: Main entry point
* ``volume.ts``: Volume handling
* ``mesh.ts``: Mesh and MeshLayer handling
* ``lib.ts``: General utilities
* ``types.ts`` / ``types/*.d.ts``: Type declarations for models, messages, and external dependencies.

Scripts (scripts/)
^^^^^^^^^^^^^^^^^^

* ``generate_options_mixin.py``: For automatically generating code in ``src/ipyniivue/config_options.py``. Modify this file and run ``python scripts/generate_options_mixin.py`` from the root directory instead of modifying ``src/ipyniivue/config_options.py`` directly.

Documentation & Tests
^^^^^^^^^^^^^^^^^^^^^

* ``docs/``: Sphinx documentation source (``.rst``), configuration (``conf.py``), and build scripts (``Makefile``, ``make.bat``).
* ``tests/``: Pytest unit tests.