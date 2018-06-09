***************
Getting started
***************

.. TIP::
  If you came here to find out how to to use the Engage ROV submersible, the
  `Engage eduROV <http://edurov.readthedocs.io/en/latest/engage.html>`_ page
  is probably for you. If you instead plan to create your own ROV or make some
  kind of modifications, you are in the right place.

.. NOTE::
  Not all details at explained on this page. You should check the API page for
  more information on the classes, methods and parameters when you need.

On this page we will walk through the
`features example <https://github.com/trolllabs/eduROV/tree/master/examples/features>`_,
one feature at a time. This example was created with the intention of
describing all the features of the edurov package. Let's get started!

.. _Displaying-the-video-feed:

Displaying the video feed
===============================

There are two main parts needed in any edurov project. First, it's the python
file that creates the :class:`~edurov.core.WebMethod` class and starts serving the server.
Secondly, a index.html file that describes how the different objects will be
displayed in the browser.

In the two code blocks underneath you can see how simple they can be created.
The index.html file needs to be called exactly this. We use the :meth:`os.path`
library to ensure correct file path description.

.. literalinclude:: ../examples/features/features.py
   :caption: features.py
   :language: python
   :linenos:
   :lines: 1,6,32-35,38-40

The index.html file must have an img element with :code:`src="stream.mjpg"`.
The server will then populate this image with the one coming from the camera.

.. literalinclude:: ../examples/features/index.html
   :caption: index.html
   :language: html
   :linenos:
   :lines: 1-4,8,9,12,21,22

Our file structure now looks like this:

::

    project
    ├── features.py
    └── index.html

If you wanted to have a security camera system this is all you had to do. If
you instead want to control you robot through the browser or display other
information, keep reading.

Moving a robot
===============================

This section will let us control the ROV from within the web browser. In
computer technology there is something called *parallelism*. It basically means
that the CPU does multiple things at the same time in different processes. This
is an important feature of the edurov package as it let's us do many things
without interrupting the video feed. (It wouldn't be very practical if the
video stopped each time we moved the robot).

Reading keystrokes
--------------------

First, we have to ask the browser to send us information when keys
are pressed. We do this by including :code:`keys.js` inside the
:code:`index.html` file. We have put it inside a folder called *static* as this
is the convention for these kind of files.

.. literalinclude:: ../examples/features/index.html
   :caption: index.html
   :language: html
   :linenos:
   :emphasize-lines: 5
   :lines: 1-4,6,8,9,12,21,22


.. literalinclude:: ../examples/features/static/keys.js
   :caption: /static/keys.js
   :language: javascript
   :linenos:
   :lines: 6-33

.. _Controlling-motors-(or-anything):

Controlling motors (or anything)
------------------------------------

In this example we will not show how to move the motors, instead the program
will print out which arrow key you are pressing. You can then change the code
to do whatever you want!

.. literalinclude:: ../examples/features/features.py
   :caption: features.py
   :language: python
   :emphasize-lines: 2,5-17,22
   :linenos:
   :lines: 1,4,6,17-30,32-36,38-40

On line 22 we are telling the :class:`~edurov.core.WebMethod` that
:code:`control_motors` should be a :code:`runtime_function`. This starts the
function in another process and shuts it down when we stop the ROV. For more
information visit the API page. Since this function is running in another
process it needs to communicate with the server. It does this by the help of
:code:`Pyro4` (line 2). We then connect to the :code:`KeyManager` and
:code:`ROVSyncer` on line 7-8. This let's us access the variables we need.

The resulting file structure:

::

    project
    ├── features.py
    ├── index.html
    └── static
        └── keys.js

Making it pretty
==================

At this point our web page is very boring. It is white with one image.
Since it's a html file we can add whatever we want to it! This time we are
adding a header, a button to stop the server and some information. In addition
we are adding some styling that will center the content and make it look nicer.

.. literalinclude:: ../examples/features/index.html
   :caption: index.html
   :language: html
   :linenos:
   :emphasize-lines: 5
   :lines: 1-6,8-14,16-22


.. literalinclude:: ../examples/features/static/style.css
   :caption: /static/style.css
   :language: css
   :linenos:


::

    project
    ├── features.py
    ├── index.html
    └── static
        ├── keys.js
        └── style.css

Displaying sensor values
===============================

Coming soon

.. _Custom-Responses:

Custom responses
===============================

In some cases you want to display information in the browser that you want to
create yourself in a python function. The :class:`~edurov.core.WebMethod` has
a parameter exactly for this purpose.

.. literalinclude:: ../examples/features/features.py
   :caption: features.py
   :language: python
   :emphasize-lines: 9-15,37
   :linenos:

.. literalinclude:: ../examples/features/index.html
   :caption: index.html
   :language: html
   :linenos:
   :emphasize-lines: 7, 15

.. literalinclude:: ../examples/features/static/extra.js
   :caption: /static/extra.js
   :language: javascript
   :linenos:

As an example we have created a button in :code:`index.html` (line 15) which
calls a function in :code:`extra.js` that asks the server what the CPU
temperature is. The new .js file is included as usual (:code:`index.html`
(line 7)). On line 7 in :code:`extra.js` we send a GET request with a value of
*cpu_temp*. The server does not know how it should answer this request, but
since we have defined a :code:`custom_response` (line 37) in
:code:`features.py` the request is forwarded to this function and we can
create the response our self!

Note that this function needs to accept *two* parameters whereas the last one
is path that is requested. If the path starts with :code:`/cpu_temp` we can
return the value, else return :code:`None`.

::

    project
    ├── features.py
    ├── index.html
    └── static
        ├── keys.js
        ├── style.css
        └── extra.js

Adding more pages
===============================

Coming soon.