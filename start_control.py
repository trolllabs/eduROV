#!/usr/bin/env python3
import argparse
from control_functions import control_main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='eduROV communication, use this to start controller')
    parser.add_argument(
        '-ip',
        metavar='IP',
        help='IP address the control listens at, (default all addresses)',
        type=str,
        default='0.0.0.0')
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
    parser.add_argument(
        '-r',
        metavar='RESOLUTION',
        type=str,
        default='1024x600',
        help='camera resolution, use WIDTHxHEIGHT (default 1024x600)')
    parser.add_argument(
        '-fps',
        metavar='FRAMERATE',
        type=int,
        default=30,
        help='camera framerate (default 30)')
    parser.add_argument(
        '-f',
        metavar='FULLSCREEN',
        type=bool,
        default=False,
        help='set True for fullscreen (not functional atm)')

    args = parser.parse_args()
    control_main(
        server_ip=args.ip,
        port_cam=args.pc,
        port_var=args.pv,
        camera_resolution=args.r,
        fullscreen=args.f,
        framerate=args.fps)
