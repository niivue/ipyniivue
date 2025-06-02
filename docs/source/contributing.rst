Contributing
============

We are glad you are here! Contributions to this package are always welcome.
Read on to learn more about the contribution process and package design.

ipyniivue uses `the recommended <https://pre-commit.com/>`__ hatchling build-system, which is convenient to use via the `hatch CLI <https://hatch.pypa.io/latest/>`__. We recommend installing hatch globally (e.g., via pipx) and running the various commands defined within pyproject.toml. hatch will take care of creating and synchronizing a virtual environment with all dependencies defined in pyproject.toml.

Install Pre-Commit hooks
^^^^^^^^^^^^^^^^^^^^^^^^
We use `pre-commit <https://packaging.python.org/en/latest/flow/#>`__ to run code checks and clear
notebook outputs before committing changes. To install the pre-commit hooks,
run the following command:

.. code-block:: console

   $ pre-commit install

As a result, the hooks will automatically check and fix some issues before
pushing with git. If changes are made after committing with git, you will need
to commit again afterwords. Alternatively, you can just run the following
command beforehand:

.. code-block:: console

    $ nb-clean clean --remove-empty-cells

Command Cheatsheet
^^^^^^^^^^^^^^^^^^
All commands are run from the root of the project, from a terminal:

+--------------------+-----------------------------------+
|       Command      |    Action                         |
+====================+===================================+
| $ hatch run format | Format project with ruff format . |
|                    | and apply linting with ruff --fix |
+--------------------+-----------------------------------+
| $ hatch run lint   | Lint project with ruff check .    |
+--------------------+-----------------------------------+
| $ hatch run test   | Run unit tests with pytest        |
+--------------------+-----------------------------------+
| $ hatch run docs   | Build docs with Sphinx            |
+--------------------+-----------------------------------+

Alternatively, you can develop ipyniivue by manually creating a virtual environment and managing installation and dependencies with pip.

.. code-block:: console

    python3 -m venv .venv && source .venv/bin/activate
    pip install -e ".[dev]"

Making Changes to the JavaScript Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is an `anywidget <https://github.com/manzt/anywidget>`__ project, which means the code base is hybrid Python and JavaScript. The JavaScript part is developed under js/ and uses `esbuild <https://esbuild.github.io>`__ to bundle the code. Any time you make changes to the JavaScript code, you need to rebuild the files under src/ipyniivue/static. This can be done in two ways:

.. code-block:: console

    $ npm run build

which will build the JavaScript code once, or you can start a development server:

.. code-block:: console

    $ npm run dev

which will start a development server that will automatically rebuild the code as you make changes. We recommend the latter approach, as it is more convenient.

Once you have the development server running, you can start the JupyterLab or VS Code to develop the widget. When finished, you can stop the development server with Ctrl+C.

NOTE: In order to have anywidget automatically apply changes as you work, make sure to export ANYWIDGET_HMR=1 environment variable. This can be set directly in a notebook with %env ANYWIDGET_HMR=1 in a cell.