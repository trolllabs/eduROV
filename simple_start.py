import Pyro4

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

if __name__ == "__main__":
    keys = KeyManager()

    with Pyro4.Daemon() as daemon:
        uri = daemon.register(keys)
        with Pyro4.locateNS() as ns:
            ns.register("KeyManager", uri)
        daemon.requestLoop()