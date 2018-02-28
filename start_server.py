import argparse
import platform
import time
import sys
from support import valid_resolution, args_resolution_help, \
    STANDARD_RESOLUTIONS, server_ip
from .servers import StreamingOutput, WebpageServer, RequestHandler

if 'raspberrypi' in platform._syscmd_uname('-a'):
    import picamera

SERVER_PORT = 8000


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
        sys.exit()

    res = valid_resolution(args.r)
    print('Visit the webpage at {}'.format(server_ip(SERVER_PORT)))
    if args.debug:
        print('Using {} @ {} fps'.format(res, args.fps))

    with picamera.PiCamera(resolution=res, framerate=args.fps) as camera:
        output = StreamingOutput()
        camera.start_recording(output, format='mjpeg')
        start = time.time()
        try:
            address = ('', SERVER_PORT)
            server = WebpageServer(server_address=address,
                                   RequestHandlerClass=RequestHandler)
            server.set_output(output)
            server.serve_forever()
        except KeyboardInterrupt:
            print('Shutting down server')
        finally:
            camera.stop_recording()
            finish = time.time()
            if args.debug:
                print('Sent {} images in {:.1f} seconds at {:.2f} fps'
                      .format(output.count,
                              finish - start, output.count / (finish - start)))
