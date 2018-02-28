import multiprocessing
import time
from client_one import client_one
from variable_server import start_variable_server

if __name__ == '__main__':
    server = multiprocessing.Process(target=start_variable_server)
    server.start()
    time.sleep(5)

    client1 = multiprocessing.Process(target=client_one)
    client1.start()
