import subprocess
import multiprocessing
from simple_start import start
from client_one import client_one

if __name__ == '__main__':
    # subprocess.Popen(['python', 'simple_start.py'], shell=False)
    server = multiprocessing.Process(target=start)
    client1 = multiprocessing.Process(target=client_one)
    processes = [server, client1]
    for p in processes:
        p.start()
