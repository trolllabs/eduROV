import struct
import io
from multiprocessing.managers import BaseManager


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


class ROVManager(BaseManager):
    def __init__(self, role, address, port, authkey=b'abc'):
        if role not in ['server', 'client']:
            raise ValueError("""role has to be 'server' or 'client'""")
        if role == 'client' and address == '0.0.0.0':
            raise ValueError('A client can not connect to all ports')
        super(ROVManager, self).__init__(address=(address, port),
                                         authkey=authkey)
        if role is 'server':
            self.register_vars_server()
            server = self.get_server()
            server.serve_forever()
        elif role is 'client':
            self.register_vars_client()
            self.connect()

    def register_vars_server(self):
        self.sensor = {}
        self.control = {}
        self.settings = {}
        self.system = {'shutdown': False, 'camera_online': False}

        self.register('sensor', callable=lambda: self.sensor)
        self.register('control', callable=lambda: self.control)
        self.register('settings', callable=lambda: self.settings)
        self.register('system', callable=lambda: self.system)

    def register_vars_client(self):
        self.register('sensor')
        self.register('control')
        self.register('settings')
        self.register('system')
