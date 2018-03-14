"""
Send motor commands to the arduino
"""

import signal

import Pyro4

from edurov.utils import detect_pi

if detect_pi():
    import serial


def start_arduino_coms(debug=False):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    states = [0, 0, 0, 0]
    lastState = '0000'
    if not debug:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.05)
        ser.close()
        ser.open()
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
                # Light
                states[3] = int(keys.state('l'))

                state = ''.join([str(n) for n in states])
                if state != lastState:
                    lastState = state
                    if not debug:
                        ser.write(state.encode())
                    else:
                        print(state)
                if not debug:
                    if ser.inWaiting():
                        serialInput = ser.readline()
                        tempWater, pressureWater, batteryVoltage = \
                         serialInput.split(':')

                        rov.sensor = {
                            'tempWater':float(tempWater),
                            'pressureWater':float(pressureWater),
                            'batteryVoltage':float(batteryVoltage),
                            'light':keys.state('l')
                        }



    print('closing arduino coms')


if __name__ == '__main__':
    start_arduino_coms()
