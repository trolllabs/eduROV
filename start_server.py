import argparse
import io
import json
import logging
import os
import platform
import random
import socketserver
import time
import sys
from http import server
from threading import Condition
from support import valid_resolution, args_resolution_help, \
    STANDARD_RESOLUTIONS, server_ip

if 'raspberrypi' in platform._syscmd_uname('-a'):
    import picamera

cwd = os.path.dirname(os.path.abspath(__file__))
index_file = os.path.join(cwd, 'index.html')
css_file = os.path.join(cwd, './static/style.css')
script_file = os.path.join(cwd, './static/script.js')
SERVER_PORT = 8000


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()
        self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
            self.count += 1
        return self.buffer.write(buf)


class StreamingHandler(server.BaseHTTPRequestHandler):
    """Main server that provides the webpage"""

    def serve_static(self, path):
        if 'style.css' in path:
            with open(css_file, 'rb') as f:
                content = f.read()
                content_type = 'text/css'
        elif 'script.js' in path:
            with open(script_file, 'rb') as f:
                content = f.read()
                content_type = 'text/javascript'
        else:
            self.send_404()
            return

        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content)

    def send_404(self):
        self.send_error(404)
        self.end_headers()

    def serve_sensor(self):
        cpu_load = random.randrange(100)
        temperature = random.randrange(10, 30)
        r = {"cpu_load": cpu_load, "temperature": temperature}
        r = json.dumps(r)
        content = r.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content)

    def serve_stream(self):
        self.send_response(200)
        self.send_header('Age', 0)
        self.send_header('Cache-Control', 'no-cache, private')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Content-Type',
                         'multipart/x-mixed-replace; boundary=FRAME')
        self.end_headers()
        try:
            while True:
                with output.condition:
                    output.condition.wait()
                    frame = output.frame
                self.wfile.write(b'--FRAME\r\n')
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Content-Length', len(frame))
                self.end_headers()
                self.wfile.write(frame)
                self.wfile.write(b'\r\n')
        except Exception as e:
            logging.warning(
                'Removed streaming client %s: %s',
                self.client_address, str(e))

    def do_POST(self):
        if self.path.startswith('/keys.json'):
            content_len = int(self.headers['Content-Length'])
            post_body = self.rfile.read(content_len).decode('utf-8')
            json_obj = json.loads(post_body)
            print(json_obj)
            self.send_response(200)
            self.end_headers()

        else:
            self.send_404()

    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            with open(index_file, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path.startswith('/static/'):
            self.serve_static(self.path)
        elif self.path.startswith('/sensordata.json'):
            self.serve_sensor()
        elif self.path == '/stream.mjpg':
            self.serve_stream()
        else:
            self.send_404()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


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
            server = StreamingServer(address, StreamingHandler)
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
