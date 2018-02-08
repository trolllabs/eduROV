from multiprocessing.managers import BaseManager


class ROVManager(BaseManager):
    def __init__(self, role, address='0.0.0.0', port=5050, authkey=b'abc'):
        if role not in ['server', 'client']:
            raise ValueError("""role has to be 'server' or 'client'""")
        if role == 'client' and address == '0.0.0.0':
            raise ValueError('A client can not connect to all ports')

        super(ROVManager, self).__init__(address=(address, port),
                                         authkey=authkey)
        if role is 'server':
            self.sensor_values = {'exit': False}
            self.register('sensor_values', callable=lambda:self.sensor_values)
            server = self.get_server()
            server.serve_forever()
        elif role is 'client':
            self.register('sensor_values')
            self.connect()