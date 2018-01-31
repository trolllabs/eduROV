import struct
import io
import sys
import socket
import pygame
from PIL import Image


def server(interface, port, resolution, fullscreen):
    pygame.init()
    screen_size = tuple([int(val) for val in resolution.split('x')])
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
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it

            data = Image.open(image_stream).tobytes()
            snapshot = pygame.image.fromstring(data, screen_size, 'RGB')
            screen.blit(snapshot, (0,0))
            pygame.display.flip()
            image_stream.seek(0)
    finally:
        connection.close()
        server_socket.close()
