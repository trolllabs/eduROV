"""
Argument parser for the web method
"""

import argparse
import signal
import subprocess
import time
import warnings
from multiprocessing import Process

warnings.simplefilter('error', UserWarning)

import Pyro4

from edurov.sense import start_sense_hat
from edurov.sync import start_sync_classes
from edurov.utils import valid_resolution, args_resolution_help, \
    STANDARD_RESOLUTIONS, detect_pi, check_requirements
from .servers import start_http_server


def preexec_function():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def start_http_and_pyro(video_resolution, fps, server_port, debug):
    name_server = subprocess.Popen('pyro4-ns', shell=False,
                                   preexec_fn=preexec_function)
    time.sleep(2)
    pyro_classes = Process(target=start_sync_classes)
    pyro_classes.start()
    time.sleep(5)

    web = Process(target=start_http_server,
                  args=(video_resolution, fps, server_port, debug))
    sense = Process(target=start_sense_hat)
    web.start()
    sense.start()
    with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
        try:
            while rov.run:
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass
        finally:
            print('Shutting down')
            web.terminate()
            rov.run = False
            sense.join()
            time.sleep(3)
            print('shutting down the rest')
            pyro_classes.terminate()
            name_server.terminate()


def main(args=None):
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
        help='print the resolutions to use with the -r flag and exit')

    args = parser.parse_args()

    check_requirements()
    if not detect_pi():
        warnings.warn('The http method can only be started on the ROV')
    elif args.resolutions:
        args_resolution_help()
    else:
        video_res = valid_resolution(args.r)
        start_http_and_pyro(video_resolution=video_res,
                            fps=args.fps,
                            server_port=args.port,
                            debug=args.debug)


if __name__ == '__main__':
    main()
