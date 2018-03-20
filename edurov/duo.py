"""
Classes and functions for the duo setup
"""

import io
import socket
import struct
import sys
from multiprocessing.pool import ThreadPool

import pygame
from PIL import Image

from edurov.utils import detect_pi
from edurov.utils import resolution_to_tuple

if detect_pi():
    import picamera

BLACK = 0, 0, 0


class Server(object):
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(1)
        print('Listening at', self.sock.getsockname())
        print('ROV should connect to {}'
              .format(socket.gethostbyname(socket.gethostname())))
        self.image_stream = io.BytesIO()

        self.client_connected = False
        self.pool = ThreadPool(processes=1)
        self.async_connection = self.pool.apply_async(self.client_connection)

    def client_connection(self):
        self.conn = self.sock.accept()[0].makefile('rb')
        self.client_connected = True

    def img_stream(self):
        self.image_stream.seek(0)
        image_len = \
            struct.unpack('<L', self.conn.read(struct.calcsize('<L')))[0]
        if not image_len:
            raise ConnectionError('Image length is None')
        self.image_stream.write(self.conn.read(image_len))
        return self.image_stream

    def get_pil_frame(self):
        return Image.open(self.img_stream()).tobytes()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Shutting down server')
        if self.client_connected:
            self.conn.close()
        self.sock.close()
        self.pool.close()


class Screen(object):
    def __init__(self, screen_size, fullscreen=False):
        self.screen_size = screen_size
        pygame.init()
        pygame.display.set_caption('eduROV (Waiting for connection)')
        self.title_updated = False
        if fullscreen:
            fullscreen = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(screen_size, fullscreen)
        self.fullscreen = fullscreen

    def update(self, pil_frame=None):
        self.read_keys()
        if pil_frame:
            if not self.title_updated:
                pygame.display.set_caption('eduROV')
                self.title_updated = True

            frame = pygame.image.fromstring(pil_frame, self.screen_size, 'RGB')
            self.screen.blit(frame, (0, 0))
        else:
            self.screen.fill(BLACK)
        pygame.display.flip()

    def read_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__exit__(True, True, True)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__exit__(True, True, True)
                if event.key == pygame.K_RETURN:
                    self.toggle_fullscreen()

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.fullscreen = False
        else:
            self.fullscreen = pygame.FULLSCREEN
        pygame.display.set_mode(self.screen_size, self.fullscreen)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.exit()


class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)


class Client(object):
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((ip, port))
        print('Client has been assigned socket name', self.sock.getsockname())
        self.conn = self.sock.makefile('wb')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Shutting down client')
        self.conn.write(struct.pack('<L', 0))
        self.conn.close()
        self.sock.close()


def rov_main(host, port, resolution):
    with Client(host, port) as client:
        output = SplitFrames(client.conn)
        with picamera.PiCamera(resolution=resolution, framerate=30) as camera:
            camera.start_recording(output, format='mjpeg')
            while True:
                camera.wait_recording(1)


def control_main(ip, port, resolution, fullscreen):
    screen_size = resolution_to_tuple(resolution)
    with Screen(screen_size=screen_size, fullscreen=fullscreen) as screen:
        with Server(ip, port) as server:
            while True:
                if server.client_connected:
                    screen.update(server.get_pil_frame())
                else:
                    screen.update()
