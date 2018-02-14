import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import socket
import fcntl
import struct
import os

cwd = os.path.dirname(os.path.abspath(__file__))
index_file = os.path.join(cwd,'index.html')
css_file = os.path.join(cwd, '/web_content/style.css')
script_file = os.path.join(cwd, '/web_content/script.js')

with open(index_file, 'r') as f:
    html = f.read()

with open(css_file, 'r') as f:
    css = f.read()

with open(script_file, 'r') as f:
    script = f.read()

PAGE = html.format('<style>{}</style>'.format(css),
                   '<script>{}</script>'.format(script))

# CSS = """
# <style>
# body {
#     margin: 0;
#     padding: 0;
# }
#
# img {
#     display: block;
#     margin: 0 auto;
# }
#
# </style>
# <script>
# function resizeToMax(id){
#     myImage = new Image()
#     var img = document.getElementById(id);
#     myImage.src = img.src;
#     var imgRatio = myImage.width / myImage.height;
#     var bodyRatio = document.body.clientWidth / document.body.clientHeight;
#     if(bodyRatio < imgRatio){
#         img.style.width = "100%";
#     } else {
#         img.style.height = "100%";
#     }
# }
# </script>
# """
#
# PAGE="""\
# <html>
# <head>
# <title>eduROV</title>
# {0}
# </head>
# <body>
# <img id="image" src="stream.mjpg" onload="resizeToMax(this.id)">
# </body>
# </html>
# """.format(CSS)


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
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
    for interface in [b'wlan0', b'eth0']:
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
    print_server_ip()

    with picamera.PiCamera(resolution='1024x768', framerate=24) as camera:
        output = StreamingOutput()
        camera.start_recording(output, format='mjpeg')
        try:
            address = ('', 8000)
            server = StreamingServer(address, StreamingHandler)
            server.serve_forever()
        finally:
            camera.stop_recording()