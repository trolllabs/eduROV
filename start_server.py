import io
import logging
import socketserver
from threading import Condition
from http import server
import socket
import struct
import os
import argparse
import time
import platform
import random
import json
if 'raspberrypi' in platform._syscmd_uname('-a'):
    import picamera
    import fcntl
from support import valid_resolution, args_resolution_help, STANDARD_RESOLUTIONS

cwd = os.path.dirname(os.path.abspath(__file__))
index_file = os.path.join(cwd, 'index.html')
css_file = os.path.join(cwd, './static/style.css')
script_file = os.path.join(cwd, './static/script.js')


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

    def serve_static(self, path):
        if 'style.css' in path:
            with open(css_file,'rb') as f:
                content = f.read()
                content_type = 'text/css'
        elif 'script.js' in path:
            with open(script_file,'rb') as f:
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

    def do_POST(self):
        print('Got: {}'.format(self.path))

    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            with open(index_file,'rb') as f:
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
        else:
            self.send_404()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ip = socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
    print(ip)
    s.close()


def print_server_ip():
    online_ips = []
    for interface in [b'eth0', b'wlan0']:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            ip = socket.inet_ntoa(fcntl.ioctl(
                sock.fileno(),
                0x8915,
                struct.pack('256s', interface[:15])
            )[20:24])
            online_ips.append(ip)
        except OSError:
            pass
        sock.close()
    print('Visit the webpage at {}'
          .format(' or '.join(['{}:8000'.format(ip) for ip in online_ips])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Start a streaming video server on raspberry pi')
    parser.add_argument(
        '-r',
        metavar='RESOLUTION',
        type=str,
        default='1024x768',
        help='''resolution, use format WIDTHxHEIGHT or an integer 0-{} 
        (default 1024x600)'''.format(len(STANDARD_RESOLUTIONS)-1))
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

    res = valid_resolution(args.r)
    print_server_ip()
    if args.debug:
        print('Using {} @ {} fps'.format(res, args.fps))

    with picamera.PiCamera(resolution=res, framerate=args.fps) as camera:
        output = StreamingOutput()
        camera.start_recording(output, format='mjpeg')
        start = time.time()
        try:
            address = ('', 8000)
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
                              finish-start, output.count/(finish-start)))
