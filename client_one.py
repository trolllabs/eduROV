import Pyro4


if __name__ == '__main__':
    with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
        print(keys.value)
        keys.value = 20
        print(keys.value)