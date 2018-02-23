import Pyro4
import random
import time


if __name__ == '__main__':
    with Pyro4.Proxy("PYRONAME:ROVServer") as rov:
        try:
            while True:
                rov.sensor = {'temp': random.randrange(10)}
                print(rov.sensor)
                time.sleep(0.1)
        finally:
            rov.shutdown()
