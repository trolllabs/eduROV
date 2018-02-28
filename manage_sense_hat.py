from support import detect_pi

if detect_pi():
    from sense_hat import SenseHat

sense = SenseHat()

sense.show_message("Hello world!")
