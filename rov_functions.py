#!/usr/bin/env python3
import multiprocessing as mp
import datetime as dt
import random
import socket
import sys
import platform
import struct
import time
if platform.system() == 'Linux':
    import picamera
from classes import SplitFrames, ROVManager


def read_camera(host, port, resolution, framerate):
    client_socket = socket.socket()
    client_socket.connect((host, port))
    connection = client_socket.makefile('wb')
    try:
        output = SplitFrames(connection)
        with picamera.PiCamera(resolution=resolution, framerate=framerate) as camera:
            time.sleep(2)
            start = time.time()
            camera.start_recording(output, format='mjpeg')
            camera.wait_recording(60)
            camera.stop_recording()
            connection.write(struct.pack('<L', 0))  # Tell server we are done
    finally:
        connection.close()
        client_socket.close()
        finish = time.time()
    print('Sent %d images in %d seconds at %.2ffps' % (
        output.count, finish - start, output.count / (finish - start)))


def read_sensors(server_ip, port_var):
    mgr = ROVManager(role='client', address=server_ip, port=port_var)
    sensor = mgr.sensor()

    while not mgr.system().get('shutdown'):
        sensor.update({'time': dt.datetime.now().isoformat(),
                       'voltage': random.randrange(5.0,11.0)})
        time.sleep(0.05)


def start_camera(server_ip, port_cam, port_var):
    mgr = ROVManager(role='client', address=server_ip, port=port_var)
    cam_resolution = mgr.settings().get('camera_resolution')
    cam_framerate = mgr.settings().get('framerate')
    camera_sender = mp.Process(
        target=read_camera,
        args=(server_ip, port_cam, cam_resolution, cam_framerate))
    camera_sender.start()


def connect_to_control(server_ip, port_var):
    connected = False
    print('Connecting to {}'.format(server_ip))
    while not connected:
        try:
            mgr = ROVManager(role='client', address=server_ip, port=port_var)
            return mgr
        except ConnectionRefusedError:
            continue
        except KeyboardInterrupt:
            print('User aborted operation')
            sys.exit()


def rov_main(server_ip, port_cam, port_var):
    mgr = connect_to_control(server_ip, port_var)
    print('Connected to control')
    time.sleep(1)
    camera = mp.Process(target=start_camera,
                        args=(server_ip, port_cam, port_var))
    sensor = mp.Process(target=read_sensors,
                        args=(server_ip, port_var))
    # camera.start()
    sensor.start()

    try:
        while not mgr.system().get('shutdown'):
            time.sleep(0.1)
    except KeyboardInterrupt:
        mgr.system().update({'shutdown': True})
        print('User aborted operation')
