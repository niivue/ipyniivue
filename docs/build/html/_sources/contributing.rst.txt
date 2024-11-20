Contributing
============

We are glad you are here! Contributions to this package are always welcome.
Read on to learn more about the contribution process and package design.

Install Pre-Commit hooks
^^^^^^^^^^^^^^^^^^^^^^^^
We use `pre-commit <https://pre-commit.com/>`__ to run code checks and clear
notebook outputs before committing changes. To install the pre-commit hooks,
run the following command:

.. code-block:: console

   $ pre-commit install

As a result, the hooks will automatically check and fix some issues before
pushing with git. If changes are made after committing with git, you will need
to commit again afterwords. Alternatively, you can just run the following
command beforehand:

.. code-block:: console

    $ nb-clean clean --remove-empty-cells --remove-all-notebook-metadata