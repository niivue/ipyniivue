Docstrings for attributes
=========================

In Jupyter, there are 2 commonly used ways to get information on an
object: 1) using the help() function (for example, ``help([].append])``)
2) putting an ? at the end of the object (for example,
``test = []; test.append?``)

These are implemented in ipyniivue. Here are some examples:

.. code-block:: none

   from ipyniivue import Niivue

   Niivue?
   Niivue.back_color?
   Niivue.thumbnail?
   Niivue.add_volume?

However, when you do the following:

.. code-block:: none

   from ipyniivue import Niivue

   nv = Niivue()
   nv.thumbnail?

The docstring for the thumbnail attribute does not show.

This is intended behavior since the option attributes of a
ipyniivue.Niivue widget should not be modified directly. Instead, setter
functions should be used.