*************
Engage eduROV
*************

Terminal command
================

By calling :code:`edurov-web` in the terminal the edurov-web example will be
launched. This command also supports multiple flags that can be displayed by
running  :code:`edurov-web -h`

-r     resolution, use format WIDTHxHEIGHT (default 1024x768)
-fps   framerate for the camera (default 30)
-port  which port the server should serve it's content (default 8000)
-d     set to print debug information

**Example**

.. code:: shell

  edurov-web -r 640x480 -fps 10

Will then set the the video to 640x480 @ 10 fps