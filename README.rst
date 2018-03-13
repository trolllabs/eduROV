======
eduROV
======

The eduROV project is all about spreading the joy of technology and learning.
The eduROV is being developed as a DIY ROV kit meant to be affordable and usable by schools, hobbyists, researchers and others as they see fit.
We are committed to be fully open-source, both software and hardware-wise, everything we develop will be available to you. Using other open-source and or open-acces tools and platforms.

Builds on this repo of previous work: https://github.com/Slattsveen/eduROV_v2

:GitHub: https://github.com/trolllabs/eduROV
:PyPI: https://pypi.org/project/edurov/

Installation
============

Controller machine
------------------

- eduROV requires python 3, if you don't have python installed, you can download it here: https://www.python.org/downloads/ Running ``python --version`` in a terminal should give you ``Python 3.x.x``
- to download the required files chose ONE of the following methods:

  1. **Using git**

     Open a terminal window on chosen location, then run::

        git clone https://github.com/trolllabs/eduROV.git

  2. **Without git**

     Download the files from this link: https://github.com/trolllabs/eduROV/archive/master.zip

     Extract the files

- open a terminal window in the newly created folder and install the requirements::

    pip install -r controller_requirements.txt

Raspberry pi
------------

- python 3 should be installed already, check by running ``python3 --version``
- download the files and move into the newly created folder::

      git clone https://github.com/trolllabs/eduROV.git
      cd eduROV/

- install the requirements::

    pip install -r rov_requirements.txt

  
Usage
=====

The eduROV package works by creating an internet server on the controlling computer, the raspberry pi then streams the video so that you can view the video feed.

On the controller, run::

    python start.py controller ""

This should open a window with the title _eduROV (Waiting for connection)_. In the terminal, the following (or similar) should be written::

    Listening at ('0.0.0.0', 1060)
    ROV should connect to 169.254.148.52

Then, on the raspberry pi, run::

    python3 start.py rov 169.254.148.52

Replace the ip address with the one printed on your computer.

Help
====

For additional paramters and information, run::

    python start.py -h
