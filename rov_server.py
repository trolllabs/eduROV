import Pyro4
import subprocess
import time

@Pyro4.expose
class ROVSyncer(object):
    def __init__(self):
        print('Created syncer')
        self._sensor = {'temp': 45.7, 'time': time.time()}

    @property
    def sensor(self):
        return self._sensor

    @sensor.setter
    def sensor(self, values):
        self._sensor.update(values)
        self._sensor['time'] = time.time()

    def echo(self, msg):
        return 'Server responds: {}'.format(msg)


@Pyro4.expose
class ROVServer(ROVSyncer):
    def __init__(self):
        self.ns_process = subprocess.Popen(
            'python -m Pyro4.naming',
            shell=False)
        self.daemon = Pyro4.Daemon()
        uri = self.daemon.register(self)
        with Pyro4.locateNS() as nameserver:
            nameserver.register("ROVServer", uri)
        super(ROVServer, self).__init__()

    @Pyro4.oneway
    def shutdown(self):
        print('Shutting down the ROVServer')
        self.__exit__(True, True, True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ns_process.terminate()
        self.ns_process.wait()
        self.daemon.shutdown()
        self.daemon.close()

    def serve(self):
        self.daemon.requestLoop()


if __name__ == '__main__':

    with ROVServer() as server:
        server.serve()
