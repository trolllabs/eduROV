import subprocess
import time

if __name__ == '__main__':
    subprocess.Popen(['python', 'rov_server.py'], shell=False)
    time.sleep(5)
    subprocess.Popen(['python', 'client_one.py'], shell=False)
    subprocess.Popen(['python', 'client_two.py'], shell=False)
    time.sleep(10)
