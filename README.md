
# ipyNiiVue

[![Build Status](https://travis-ci.org/niivue/ipyniivue.svg?branch=master)](https://travis-ci.org/niivue/ipyniivue)
[![codecov](https://codecov.io/gh/niivue/ipyniivue/branch/master/graph/badge.svg)](https://codecov.io/gh/niivue/ipyniivue)


ipyNiiVue is a Python / [Niivue](https://github.com/niivue/niivue) bridge for [Jupyter Widgets](https://jupyter.org/widgets). A Python API is used to interact with NiiVue.

## Getting started

### Installation
```sh
conda create -n ipyniivue-dev -c conda-forge nodejs yarn python jupyterlab
conda activate ipyniivue-dev
git clone --recurse-submodules https://github.com/niivue/ipyniivue.git
cd ipyniivue
yarn
pip install -e .
yarn run build
jupyter lab
```

To view changes made in the typescript, reload the jupyter page. To view changes made in the python, restart the kernel.

### Usage
![example](docs/example.png)


