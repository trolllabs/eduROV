import subprocess
import multiprocessing
import time
from simple_start import start
from client_one import client_one

if __name__ == '__main__':
    # subprocess.Popen(['python', 'simple_start.py'], shell=False)
    server = multiprocessing.Process(target=start)
    server.start()
    time.sleep(5)
    client1 = multiprocessing.Process(target=client_one)
    client1.start()
