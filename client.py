import Pyro4


if __name__ == '__main__':

    rov_server = Pyro4.Proxy("PYRONAME:ROVServer")
    print(rov_server.echo('I am a client'))
    rov_server.shutdown()
    # rov_server._pyroRelease()
