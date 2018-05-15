API
===

.. TIP::
  If you are having a hard time, you can always have a look at the examples
  page where the classes, methods and parameters are used in practice.

WebMethod
---------

.. code:: python

  import os
  from edurov import WebMethod

  file = os.path.join(os.path.dirname(__file__), 'index.html', )
  web_method = WebMethod(index_file=file)
  web_method.serve()

.. autoclass:: edurov.core.WebMethod
  :members:

ROVSyncer
---------

.. code:: python

  import Pyro4

  with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
      while rov.run:
          print('The ROV is still running')

.. autoclass:: edurov.sync.ROVSyncer
  :members:

KeyManager
----------

.. code:: python

  import Pyro4

  with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
    with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
        keys.set_mode(key='l', mode='toggle')
        while rov.run:
            if keys.state('K_UP'):
                print('You are pressing the up arrow')
            if keys.state('K_l'):
                print('light on')
            else:
                print('light off')

When using the methods below a **key identifier** must be used. Either the
keycode (int) or the KeyASCII or Common Name (str) from the table on the bottom
of this page can be used. Using keycode is faster.

.. autoclass:: edurov.sync.KeyManager
  :members:

Keys table
+++++++++++

.. include:: ../edurov/keys.txt
  :literal:
