import Pyro4
import time


if __name__ == '__main__':
    with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
        print('two ' + str(keys.state('r')))
        time.sleep(5)
        print('two ' + str(keys.state('r')))