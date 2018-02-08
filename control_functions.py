import multiprocessing as mp
from multiprocessing.pool import ThreadPool
import sys
import io
import struct
import socket
import time
import pygame
from PIL import Image
from classes import ROVManager

BLACK = 0,0,0


def get_camera_connection(server_socket):
    print('Waiting for camera feed...')
    connection = server_socket.accept()[0].makefile('rb')
    print('Camera connected')
    return connection


def get_camera(server_ip, port_var, port_cam, resolution, fullscreen):
    mgr = ROVManager(role='client', address='127.0.0.1', port=port_var)
    pygame.init()
    pygame.display.set_caption('eduROV')
    screen_size = tuple([int(val) for val in resolution.split('x')])
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((server_ip, port_cam))
    server_socket.listen(0)

    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(get_camera_connection, (server_socket,))

    try:
        while not mgr.system().get('shutdown'):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mgr.system().update({'shutdown': True})
                    sys.exit()
            try:
                status = async_result.successful()
                connection = async_result.get()
                mgr.system().update({'camera_online':True})
            except AssertionError:
                continue

            if mgr.system().get('camera_online'):
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
                # Rewind byte stream
                image_stream.seek(0)
                screen.blit(frame, (0,0))
            else:
                screen.fill(BLACK)
            pygame.display.flip()
            pygame.display.update()
    finally:
        if mgr.system().get('camera_online'):
            connection.close()
        server_socket.close()


def start_server(server_ip, port_var):
    print('ROV should connect to {}'
          .format(socket.gethostbyname(socket.gethostname())))
    ROVManager(role='server', address=server_ip, port=port_var)


def control_main(server_ip, port_cam, port_var, camera_resolution, fullscreen):
    server = mp.Process(target=start_server,
                        args=(server_ip, port_var))
    camera_feed = mp.Process(target=get_camera,
                             args=(server_ip, port_var, port_cam,
                                   camera_resolution, fullscreen))
    server.start()
    time.sleep(2)
    camera_feed.start()

    mgr = ROVManager(role='client', address='127.0.0.1', port=port_var)

    try:
        while not mgr.system().get('shutdown'):
            time.sleep(0.1)
    except KeyboardInterrupt:
        mgr.system().update({'shutdown':True})
        print('User aborted operation')
    finally:
        print('Shutting down server')
        time.sleep(1)
        server.terminate()
