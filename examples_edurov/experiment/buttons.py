import argparse

import requests

from edurov.utils import serial_connection, receive_arduino_simple


def main(server_ip, server_port):
    ser = serial_connection(baudrate=9600)
    msg = receive_arduino_simple(serial_connection=ser, min_length=5)
    if msg:
        button = msg.split('=')[1]
        link = 'http://{ip}:{port}/new_hit?button={btn}' \
            .format(ip=server_ip, port=server_port, btn=button)
        r = requests.get(link)

        if r.status_code is 200:
            print('Successly sent button {}'.format(button))
        else:
            print('error sending')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Register button hits from arduino and sends http request')
    parser.add_argument(
        '-ip',
        default='192.168.0.230',
        help='IP of webserver',
        type=str)
    parser.add_argument(
        '-port',
        default=8000,
        help='port of webserver',
        type=str)

    args = parser.parse_args()
    main(server_ip=args.ip, server_port=args.port)