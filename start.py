#!/usr/bin/env python3
import argparse
from client_functions import rov
from server_functions import controller


if __name__ == '__main__':
    choices = {'controller': controller, 'rov': rov}
    parser = argparse.ArgumentParser(
        description='Stream video from picamera to machine on same network')
    parser.add_argument(
        'role',
        choices=choices,
        help='which role to play')
    parser.add_argument(
        'ip',
        help='IP address the server listens at and client sends to',
        type=str)
    parser.add_argument(
        '-p',
        metavar='PORT',
        type=int,
        default=1060,
        help='IP port (default 1060)')
    parser.add_argument(
        '-r',
        metavar='RESOLUTION',
        type=str,
        default='1024x600',
        help='resolution, use format WIDTHxHEIGHT (default 1024x600)')
    parser.add_argument(
        '-f',
        metavar='FULLSCREEN',
        type=bool,
        default=False,
        help='set True for fullscreen (not functional atm)')

    args = parser.parse_args()
    function_ = choices[args.role]
    if function_ is rov:
        rov(host=args.ip,
            port=args.p,
            resolution=args.r)
    elif function_ is controller:
        controller(ip=args.ip,
                   port=args.p,
                   resolution=args.r,
                   fullscreen=args.f)
