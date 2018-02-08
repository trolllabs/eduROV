#!/usr/bin/env python3
import argparse
from rov import rov_main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='eduROV communication, use this to start ROV')
    parser.add_argument(
        'ip',
        help='IP address ROV sends data to',
        type=str)
    parser.add_argument(
        '-pc',
        metavar='PORTcamera',
        type=int,
        default=5050,
        help='IP port for camera feed (default 5050)')
    parser.add_argument(
        '-pv',
        metavar='PORTvariables',
        type=int,
        default=5060,
        help='IP port for communicating variables (default 5060)')

    args = parser.parse_args()
    rov_main(
        server_ip=args.ip,
        port_cam=args.pc,
        port_var=args.pv)
