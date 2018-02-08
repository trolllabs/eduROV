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
from helpers import output

BLACK = 0, 0, 0


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
                async_result.successful()
                connection = async_result.get()
                mgr.system().update({'camera_online': True})
            except AssertionError:
                continue

            if mgr.system().get('camera_online') is True:
                try:
                    # Read the length of the image as a 32-bit unsigned int.
                    # If the length is zero, quit the loop
                    image_len = struct.unpack(
                        '<L', connection.read(struct.calcsize('<L')))[0]
                    if not image_len:
                        break
                    # Read image data and convert:
                    # BytesIO > PIL.Image > pygame.image
                    image_stream = io.BytesIO()
                    image_stream.write(connection.read(image_len))
                    PILframe = Image.open(image_stream).tobytes()
                    frame = pygame.image.fromstring(PILframe,
                                                    screen_size,
                                                    'RGB')
                    screen.blit(frame, (0, 0))
                    # Rewind byte stream
                    image_stream.seek(0)
                except struct.error:
                    print('Problem reading data from camera')
                    mgr.system().update({'shutdown': True})
                    break
            else:
                screen.fill(BLACK)
            pygame.display.flip()
            pygame.display.update()
    finally:
        if mgr.system().get('camera_online'):
            connection.close()
        else:
            pool.terminate()
        server_socket.close()

def view_sensors(port_var):
    mgr = ROVManager(role='client', address='127.0.0.1', port=port_var)
    while not mgr.system().get('shutdown'):
        output(mgr.sensor())
        time.sleep(0.1)


def start_server(server_ip, port_var):
    print('ROV should connect to {}'
          .format(socket.gethostbyname(socket.gethostname())))
    ROVManager(role='server', address=server_ip, port=port_var)


def update_settings(mgr, camera_resolution, fullscreen, framerate):
    mgr.settings().update({'camera_resolution': camera_resolution,
                           'fullscreen': fullscreen,
                           'framerate': framerate})


def control_main(server_ip, port_cam, port_var, camera_resolution, fullscreen,
                 framerate):
    server = mp.Process(
        target=start_server,
        args=(server_ip, port_var))
    camera_receiver = mp.Process(
        target=get_camera,
        args=(server_ip, port_var, port_cam, camera_resolution, fullscreen))
    sensor_output = mp.Process(
        target=view_sensors,
        args=(port_var,))
    server.start()
    # camera_receiver.start()
    sensor_output.start()

    mgr = ROVManager(role='client', address='127.0.0.1', port=port_var)
    update_settings(mgr, camera_resolution, fullscreen, framerate)

    try:
        while not mgr.system().get('shutdown'):
            time.sleep(0.1)
    except KeyboardInterrupt:
        mgr.system().update({'shutdown': True})
        print('User aborted operation')
    finally:
        print('Shutting down server')
        time.sleep(1)
        server.terminate()
