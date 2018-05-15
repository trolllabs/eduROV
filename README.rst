eduROV - Educational Remotely Operated Vehicle
==============================================

The eduROV project is all about spreading the joy of technology and learning.
The eduROV is being developed as a DIY ROV kit meant to be affordable and
usable by schools, hobbyists, researchers and others as they see fit.
We are committed to be fully open-source, both software and hardware-wise,
everything we develop will be available to you. Using other open-source and or
open-acces tools and platforms.

:GitHub: https://github.com/trolllabs/eduROV
:PyPI: https://pypi.org/project/edurov/
:Documentation: http://edurov.readthedocs.io
:Engage eduROV: https://www.edurov.no/

.. image:: ./docs/edurov_gui.jpg

Prerequisites
*************
- eduROV requires python 3, if you don't have python installed, you can
  download it here: https://www.python.org/downloads/
- if python 3 is not your default python interpreter, pip3 and python3 should
  be used as in this instruction
- the camera on the raspberry pi has to be enabled, see
  https://www.raspberrypi.org/documentation/configuration/camera.md

Installation
************
Run the following commands in a terminal on the Raspberry Pi.::

  sudo pip3 install edurov

For a more in depth description visit `the official documentation <http://edurov.readthedocs.io/>`_.

Usage
*****

Engage eduROV submersible
-------------------------

On the Raspberry Pi, run the following command::

  edurov-web

This will start the web server and print the ip where the web page can be
viewed, e.g. ``Visit the webpage at 192.168.0.197:8000``.

Create your own
---------------

The eduROV package includes multiple classes and functions to facilitate
easy robot communication with video feed. It will get you up and running in a
matter of minutes. Visit
`the official documentation <http://edurov.readthedocs.io/>`_ for examples and
API.

Performance
***********
The eduROV package were created with a strong focus on keeping the latency at
a minimum. When deploying on a wireless network the actual performance will
vary depending on factors such as distance, interference and hardware.

.. image:: ./docs/latency.png
