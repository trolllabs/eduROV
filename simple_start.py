import Pyro4
import subprocess

@Pyro4.expose
class KeyManager():
    def __init__(self):
        self._value = 45

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

def start():
    subprocess.Popen('pyro4-ns', shell=False)

    keys = KeyManager()
    with Pyro4.Daemon() as daemon:
        uri = daemon.register(keys)
        with Pyro4.locateNS() as ns:
            ns.register("KeyManager", uri)
        daemon.requestLoop()


if __name__ == "__main__":
    start()