************
Installation
************

Raspbian
========

First, you will need a raspberry pi with an operating system running on it.
Visit the `official software guide <https://www.raspberrypi.org/learning/software-guide/quickstart/>`_
for a step by step guide on how to do that..

Remote control
==============

In most cases it is more practical to control the Raspberry Pi using another
computer. The two most popular methods are with either
`SSH <https://www.raspberrypi.org/documentation/remote-access/ssh/README.md>`_
or `VNC <https://www.raspberrypi.org/documentation/remote-access/vnc/README.md>`_.

Update system
=============

Make sure that your Raspberry Pi is up to date::

    sudo apt-get update
    sudo apt-get dist-upgrade

Python version
==============

The edurov package requires python 3. If python 3 si not your default python
version (check by running :code:`python --version`), you can either (1) change the
default python version, or (2) use pip3 and python3 instead.

1. **Change default python version**

   Take a look at `this page <https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux>`_.


2. **Use pip3 and python3**

   If you don't want to make any changes, you can call :code:`pip3` instead of :code:`pip`
   and :code:`python3` instead of :code:`python`. This will use version 3 when installing
   and running python scripts instead.

Install using pip
=================

Install edurov, sudo rights are needed to enable console scripts::

  sudo pip install edurov


Static IP
=========

If you are remotely connected to the Pi it can be very useful with a static ip
so that you can find the Pi on the network. How you should configure this
depends how your network is setup. A guide can be found
`here <https://www.modmypi.com/blog/how-to-give-your-raspberry-pi-a-static-ip-address-update>`_.

Start at system startup
=======================

If you want the edurov-web command to run automatically when the raspberry pi
has started. Run the following command::

    sudo nano /etc/rc.local

Then add the following line to the bottom of the screen, but *before* the line
that says :code:`exit 0`::

    edurov-web &

Exit and save by pressing CTRL+C, y, ENTER. The system then needs to be
rebooted::

    sudo shutdown -r now
