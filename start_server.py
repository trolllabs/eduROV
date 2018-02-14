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
import sys
import platform
if 'raspberrypi' in platform._syscmd_uname('-a'):
    import picamera
    import fcntl

cwd = os.path.dirname(os.path.abspath(__file__))
index_file = os.path.join(cwd, 'index.html')
css_file = os.path.join(cwd, './web_content/style.css')
script_file = os.path.join(cwd, './web_content/script.js')

with open(index_file, 'r') as f:
    html = f.read()
with open(css_file, 'r') as f:
    css = f.read()
with open(script_file, 'r') as f:
    script = f.read()
PAGE = html.format('<style>{}</style>'.format(css),
                   '<script>{}</script>'.format(script))

STANDARD_RESOLUTIONS = ['160x120', '240x160', '640x360', '640x480', '960x540',
                        '960x640', '1024x576', '1024x600', '1024x768', '1152x864',
                        '1280x720', '1296x972', '1640x1232', '1920x1080']


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
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            # content = PAGE.encode('utf-8')
            with open('index2.html','r') as f:
                content = f.read().encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/static/style.css':
            with open(css_file,'r') as f:
                content = f.read().encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/css')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/static/script.js':
            with open(script_file,'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/javascript')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
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
            self.send_error(404)
            self.end_headers()


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


def valid_resolution(resolution):
    if 'x' in resolution:
        if len(resolution.split('x')) is 2:
            return resolution
        else:
            raise ValueError('Resolution must be WIDTHxHEIGHT or an integer')
    try:
        idx = int(resolution)
        if idx in range(0,len(STANDARD_RESOLUTIONS)):
            return STANDARD_RESOLUTIONS[idx]
        else:
            raise ValueError('Resolution index must be inr range 0-{}, not {}'
                             .format(len(STANDARD_RESOLUTIONS), idx))
    except ValueError:
        raise ValueError('Resolution must be WIDTHxHEIGHT or an integer')


def args_resolution_help():
    print('{:<8} {:<10}'.format('Number', 'Resolution'))
    for idx, res in enumerate(STANDARD_RESOLUTIONS):
        print('{:<8} {:<10}'.format(idx, res))
    sys.exit()


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
