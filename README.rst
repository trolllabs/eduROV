======
eduROV
======

The eduROV project is all about spreading the joy of technology and learning.
The eduROV is being developed as a DIY ROV kit meant to be affordable and
usable by schools, hobbyists, researchers and others as they see fit.
We are committed to be fully open-source, both software and hardware-wise,
everything we develop will be available to you. Using other open-source and or
open-acces tools and platforms.

Builds on this repo of previous work: https://github.com/Slattsveen/eduROV_v2

:GitHub: https://github.com/trolllabs/eduROV
:PyPI: https://pypi.org/project/edurov/

Preparation
-----------
- eduROV requires python 3, if you don't have python installed, you can
  download it here: https://www.python.org/downloads/
- if python 3 is not your default python interpreter, pip3 should be used for
  installation as in this instruction
- the camera on the raspberry pi has to be enabled, see
https://www.raspberrypi.org/documentation/configuration/camera.md

Installation
------------
Run the following command in a terminal window on your raspberry pi
(sudo rights are needed to enable console scripts)::

  sudo pip3 install edurov --pre

If you are planning on using the *duo* method as described below, you will also
need to perform this installation on your controlling computer.

Usage
-----

Methods
+++++++

:Web The raspberry pi will serve a web page that can be viewed in web browser
  on any computer on the same network
:Duo Requires that the eduROV packaged is installed on second computer and the
  video is viewed using pygame

Web method
==========

On the raspberry pi, run the following command::

  edurov-web

This will start the web server and print the ip where the web page can be
viewed.

Duo method
==========

The controlling computer needs to be started first::

  edurov-duo control ""

This will start the duo method in control mode at all ip's. This command will
print the ip address the ROV should connect to, example ``ROV should connect
to 192.168.0.190``. Then on the raspberry pi, run the following command::

  edurov-duo rov 192.168.0.190

Remember to change the ip to the one printed on your controlling computer.

Help
----

For additional parameters and information, the following commands can be used::

    edurov-web -h
    edurov-duo -h
