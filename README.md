
# ipyniivue
show a nifti image in a webgl 2.0 canvas within a jupyter notebook cell

![example](docs/example.png)
[Niivue](https://github.com/niivue/niivue) in Jupyter

## Installation
```sh
git clone https://github.com/niivue/ipyniivue
cd ipyniivue
yarn
yarn run build
pip install -e .
```
```
jupyter lab
```

## Usage
example usage
```py
from ipyniivue import Niivue

nv = ipyniivue.Niivue()
volumes = [
    {
        'url': 'https://niivue.github.io/niivue/images/mni152.nii.gz',
        'opacity': 1,
        'visible': True,
    }
]
nv.load_volumes(volumes)
nv
```