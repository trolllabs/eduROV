#!/usr/bin/env python3
import socket
import platform
import struct
import time
if platform.system() == 'Linux':
    import picamera
from classes import SplitFrames, ROVManager


def read_camera(host, port, resolution):
    client_socket = socket.socket()
    client_socket.connect((host, port))
    print('Client has been assigned socket name', client_socket.getsockname())
    connection = client_socket.makefile('wb')
    try:
        output = SplitFrames(connection)
        with picamera.PiCamera(resolution=resolution, framerate=30) as camera:
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


def start_camera(server_ip, port_cam, port_var):
    pass


def rov_main(server_ip, port_cam, port_var):
    print('rov main')