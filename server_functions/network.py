import struct
import io
import sys
import socket
import pygame
from PIL import Image


def check_keys(screen_size, fullscreen):
    quit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit = True
            if event.key == pygame.K_RETURN:
                if not fullscreen:
                    pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
                    fullscreen = True
                else:
                    pygame.display.set_mode(screen_size)
                    fullscreen = False
    return quit, fullscreen


def get_screen(screen_size, fullscreen):
    if fullscreen:
        return pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode(screen_size)


class Server(object):
    def __init__(self, ip, port):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(0)
        print('Listening at', self.sock.getsockname())
        print('Client should connect to {}'
              .format(socket.gethostbyname(socket.gethostname())))
        # Accept a single connection and make a file-like object out of it
        self.conn = self.sock.accept()[0].makefile('rb')
        self.image_stream = io.BytesIO()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Shutting down server')
        self.conn.close()
        self.sock.close()
        sys.exit()

    def __enter__(self):
        return self

    def img_stream(self):
        self.image_stream.seek(0)
        image_len = \
            struct.unpack('<L', self.conn.read(struct.calcsize('<L')))[0]
        if not image_len:
            raise ConnectionError('Image length is None')
        # Read image data and convert: BytesIO > PIL.Image > pygame.image
        # image_stream = io.BytesIO()
        self.image_stream.write(self.conn.read(image_len))
        return self.image_stream


def server(ip, port, resolution, fullscreen):
    pygame.init()
    screen_size = tuple([int(val) for val in resolution.split('x')])
    screen = get_screen(screen_size, fullscreen)

    with Server(ip, port) as serve:
        while True:
            exit, fullscreen = check_keys(screen_size, fullscreen)
            if exit: break
            pil_frame = Image.open(serve.img_stream()).tobytes()
            frame = pygame.image.fromstring(pil_frame, screen_size, 'RGB')
            screen.blit(frame, (0,0))
            pygame.display.flip()
