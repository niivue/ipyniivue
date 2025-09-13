Architecture
============

IPyNiiVue is a widget that bridges WebGL-powered JavaScript visualization (Niivue) with Python in notebooks. This document contains an overview of how JavaScript interacts with Python in this library.

System Overview
---------------

- **Python Side**: Users interact with the ``NiiVue`` class to load and manipulate neuroimaging data
- **JavaScript Side**: Handles WebGL rendering and user interactions in the browser
- **Communication Layer**: Traitlets synchronize state between Python and JavaScript via WebSocket (JupyterLab) or HTTP (Marimo)

Architecture Layers
-------------------

1. Python Backend (Kernel)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Runs in the notebook kernel process and contains:

- ``NiiVue``, ``Volume``, ``Mesh``, and ``MeshLayer`` classes
- State management through traitlets
- Data processing and computational logic
- Chunked data handling for large data from the frontend (to overcome Tornado's 10MB limit)

2. Widget Bridge Layer
~~~~~~~~~~~~~~~~~~~~~~

Provided by anywidget framework:

- Maintains synchronized widget models between kernel and browser
- Handles state synchronization via traitlets
- Manages WebSocket/HTTP communication
- Serializes/deserializes data between Python and JavaScript

3. JavaScript Frontend (Browser)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Runs in the browser and includes:

- WebGL rendering via Niivue.js library
- UI event handling (mouse, keyboard interactions)
- Visual output in notebook cells

Data Flow
---------

1. **State Updates**: Property changes (opacity, colormap, etc.) sync automatically via traitlets
2. **Large Data Transfer**: Volume/mesh data transmitted in chunks to handle size limitations
3. **Efficient Updates**: Only array differences (indices + values) sent for existing data
4. **Event Handling**: User interactions in JS trigger Python callbacks via custom messages

Some Implementation Details
---------------------------

**JavaScript Bundle**:

- Source: ``js/`` directory
- Build: esbuild bundles to ``src/ipyniivue/static/widget.js``
- Main components: ``widget.ts``, ``volume.ts``, ``mesh.ts``, ``lib.ts``

**Python Components**:

- ``widget.py``: Core NiiVue widget and data models
- ``serializers.py``: Data conversion between Python and JavaScript
- ``config_options.py``: Configuration management
- ``traits.py``: Custom trait types for specialized data

**Build System**:

- ``build.js``: Generates colormaps and shader names during build
- ``pyproject.toml``: Python packaging configuration