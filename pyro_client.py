import Pyro4


if __name__ == '__main__':
    # with Pyro4.Proxy("PYRONAME:ROVServer") as rov:
    #     rov.shutdown()
    with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
        print(keys.state('r'))
        keys.keydown('r')
        print(keys.state('r'))
        keys.keyup('r')
        print(keys.state('r'))