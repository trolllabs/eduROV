import multiprocessing
import subprocess
import Pyro4
import time
from client_one import client_one, client_two
from pyro_classes import start_pyro_classes

if __name__ == '__main__':
    name_server = subprocess.Popen('pyro4-ns', shell=False)
    pyro_classes = multiprocessing.Process(target=start_pyro_classes)
    pyro_classes.start()
    time.sleep(5)

    client1 = multiprocessing.Process(target=client_one)
    client2 = multiprocessing.Process(target=client_two)
    clients = [client1, client2]
    for cli in clients:
        cli.start()
    with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
        try:
            while rov.run:
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass
        finally:
            print('Shutting down')
            rov.run = False
            for cli in clients:
                cli.join()
            pyro_classes.terminate()
            name_server.terminate()
            name_server.wait()
