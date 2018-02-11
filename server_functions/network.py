import struct
import io
import sys
import socket
import multiprocessing
import pygame
from PIL import Image

def get_frame(connection, download_q):
    image_stream = io.BytesIO()
    # Read the length of the image as a 32-bit unsigned int. If the
    # length is zero, quit the loop
    while True:
        image_len = \
            struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Read image data and convert: BytesIO > PIL.Image > pygame.image
        image_stream.write(connection.read(image_len))
        download_q.put(image_stream)
        # Rewind byte stream
        image_stream.seek(0)

def jpg_to_rgb(screen_size, download_q, rgb_q):
    while True:
        PILframe = Image.open(download_q.get()).tobytes()
        rgb_q.put(pygame.image.frombuffer(PILframe, screen_size, 'RGB'))

def blit_bytes(screen, rgb_q):
    while True:
        # Update screen
        screen.blit(rgb_q.get(), (0,0))
        pygame.display.flip()


def server(interface, port, resolution, fullscreen):
    pygame.init()
    screen_size = tuple([int(val) for val in resolution.split('x')])
    if fullscreen:
        screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(screen_size)

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((interface, port))
    server_socket.listen(0)
    print('Listening at', server_socket.getsockname())
    print('Client should connect to {}'
          .format(socket.gethostbyname(socket.gethostname())))

    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')
    try:
        download_q = multiprocessing.Queue()
        rgb_q = multiprocessing.Queue()
        p1 = multiprocessing.Process(target=get_frame,
                                     args=(connection, download_q))
        p2 = multiprocessing.Process(target=jpg_to_rgb,
                                     args=(screen_size, download_q, rgb_q))
        p3 = multiprocessing.Process(target=blit_bytes,
                                     args=(screen, rgb_q))
        p1.start()
        p2.start()
        p3.start()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
    finally:
        connection.close()
        server_socket.close()
