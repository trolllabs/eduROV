import argparse
import subprocess
import time
from multiprocessing import Process

import Pyro4

from http_servers import start_http_server
from manage_sense_hat import start_sense_hat
from pyro_classes import start_pyro_classes
from support import valid_resolution, args_resolution_help, \
    STANDARD_RESOLUTIONS


def start_http_and_pyro(video_resolution, fps, server_port, debug):
    name_server = subprocess.Popen('pyro4-ns', shell=False)
    pyro_classes = Process(target=start_pyro_classes)
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
            rov.run = False
            sense.join()
            time.sleep(3)
            print('shutting down the rest')
            web.terminate()
            pyro_classes.terminate()
            name_server.terminate()
            # name_server.wait()


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
        video_res = valid_resolution(args.r)
        start_http_and_pyro(video_resolution=video_res,
                            fps=args.fps,
                            server_port=args.port,
                            debug=args.debug)
