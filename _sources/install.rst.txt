Installation
============

To first install IPyNiiVue and its dependencies, simply run:

.. code-block:: console

    $ pip install ipyniivue

Usage
^^^^^^

In a Jupyter environment:

.. code-block:: python

    from ipyniivue import NiiVue

    nv = NiiVue()
    nv.load_volumes([{"path": "images/mni152.nii.gz"}])
    nv

See the `basic demo <https://github.com/niivue/ipyniivue/blob/main/examples/basic_multiplanar.ipynb>`__ to learn more.