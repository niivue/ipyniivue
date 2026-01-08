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

### Getting Started

These steps set up a **local development environment** for `ipyniivue` with live JavaScript rebuilding via `anywidget`.

#### Prerequisites
- Python 3.10+
- Node.js (LTS recommended)
- `hatch` installed (e.g. via `pipx install hatch`)
- Ensure **`ipyniivue` is *not* already installed** in your Python environment

---

#### Step-by-step setup

##### 0. Verify your Python environment
Make sure `hatch` is available and `ipyniivue` is not installed:

```bash
hatch --version
pip show ipyniivue || echo "ipyniivue not installed (good)"
```

---

##### 1. Clone the repository
```bash
git clone https://github.com/niivue/ipyniivue.git
```

---

##### 2. Enter the repository
```bash
cd ipyniivue
```

---

##### 3. Install JavaScript dependencies
From the repository root:

```bash
npm install
```

---

##### 4. Start a Hatch shell (Python environment)
```bash
hatch shell
```

This activates the project’s Python development environment.

---

##### 5. Install Python dependencies (editable mode)
```bash
pip install -e ".[dev]"
```

This activates the project’s Python development environment.

---

##### 6. Start the JavaScript dev server
In the same terminal:

```bash
cd js
npm run dev
```

This runs the JavaScript build in **watch mode**, rebuilding the widget automatically when files change.

> Leave this terminal running.

---

##### 7. Open a new terminal tab
Open a **second terminal tab/window**, again from the `ipyniivue` repository root.

---

##### 8. Start another Hatch shell
```bash
hatch shell
```

---

##### 9. Install `ipyniivue` in editable mode
```bash
pip install -e .
```

This ensures Python picks up the locally built widget assets.

---

##### 10. Launch JupyterLab
```bash
jupyter lab
```

You can now open an example notebook and develop `ipyniivue` with live JavaScript updates.

---

#### Development tips
- For best results with live updates, set:
  ```bash
  export ANYWIDGET_HMR=1
  ```
  before launching JupyterLab.
- If the widget does not appear or fails to load, ensure:
  - `npm run dev` is still running
  - `pip install -e .` was run **after** starting the JS build
- If you switch branches or pull updates that change JS files, restart `npm run dev`.


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

## Generating the Notebook Gallery

ipyniivue includes tooling to generate a **static HTML gallery** from example notebooks.

Each notebook is:

1. Executed in isolation
2. Converted to static HTML
3. Snapshotted using the final rendered canvas
4. Added to a gallery page with thumbnails that link to the generated HTML

All generated artifacts live in a **test-only output directory** and are **never committed**.

### Gallery output location

```
tests-out/
  html/          # generated static HTML per notebook
  gallery/
    thumbnails/  # canvas thumbnails
    index.html   # gallery page
```

The entire `tests-out/` directory is gitignored and safe to delete at any time.

---

### Generate the gallery

```bash
npm run gallery
```

This will:
- Execute notebooks found in `examples/`
- Generate static HTML into `tests-out/html/`
- Create thumbnails from the final rendered canvas
- Generate `tests-out/gallery/index.html`

You can open the gallery locally:

```bash
open tests-out/gallery/index.html
```

---

### Clean generated gallery artifacts

To remove all generated HTML, thumbnails, and executed notebooks:

```bash
npm run clean:generated-html
```

To preview what would be removed:

```bash
npm run clean:generated-html:dry
```

---

## End-to-End (E2E) Testing with Playwright

ipyniivue uses **Playwright** to run end-to-end tests against **pre-executed static HTML**, rather than interacting with live Jupyter notebooks.

This approach provides:
- Deterministic results
- No UI flakiness
- No dependency on JupyterLab state
- True visual regression testing for WebGL output

---

### E2E testing workflow

The E2E pipeline consists of two steps:

1. **Prepare static HTML**
2. **Run Playwright tests**

```bash
npm run test:e2e
```

This runs:

```
scripts/prepare-e2e.cjs   # executes notebooks → static HTML in tests-out/
playwright test           # loads static HTML and runs assertions
```

---

### What is tested?

For each notebook:

- The static HTML loads successfully
- A `<canvas>` element is rendered
- A WebGL context is available
- The rendered canvas matches a **saved visual snapshot**

Snapshots are stored under:

```
e2e-tests/__screenshots__/
```

These snapshot images **should be committed**, as they define the visual baseline.

---

### Updating visual snapshots

When a visualization changes intentionally:

```bash
npx playwright test --update-snapshots
```

This regenerates the baseline screenshots.

---

### Generated test artifacts

All generated HTML and intermediate files are written to:

```
tests-out/
```

This directory is:
- Automatically reused between runs
- Cleaned via `npm run clean:generated-html`
- Ignored by git

---

### Why static HTML testing?

We intentionally avoid driving the JupyterLab UI in tests.

Static HTML testing provides:
- Stable WebGL output
- Faster CI
- Clear visual diffs
- No notebook state pollution
- No source-control churn

This is the recommended approach for testing interactive notebook-based visualization libraries.
