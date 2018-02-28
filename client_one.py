import Pyro4
import time


if __name__ == '__main__':
    with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
        time.sleep(2)
        print('one ' + str(keys.state('r')))
        keys.set('r', True)
        print('one ' + str(keys.state('r')))