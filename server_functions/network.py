import struct
import io
import sys
import socket
import pygame
from PIL import Image


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
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = \
                struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Read image data and convert: BytesIO > PIL.Image > pygame.image
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            PILframe = Image.open(image_stream).tobytes()
            frame = pygame.image.fromstring(PILframe, screen_size, 'RGB')
            # Update screen
            screen.blit(frame, (0,0))
            pygame.display.flip()
            # Rewind byte stream
            image_stream.seek(0)
    finally:
        connection.close()
        server_socket.close()
