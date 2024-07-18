# ipyniivue

A Jupyter Widget for [Niivue](https://github.com/niivue/niivue) based on
anywidget.

# Installation

```sh
pip install ipyniivue
```

## Usage

In a Jupyter environment:

```py
from ipyniivue import NiiVue

nv = NiiVue()
nv.load_volumes([{"path": "images/mni152.nii.gz"}])
nv
```

See the [basic demo](./examples/basic_multiplanar.ipynb) to learn more.

## Development

**ipyniivue** uses [the
recommended](https://packaging.python.org/en/latest/flow/#) `hatchling`
build-system, which is convenient to use via the [`hatch`
CLI](https://hatch.pypa.io/latest/). We recommend installing `hatch` globally
(e.g., via `pipx`) and running the various commands defined within
`pyproject.toml`. `hatch` will take care of creating and synchronizing a
virtual environment with all dependencies defined in `pyproject.toml`.

### Commands Cheatsheet

All commands are run from the root of the project, from a terminal:

| Command                | Action                                                                    |
| :--------------------- | :-------------------------------------------------------------------------|
| `hatch run format`     | Format project with `ruff format .` and apply linting with `ruff --fix .` |
| `hatch run lint`       | Lint project with `ruff check .`.                                         |
| `hatch run test`       | Run unit tests with `pytest`                                              |

Alternatively, you can develop **ipyniivue** by manually creating a virtual
environment and managing installation and dependencies with `pip`.

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Making Changes to the JavaScript Code

This is an [anywidget](https://github.com/manzt/anywidget) project, which means
the code base is hybrid Python and JavaScript. The JavaScript part is developed
under `js/` and uses [esbuild](https://esbuild.github.io/) to bundle the code.
Any time you make changes to the JavaScript code, you need to rebuild the files
under `src/ipyniivue/static`. This can be done in two ways:

```sh
npm run build
```

which will build the JavaScript code once, or you can start a development server:

```sh
npm run dev
```

which will start a development server that will automatically rebuild the code
as you make changes. We recommend the latter approach, as it is more convenient.

Once you have the development server running, you can start the JupyterLab
or VS Code to develop the widget. When finished, you can stop the development
server with `Ctrl+C`.

> NOTE: In order to have anywidget automatically apply changes as you work,
> make sure to `export ANYWIDGET_HMR=1` environment variable. This can be set
> directly in a notebook with `%env ANYWIDGET_HMR=1` in a cell.

## Release Process

1. Releases are automated using GitHub Actions and the
   [`release.yml`](.github/workflows/release.yml) workflow.
2. The workflow is triggered when a new tag matching the pattern `v*` is pushed
   to the repository.
3. To create a new release, create a tag from the command line:
    ```sh
    git tag -a vX.X.X -m "vX.X.X"
    git push --follow-tags
    ```
4. When triggered, the workflow will:
  - Publish the package to PyPI with the tag version.
  - Generate a changelog based on conventional commits and create a GitHub
    Release with the changelog.

### Changelog Generation

- We generate a changelog for GitHub releases with
  [`antfu/changelogithub`](https://github.com/antfu/changelogithub)
- Each changelog entry is grouped and rendered based on conventional commits,
  and it is recommended to follow the [Conventional
  Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary).
- The tool generates the changelog based on the commits between the latest
  release tag and the previous release tag.

By following this release process and utilizing conventional commits, you can
ensure consistent and informative releases for your project.
