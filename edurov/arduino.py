"""
Send motor commands to the arduino
"""

import signal

import Pyro4

from edurov.utils import detect_pi, send_arduino, receive_arduino, warning

if detect_pi():
    import serial


def valid_arduino_string(arduino_string):
    if arduino_string:
        if arduino_string.count(':') == 2:
            try:
                [float(v) for v in arduino_string.split(':')]
                return True
            except:
                return False
    return False


def get_serial_connection(port, baudrate, timeout):
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.05)
        ser.close()
        ser.open()
        return ser
    except FileNotFoundError:
        pass
    except serial.serialutil.SerialException:
        pass
    warning(message='Could not establish serial connection at {}'
            .format(port), filter='default')
    return None


def start_arduino_coms(debug=False):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    states = [0, 0, 0, 0]
    lastState = '0000'
    if not debug:
        ser = get_serial_connection(
            port='/dev/ttyACM0',
            baudrate=115200,
            timeout=0.05
        )
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

    print('closing arduino coms')


if __name__ == '__main__':
    start_arduino_coms()
