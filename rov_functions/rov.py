#!/usr/bin/env python3
import socket
import platform
import io
import sys
import struct
import time
if platform.system() == 'Linux':
    import picamera
    class Camera(picamera.PiCamera):
        def __init__(self, resolution, framerate=30):
            super(Camera, self).__init__(resolution=resolution,
                                         framerate=framerate)
            time.sleep(2)

        def stop(self):
            self.__exit__(True, True, True)
        #
        # def __enter__(self):
        #     return self
        #
        # def __exit__(self, exc_type, exc_val, exc_tb):
        #     super(Camera, self).__exit__(exc_type, exc_val, exc_tb)
        #     self.stop_recording()


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

    def stop(self):
        self.__exit__(True, True, True)

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
        with Camera(resolution) as camera:
            camera.start_recording(output, format='mjpeg')
            camera.wait_recording(0)
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                camera.stop()
                client.stop()
