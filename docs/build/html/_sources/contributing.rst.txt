Contributing
============

We are glad you are here! Contributions to this package are always welcome.
Read on to learn more about the contribution process and package design.

Setting up your development environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To get started, you will need to clone the pyLossless repository and install
the package in development mode. This will allow you to make changes to the
package and see the changes reflected in your python environment.

This assumes that you have already forked and cloned the pyLossless repository,
and that you have navigated to the root of the repository in your terminal.

.. code-block:: console

   $ pip install --editable ./pylossless
   $ pip install -r requirements_testing.txt
   $ pip install -r docs/requirements_doc.txt

Install Pre-Commit hooks
^^^^^^^^^^^^^^^^^^^^^^^^
We use `pre-commit <https://pre-commit.com/>`__ to run code checks before
committing changes. To install the pre-commit hooks, run the following command:

.. code-block:: console

   $ pre-commit install --install-hooks