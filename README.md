
# ipyniivue
show a nifti image in a webgl 2.0 canvas within a jupyter notebook cell

![example](docs/example.png)
[Niivue](https://github.com/niivue/niivue) in Jupyter

## Installation
```sh
git clone https://github.com/niivue/ipyniivue_ts
cd ipyniivue_ts
pip install -e .
jupyter nbextension install --py --symlink --sys-prefix ipyniivue
jupyter nbextension enable --py --sys-prefix ipyniivue
jupyter labextension develop . --overwrite
```
```
jupyter notebook
```
