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
