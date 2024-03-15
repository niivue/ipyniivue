# ipyniivue_experimental

A Jupyter Widget for [Niivue](https://github.com/niivue/niivue) based on
anywidget.

# Installation

```sh
pip install ipyniivue_experimental
```

# Usage

In a Jupyter environment:

```py
from ipyniivue_experimental import AnyNiivue

nv = AnyNiivue()
nv.load_volumes([{"path": "images/mni152.nii.gz"}])
nv
```

See the [basic demo](./demo/basic_multiplanar.ipynb) to learn more.

# Development

This is an [anywidget](https://github.com/manzt/anywidget) project. To get
started create a virtual Python environment and install the necessary
development dependencies.

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]" 
```

Then, install JS dependencies with `npm` and run the dev server.

```sh
npm install
npm run dev
```

You can now start VS Code or JupyterLab to develop the widget. When finished,
stop the JS development server.

> NOTE: In order to have anywidget automatically apply changes as you work,
> make sure to `export ANYWIDGET_HMR=1` environment variable.

# Changelog:

## v0.0.7

Change to traitlet approach

## v0.0.5 

Adding functions 
load_volumes, load_meshes, set_opacity, set_crosshair_width and set_crosshair_color.

## v0.0.4

Setting up the project
