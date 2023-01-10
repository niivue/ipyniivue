
# ipyniivue

[![Build Status](https://travis-ci.org/niivue/ipyniivue.svg?branch=master)](https://travis-ci.org/niivue/ipyniivue)
[![codecov](https://codecov.io/gh/niivue/ipyniivue/branch/master/graph/badge.svg)](https://codecov.io/gh/niivue/ipyniivue)


NiiVue Jupyter Library

## Installation
```sh
git clone https://github.com/niivue/ipyniivue
cd ipyniivue
npm i anthonyandroulakis/niivue#thresholding
yarn
yarn run watch
```
Then, in a separate command line
```
jupyter lab
```

The `npm i anthonyandroulakis/niivue#thresholding` step is temporary and will only exist until the thresholding branch of niivue gets published onto npmjs.org       
      
To view changes made in the typescript, reload the jupyter page. To view changes made in the python, restart the kernel.

## Usage
example usage
```py
from ipyniivue import Niivue

nv = Niivue()
nv
```
![example](docs/example.png)


