import Pyro4

@Pyro4.expose
class ROVServer:
    def __init__(self):
        self.daemon = Pyro4.Daemon(port=9999)
        self.uri = self.daemon.register(self, objectId='ROVServer')

    def hello(self, msg):
        print('client said {}'.format(msg))
        return 'hola'

    @Pyro4.oneway
    def shutdown(self):
        print('shutting down...')
        self.__exit__(True, True, True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.daemon.shutdown()
        self.daemon.close()

    def serve(self):
        self.daemon.requestLoop()

if __name__ == '__main__':

    with ROVServer() as server:
        server.serve()