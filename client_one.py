import Pyro4

def client_one():
    with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
        print(keys.value)
        keys.value = 20
        print(keys.value)


if __name__ == '__main__':
    client_one()