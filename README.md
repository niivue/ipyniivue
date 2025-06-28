# ipyniivue

[![PyPI Version](https://badge.fury.io/py/ipyniivue.svg)](https://badge.fury.io/py/ipyniivue)
[![License](https://img.shields.io/github/license/niivue/ipyniivue)](https://opensource.org/license/bsd-2-clause)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/niivue/ipyniivue/main?urlpath=lab%2Ftree%2Fexamples)

**A Jupyter Widget for [Niivue](https://github.com/niivue/niivue) based on [anywidget](https://github.com/manzt/anywidget).**

---


## Installation

Install ipyniivue using `pip`:

```sh
pip install ipyniivue
```

---

## Usage

In a Jupyter environment:

```python
from ipyniivue import NiiVue

nv = NiiVue()
nv.load_volumes([{"path": "images/mni152.nii.gz"}])
nv
```

This will render an interactive Niivue widget within your notebook.

**See the [basic demo](./examples/basic_multiplanar.ipynb) to learn more.**

---

## Documentation

See the [Documentation](https://niivue.github.io/ipyniivue) for usage.


---

## Development

ipyniivue uses the recommended [`hatchling`](https://packaging.python.org/en/latest/flow/#using-hatch) build system, which is convenient to use via the [`hatch` CLI](https://hatch.pypa.io/latest/). We recommend installing `hatch` globally (e.g., via `pipx`) and running the various commands defined within `pyproject.toml`. `hatch` will take care of creating and synchronizing a virtual environment with all dependencies defined in `pyproject.toml`.

### Command Cheat Sheet

Run these commands from the root of the project:

| Command                | Description                                                          |
|------------------------|----------------------------------------------------------------------|
| `hatch run format`     | Format the project with `ruff format .` and apply linting with `ruff --fix .` |
| `hatch run lint`       | Lint the project with `ruff check .`                                 |
| `hatch run test`       | Run unit tests with `pytest`                                         |
| `hatch run docs`       | Build docs with `Sphinx`                                             |

Alternatively, you can manually create a virtual environment and manage installation and dependencies with `pip`:

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Making Changes to the JavaScript Code

This is an [anywidget](https://github.com/manzt/anywidget) project, meaning the codebase is a hybrid of Python and JavaScript. The JavaScript code resides under the `js/` directory and uses [esbuild](https://esbuild.github.io/) for bundling. Whenever you make changes to the JavaScript code, you need to rebuild the files under `src/ipyniivue/static`.

You have two options:

1. **Build Once**: Build the JavaScript code one time:

    ```sh
    npm run build
    ```

2. **Start Development Server**: Start a development server that automatically rebuilds the code as you make changes:

    ```sh
    npm run dev
    ```

    We recommend this approach for a smoother development experience.

**Working with Jupyter**

Once the development server is running, you can start JupyterLab or Visual Studio Code to develop the widget. When you're finished, stop the development server with `Ctrl+C`.

> **Note:** To have `anywidget` automatically apply changes as you work, set the environment variable `ANYWIDGET_HMR=1`. You can set this directly in a notebook cell:
>
> ```python
> %env ANYWIDGET_HMR=1
> ```
> or in the shell:
> ```sh
> export ANYWIDGET_HMR=1
> ```

---

## Release Process

Releases are automated using GitHub Actions via the [`release.yml`](.github/workflows/release.yml) workflow.

### Steps to Create a New Release

1. **Commit Changes**: Ensure all your changes are committed.

2. **Create a Tag**: Create a new tag matching the pattern `v*`:

    ```sh
    git tag -a vX.X.X -m "vX.X.X"
    git push --follow-tags
    ```

3. **Workflow Actions**: When triggered, the workflow will:

   - Publish the package to PyPI with the tag version.
   - Generate a changelog based on conventional commits.
   - Create a GitHub Release with the changelog.

### Changelog Generation

- We generate a changelog for GitHub releases with [`antfu/changelogithub`](https://github.com/antfu/changelogithub).
- Each changelog entry is grouped and rendered based on conventional commits.
- It's recommended to follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary) specification.
