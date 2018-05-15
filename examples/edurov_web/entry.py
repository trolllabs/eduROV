import argparse

from edurov.utils import valid_resolution, check_requirements
from .start import main


def edurov_web(args=None):
    parser = argparse.ArgumentParser(
        description='Start the Engage eduROV web server')
    parser.add_argument(
        '-r',
        metavar='RESOLUTION',
        type=str,
        default='1024x768',
        help='''resolution, use format WIDTHxHEIGHT (default 1024x768)''')
    parser.add_argument(
        '-fps',
        metavar='FRAMERATE',
        type=int,
        default=30,
        help='framerate for the camera (default 30)')
    parser.add_argument(
        '-port',
        metavar='SERVER_PORT',
        type=int,
        default=8000,
        help="which port the server should serve it's content (default 8000)")
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='set to print debug information')

    args = parser.parse_args()

    if check_requirements():
        video_res = valid_resolution(args.r)
        main(
            video_resolution=video_res,
            fps=args.fps,
            server_port=args.port,
            debug=args.debug)
