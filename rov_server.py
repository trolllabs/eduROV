from .rov_classes import ROVServer


if __name__ == '__main__':
    with ROVServer() as server:
        server.serve()
