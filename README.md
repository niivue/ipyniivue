# ipyniivue_experimental


```sh
python3.11 -m venv .venv && source .venv/bin/activate
pip install ipyniivue_experimental
pip install jupyterlab
```

# Example

```
from ipyniivue_experimental import AnyNiivue

nv = AnyNiivue()
nv
```


```
# second cell, wait for one second till the frontend code from cell1 is done loading.
my_volumes = [
           { "url": "https://niivue.github.io/niivue/images/mni152.nii.gz" }
        ]
nv.load_volumes(my_volumes)
```


# How this project was made:

This project was made with 


1.
```
npm create anywidget@latest
```
2.


create-anywidget version 0.4.5

┌  Welcome to anywidget!
│
◇  Where should we create your project?
│  .
│
◇  Directory not empty. Continue?
│  Yes
│
◇  Which framework?
│  Vanilla
│
◇  Which variant?
│  JavaScript
│
└  Your project is ready!


3

```
npm install
```

4
```
npm i @niivue/niivue
```

python3.11 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]" 
```

```
npm run dev
```


# Changelog:

## v0.0.5 

Adding functions 
load_volumes, load_meshes, set_opacity, set_crosshair_width and set_crosshair_color.



## v0.0.4

Setting up the project