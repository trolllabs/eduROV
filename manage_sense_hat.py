from support import detect_pi

if detect_pi():
    from sense_hat import SenseHat

X = [255, 0, 0]  # Red
O = [255, 255, 255]  # White

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

sense = SenseHat()
sense.set_pixels(up)
