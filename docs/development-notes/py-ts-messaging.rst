Messaging between Python and Typescript
=======================================

| ipyniivue uses websocket messages to communicate between the Python
  and TypeScript sides.
| On the Python end,

.. code:: py

   DOMWidget.send(command, buffers)

is used and on the TypeScript end,

.. code:: js

   DOMWidgetModel.send(content, callbacks, buffers);

is used.

Setters
-------

Setters in ipyNiiVue are implemented by sending a message from Python to
TypeScript.

To send a custom command, ``DOMWidgetModel.send([name, args], buffers)``
is used, where the name is the name of the function to call and args is
a list. Buffers are used for large data transfers.

The ``Niivue.save_scene`` function is an example of a setter. This
function, which saves the webgl2 canvas as a png format bitmap, sends
the content ``["saveScene", [filename]]`` over websockets. On the
TypeScript end, the command is processed and ``nv.saveScene(args[0])``
is run.

Note, the reason for listing out each case in the switch statement in
the TypeScript end instead of using something like
``nv[name]?.apply(nv, args)`` is that some niivue setter functions need
to be awaited. Awaiting all functions (using
``await nv[name]?.apply(nv, args)``) would result in a performance drop, as
described in here: https://stackoverflow.com/a/55276645.

Getters
-------

Some getters in ipyNiiVue are implemented by: 1) sending a websocket
message from Python to TypeScript and waiting for a response. 2) sending
a websocket message from TypeScript back to Python.

The ``Niivue.run_custom_code`` function displays this implementation.

.. code:: py

   >>> colormaps = nv.run_custom_code('nv.colorMaps()')
   Done.

   >>> print(colormaps)
   ['actc', 'bcgwhw', 'bcgwhw_dark', 'blue', 'blue2red', 'bluegrn', 'bone', 'bronze', 'cividis', 'cool', 'copper', 'copper2', 'ct_airways', 'ct_artery', 'ct_bones', 'ct_brain', 'ct_brain_gray', 'ct_cardiac', 'ct_head', 'ct_kidneys', 'ct_liver', 'ct_muscles', 'ct_scalp', 'ct_skull', 'ct_soft', 'ct_soft_tissue', 'ct_surface', 'ct_vessels', 'ct_w_contrast', 'cubehelix', 'electric_blue', 'freesurfer', 'ge_color', 'gold', 'gray', 'green', 'hot', 'hotiron', 'hsv', 'inferno', 'jet', 'linspecer', 'magma', 'mako', 'nih', 'plasma', 'random', 'red', 'redyell', 'rocket', 'surface', 'turbo', 'violet', 'viridis', 'warm', 'winter', 'x_rain']

Note, Niivue.run_custom_code uses eval on the TypeScript end to evaluate
the JavaScript.

Wait for Websocket messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~

ipyNiiVue uses the `jupyter-ui-poll
library <https://github.com/Kirill888/jupyter-ui-poll>`__ to block for
cell interaction while waiting for websocket messages.

Without this polling library, the wait-for while loop in
``Niivue.run_custom_code`` would prevent the Python-TypeScript
messaging.

Chunking
~~~~~~~~

Large messages coming from the TypeScript end are chunked into 5mb
chunks.

This is done to prevent the websocket from disconnecting when greater
than 10mb of data needs to be sent over the websocket. See
https://github.com/jupyter-widgets/ipywidgets/issues/2522.

Debugging TypeScript to Python messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Debugging the messages that come from the TypeScript end is not
straightforward. Errors that come from ``Niivue.on_msg(...)`` and
``Niivue._handle_frontend_msg`` are not shown in the logs.

Instead, to retrieve error logs for these (if there are errors), you
need to look at the websocket traffic. To do this, open Developer Tools
-> Network -> WS. Then, you will need to find which websocket connection
is responsible for sending messages about widget states (you will need
to run a cell in Jupyter and see which websocket connection sends back
messages). Red down arrows show incoming data and green up arrows show
outgoing data, for Chrome Developer Tools. |example developer tools
view|

After you find the correct websocket connection, tab through the
incomming messages to find the message with channel=‘iopub’ and
msg_type=‘error’. An example is shown below: |traceback|

Right click on the traceback (is under content), click ``Copy value``,
go to the Console, and define a variable. Set the value of this variable
to be the value you just copied. For the purposes of this demonstration,
let’s assume this variable is named ``errors``. Next, you can run the
following in console to print the errors:

.. code:: js

   for (const i of errors) {
       console.log(i);
   }

.. |example developer tools view| image:: ./ws.png
.. |traceback| image:: ./traceback.png
