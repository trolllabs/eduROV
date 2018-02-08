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

        self.shared_dicts = ['sensor', 'control', 'settings', 'system']
        # IMPORTANT! 'system' must be the last list item

        if role is 'server':
            self.register_vars_server()
            server = self.get_server()
            server.serve_forever()
        elif role is 'client':
            self.register_vars_client()
            self.connect()
            print('Client connected successfully')

    def register_vars_server(self):
        for d in self.shared_dicts:
            self.__setattr__(d, {})
            self.register(d, callable=lambda: self.__getattribute__(d))
        self.system.update({'shutdown': False})

    def register_vars_client(self):
        for d in self.shared_dicts:
            self.register(d)
