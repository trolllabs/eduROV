"""
Starts the edurov-web version.
"""

import signal

import Pyro4

from edurov import WebMethod
from edurov.arduino import get_serial_connection, send_arduino, \
    receive_arduino, valid_arduino_string
from edurov.utils import detect_pi
import os

if detect_pi():
    from sense_hat import SenseHat


def arduino(debug=False):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    states = [0, 0, 0, 0]
    lastState = '0000'
    if not debug:
        ser = get_serial_connection()
    with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
        with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
            keys.set_mode(key='l', mode='toggle')
            while rov.run:
                dic = keys.qweasd_dict
                if dic['w']:
                    states[0] = 1
                elif dic['s']:
                    states[0] = 2
                else:
                    states[0] = 0

                if dic['a']:
                    states[1] = 1
                elif dic['q']:
                    states[1] = 2
                else:
                    states[1] = 0

                if dic['e']:
                    states[2] = 2
                elif dic['d']:
                    states[2] = 1
                else:
                    states[2] = 0
                light_state = int(keys.state('l'))
                states[3] = light_state

                state = ''.join([str(n) for n in states])
                if state != lastState:
                    lastState = state
                    if not debug and ser:
                        send_arduino(msg=state, serial_connection=ser)
                    else:
                        print(state)
                if not debug and ser:
                    arduino_string = receive_arduino(serial_connection=ser)
                    if valid_arduino_string(arduino_string):
                        v1, v2, v3 = arduino_string.split(':')

                        rov.sensor = {
                            'tempWater': float(v1),
                            'pressureWater': float(v2),
                            'batteryVoltage': float(v3),
                            'light': light_state
                        }


def senser(debug=False):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    sense = SenseHat()
    with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
        while rov.run:
            orientation = sense.get_orientation()
            rov.sensor = {'temp': sense.get_temperature(),
                          'pressure': sense.get_pressure(),
                          'humidity': sense.get_humidity(),
                          'pitch': orientation['pitch'],
                          'roll': orientation['roll'] + 180,
                          'yaw': orientation['yaw']}


def main(video_resolution='1024x768', fps=30, server_port=8000, debug=False):
    print(os.path.abspath(__file__))
    web_method = WebMethod(
        video_resolution=video_resolution,
        fps=fps,
        server_port=server_port,
        debug=debug,
        runtime_functions=[arduino, senser],
        index_file = 'index.html'
    )
    web_method.serve()


if __name__ == '__main__':
    main()
