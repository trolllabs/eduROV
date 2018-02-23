import subprocess
import time

# completed = subprocess.run('python -m Pyro4.naming', shell=False)
# print('returncode:', completed.returncode)

nsProcess = subprocess.Popen('python -m Pyro4.naming', shell=False)
time.sleep(3)
print('i am now doing my shit here')
time.sleep(3)
nsProcess.terminate()
nsProcess.wait()