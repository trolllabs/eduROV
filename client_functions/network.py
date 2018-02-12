#!/usr/bin/env python3
import socket
import platform
import io
import struct
import time
if platform.system() == 'Linux':
    import picamera


class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; send the old one's length then the data
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)


def client(host, port, resolution):
    client_socket = socket.socket()
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect((host, port))
    print('Client has been assigned socket name', client_socket.getsockname())
    connection = client_socket.makefile('wb')
    try:
        output = SplitFrames(connection)
        with picamera.PiCamera(resolution=resolution, framerate=30) as camera:
            time.sleep(2)
            start = time.time()
            try:
                camera.start_recording(output, format='mjpeg')
                while True:
                    pass
            except KeyboardInterrupt:
                print('Shutting down client')
            finally:
                camera.stop_recording()

    finally:
        connection.write(struct.pack('<L', 0))  # Tell server we are done
        connection.close()
        client_socket.close()
        finish = time.time()
    print('Sent %d images in %d seconds at %.2ffps' % (
        output.count, finish - start, output.count / (finish - start)))
