import Pyro4
import subprocess


@Pyro4.expose
class ROVServer:
    def __init__(self):
        self.ns_process = subprocess.Popen('python -m Pyro4.naming',
                                            shell=False)
        self.daemon = Pyro4.Daemon()
        ns = Pyro4.locateNS()
        uri = self.daemon.register(self, objectId='ROVServer')
        ns.register("ROVServer", uri)

    def echo(self, msg):
        return 'Server repsonds: {}'.format(msg)

    @Pyro4.oneway
    def shutdown(self):
        print('shutting down...')
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
