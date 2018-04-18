import argparse
import os
import RPi.GPIO as GPIO
import Pyro4

from edurov import WebMethod


class Motor(object):
    def __init__(self, a_pin, b_pin, reverse=False, pwd=False):
        self.reverse = reverse
        if not reverse:
            self.a_pin = a_pin
            self.b_pin = b_pin
        else:
            self.a_pin = b_pin
            self.b_pin = a_pin
        GPIO.setmode(GPIO.BCM)
        for pin in [a_pin, b_pin]:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def forward(self, speed=1.0):
        if not self.reverse:
            GPIO.output(self.a_pin, GPIO.HIGH)
            GPIO.output(self.b_pin, GPIO.LOW)

    def backward(self, speed=1.0):
        if not self.reverse:
            GPIO.output(self.a_pin, GPIO.LOW)
            GPIO.output(self.b_pin, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.a_pin, GPIO.LOW)
        GPIO.output(self.b_pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()


def control_motors():
    m1 = Motor(4, 18)
    m2 = Motor(12, 19)

    with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
        with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
            while rov.run:
                keys_dict = keys.arrow_dict()
                if keys_dict['up arrow']:
                    m1.forward()
                    m2.forward()
                elif keys_dict['down arrow']:
                    m1.backward()
                    m2.backward()
                else:
                    m1.stop()
                    m2.stop()
            m1.cleanup()
            m2.cleanup()


def main(video_resolution='1024x768', fps=30, server_port=8000, debug=False):
    web_method = WebMethod(
        video_resolution=video_resolution,
        fps=fps,
        server_port=server_port,
        debug=debug,
        runtime_functions=control_motors,
        index_file=os.path.join(os.path.dirname(__file__), 'index.html', )
    )
    web_method.serve()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Start a streaming video server on raspberry pi')
    parser.add_argument(
        '-r',
        metavar='RESOLUTION',
        type=str,
        default='1024x768',
        help='''resolution, use format WIDTHxHEIGHT or an integer''')
    parser.add_argument(
        '-fps',
        metavar='FRAMERATE',
        type=int,
        default=30,
        help='framerate for the camera (default 30)')
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='set to print debug information')

    args = parser.parse_args()

    main(
        video_resolution=args.r,
        fps=args.fps,
        server_port=8000,
        debug=args.debug
        )
