
# ipyNiiVue

[![Build Status](https://travis-ci.org/niivue/ipyniivue.svg?branch=master)](https://travis-ci.org/niivue/ipyniivue)
[![codecov](https://codecov.io/gh/niivue/ipyniivue/branch/master/graph/badge.svg)](https://codecov.io/gh/niivue/ipyniivue)


ipyNiiVue is a Python / [Niivue](https://github.com/niivue/niivue) bridge for [Jupyter Widgets](https://jupyter.org/widgets). A Python API is used to interact with NiiVue.

## Getting started

### Installation
```sh
git clone --recurse-submodules -j8 git://github.com/niivue/ipyniivue.git
cd ipyniivue
yarn
yarn run watch
```
Then, in a separate command line
```
jupyter lab
```

To view changes made in the typescript, reload the jupyter page. To view changes made in the python, restart the kernel.

### Usage
![example](docs/example.gif)


