import time

from support import detect_pi

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

sense = SenseHat()
sense.set_pixels(up)
time.sleep(2)
sense.set_pixels(left)
time.sleep(2)
sense.set_pixels(down)
time.sleep(2)
sense.set_pixels(right)
time.sleep(2)
