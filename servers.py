import io
import os
import json
import logging
import random
import socketserver
import time
from http import server
from threading import Condition

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


class RequestHandler(server.BaseHTTPRequestHandler):
    """Main server that provides the webpage"""
    output = None

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
                with self.output.condition:
                    self.output.condition.wait()
                    frame = self.output.frame
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


class WebpageServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    def __init__(self, server_address, RequestHandlerClass,
                 stream_output, debug=False):
        self.start = time.time()
        self.debug = debug
        self.RequestHandlerClass.output = stream_output
        super(WebpageServer, self).__init__(server_address,
                                            RequestHandlerClass)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Shutting down server')
        if self.debug:
            finish = time.time()
            frame_count = self.RequestHandlerClass.output.count
            print('Sent {} images in {:.1f} seconds at {:.2f} fps'
                  .format(frame_count,
                          finish - self.start,
                          frame_count / (finish - self.start)))
