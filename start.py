import multiprocessing
import subprocess
import Pyro4
import time
from client_one import client_one
from variable_server import start_variable_server

if __name__ == '__main__':
    name_server = subprocess.Popen('pyro4-ns', shell=False)
    var_server = multiprocessing.Process(target=start_variable_server)
    var_server.start()
    time.sleep(5)

    client1 = multiprocessing.Process(target=client_one)
    client1.start()
    with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
        try:
            while rov.run:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print('Shutting down')
        finally:
            rov.run = False
            client1.join()
            var_server.terminate()
            name_server.terminate()
            name_server.wait()
