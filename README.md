# ipyNiiVue
Try out in mybinder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/niivue/ipyniivue/HEAD)       
display and interact with a NIfTI image in a WebGl 2.0 canvas within a Jupyter notebook cell

## Installation
```sh
git clone https://github.com/niivue/ipyniivue
cd ipyniivue
yarn
pip install -e .
yarn run watch
```
Then, in a separate command line
```
jupyter lab
```

To view changes made in the typescript, reload the jupyter page. To view changes made in the python, restart the kernel.

## Usage
example usage
```py
from ipyniivue import Niivue

nv = Niivue()
nv
```
![example](docs/example.png)
