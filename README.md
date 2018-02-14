# eduROV
The eduROV project is all about spreading the joy of technology and learning. 
The eduROV is being developed as a DIY ROV kit meant to be affordable and usable by schools, hobbyists, researchers and others as they see fit.
We are committed to be fully open-source, both software and hardware-wise, everything we develop will be available to you. Using other open-source and or open-acces tools and platforms.

Builds on this repo of previous work: https://github.com/Slattsveen/eduROV_v2


## Installation

- python 3 should be installed already, check by running `python3 --version`
- download the files and move into the newly created folder:
  ```
  git clone https://github.com/trolllabs/eduROV.git
  cd eduROV/
  ```
- select correct branch:
  ```
  git checkout http
  ```
  ```
- install the requirements:
  ```
  pip install -r requirements.txt
  ```
  
## Usage

The eduROV package works by starting a http server on the raspberry pi. This server can be accessed on any machine connected to the same network as the pi, either through a router or or a peer-to-peer network.

```
On the raspberry pi, run:
```
python3 start_server.py
```
This will print the ip address where the website can be accessed. Then, open this website in a browser on your computer.

## Help

For additional paramters and information, run:
```
python start.py -h
```