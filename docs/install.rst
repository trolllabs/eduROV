Installation
============

Update system
-------------
First, make sure that your Raspberry Pi is up to date::

    sudo apt-get update
    sudo apt-get dist-upgrade

Python version
--------------

The edurov package requires python 3. If python 3 si not your default python
version (check by running :code:`python --version`), you can either (a) change the
default python version, or (b) use pip3 and python3 instead.

a. Change default python version

   Take a look at `this page <https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux>`_.

b. Use pip3 and python3

   If you don't want to make any changes, you can call :code:`pip3` instead of :code:`pip`
   and :code:`python3` instead of :code:`python`. This will use version 3 when installing
   and running python scripts instead.

Install using pip
-----------------

Install edurov, sudo rights are needed to enable console scripts::

  sudo pip install edurov
