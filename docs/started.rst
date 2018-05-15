Getting started
================

.. TIP::
  If you came here to find out how to to use the Engage ROV submersible, the
  `Engage eduROV <http://edurov.readthedocs.io/en/latest/engage.html>`_ page
  is probably for you. If you instead plan to create your own ROV or make some
  kind of modifications, you are in the right place.

On this page we will walk through the
`features example <https://github.com/trolllabs/eduROV/tree/master/examples/features>`_,
one feature at a time. This example was created with the intention of
describing all the features of the edurov package. Let's get started!

Displaying the video feed
-------------------------
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
The server will then populate this tag with the one coming from the camera.

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