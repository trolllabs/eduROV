import argparse
import multiprocessing
import subprocess
import time

from http_servers import start_http_server
from manage_sense_hat import start_sense_hat
from rov_classes import start_variable_server
from support import valid_resolution, args_resolution_help, \
    STANDARD_RESOLUTIONS

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Start a streaming video server on raspberry pi')
    parser.add_argument(
        '-r',
        metavar='RESOLUTION',
        type=str,
        default='1024x768',
        help='''resolution, use format WIDTHxHEIGHT or an integer 0-{} 
        (default 1024x600)'''.format(len(STANDARD_RESOLUTIONS) - 1))
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
    parser.add_argument(
        '--resolutions',
        action="store_true",
        help='print the resolutions to use with the -r flag')

    args = parser.parse_args()
    if args.resolutions:
        args_resolution_help()
    else:
        # Pyro servers
        subprocess.Popen(['python', 'rov_classes.py'], shell=False)
        # variable_server = multiprocessing.Process(target=start_variable_server)
        # variable_server.start()
        time.sleep(5)

        # Sense hat
        subprocess.Popen(['python', 'manage_sense_hat.py'], shell=False)
        # sense_hat = multiprocessing.Process(target=start_sense_hat)
        # sense_hat.start()

        # Web servers
        video_res = valid_resolution(args.r)
        start_http_server(video_resolution=video_res,
                          fps=args.fps,
                          server_port=args.port,
                          debug=args.debug)
