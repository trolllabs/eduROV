import Pyro4

def client_one():
    with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
        print(keys.state('w'))
        keys.set('w', True)
        print(keys.state('w'))


if __name__ == '__main__':
    client_one()