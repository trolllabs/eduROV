import argparse
import os

import Pyro4
import RPi.GPIO as GPIO
from electronics import Motor, Button

from edurov import WebMethod


def control_motors():
    normal_speed = 0.7
    turn_speed = 0.5

    GPIO.setmode(GPIO.BCM)
    m1 = Motor(4, 18, pwm=True)
    m2 = Motor(12, 19, pwm=True)
    u = Button()
    d = Button()
    l = Button()
    r = Button()

    with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
        with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
            while rov.run:
                keys_dict = keys.arrow_dict
                u.update(keys_dict['up arrow'])
                d.update(keys_dict['down arrow'])
                l.update(keys_dict['left arrow'])
                r.update(keys_dict['right arrow'])

                motor1_speed = 0
                motor2_speed = 0
                if keys_dict['up arrow']:
                    motor1_speed += u.value * normal_speed
                    motor2_speed += u.value * normal_speed
                    if keys_dict['left arrow']:
                        motor1_speed += l.value * turn_speed
                        motor2_speed -= l.value * turn_speed
                    elif keys_dict['right arrow']:
                        motor1_speed -= r.value * turn_speed
                        motor2_speed += r.value * turn_speed
                elif keys_dict['down arrow']:
                    motor1_speed -= d.value * normal_speed
                    motor2_speed -= d.value * normal_speed
                    if keys_dict['left arrow']:
                        motor1_speed -= l.value * turn_speed
                        motor2_speed += l.value * turn_speed
                    elif keys_dict['right arrow']:
                        motor1_speed += r.value * turn_speed
                        motor2_speed -= r.value * turn_speed
                elif keys_dict['left arrow']:
                    motor1_speed += l.value * turn_speed
                    motor2_speed -= l.value * turn_speed
                elif keys_dict['right arrow']:
                    motor1_speed -= r.value * turn_speed
                    motor2_speed += r.value * turn_speed

                m1.speed(motor1_speed)
                m2.speed(motor2_speed)
    m1.close()
    m2.close()
    GPIO.cleanup()


def main(video_resolution='1024x768', fps=30, server_port=8000, debug=False):
    web_method = WebMethod(
        video_resolution=video_resolution,
        fps=fps,
        server_port=server_port,
        debug=debug,
        runtime_functions=control_motors,
        index_file=os.path.join(os.path.dirname(__file__), 'index.html')
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
