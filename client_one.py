import Pyro4
import time
import signal

def client_one():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
        with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
            while rov.run:
                print(keys.state('w'))
                keys.set('w', True)
                print(keys.state('w'))
                time.sleep(2)
    print('client 1 finished')


if __name__ == '__main__':
    client_one()