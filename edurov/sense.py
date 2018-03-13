"""
Manage the sense hat
"""

import signal

import Pyro4

from edurov.utils import detect_pi

if detect_pi():
    from sense_hat import SenseHat

X = [255, 255, 255]
O = [0, 0, 0]

up = [
    O, O, O, X, X, O, O, O,
    O, O, X, X, X, X, O, O,
    O, X, X, X, X, X, X, O,
    X, X, O, X, X, O, X, X,
    O, O, O, X, X, O, O, O,
    O, O, O, X, X, O, O, O,
    O, O, O, X, X, O, O, O,
    O, O, O, X, X, O, O, O
]

down = [
    O, O, O, X, X, O, O, O,
    O, O, O, X, X, O, O, O,
    O, O, O, X, X, O, O, O,
    O, O, O, X, X, O, O, O,
    X, X, O, X, X, O, X, X,
    O, X, X, X, X, X, X, O,
    O, O, X, X, X, X, O, O,
    O, O, O, X, X, O, O, O
]

left = [
    O, O, O, X, O, O, O, O,
    O, O, X, X, O, O, O, O,
    O, X, X, O, O, O, O, O,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    O, X, X, O, O, O, O, O,
    O, O, X, X, O, O, O, O,
    O, O, O, X, O, O, O, O
]

right = [
    O, O, O, O, X, O, O, O,
    O, O, O, O, X, X, O, O,
    O, O, O, O, O, X, X, O,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    O, O, O, O, O, X, X, O,
    O, O, O, O, X, X, O, O,
    O, O, O, O, X, O, O, O
]


def start_sense_hat():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    sense = SenseHat()
    with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
        with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
            while rov.run:
                # Read key presses
                dic = keys.arrow_dict
                if dic['up arrow']:
                    sense.set_pixels(left)
                elif dic['down arrow']:
                    sense.set_pixels(right)
                elif dic['right arrow']:
                    sense.set_pixels(up)
                elif dic['left arrow']:
                    sense.set_pixels(down)
                else:
                    sense.clear()
                # Update sensors
                orientation = sense.get_orientation()
                rov.sensor = {'temp':sense.get_temperature(),
                              'pressure':sense.get_pressure(),
                              'humidity':sense.get_humidity(),
                              'pitch':orientation['pitch'],
                              'roll':orientation['roll'],
                              'yaw':orientation['yaw']}
    print('closing sense hat')


if __name__ == '__main__':
    start_sense_hat()
