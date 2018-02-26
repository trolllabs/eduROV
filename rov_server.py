import Pyro4
import subprocess
import time
import pygame


@Pyro4.expose
class Key(object):
    def __init__(self, KeyASCII, ASCII, common, keycode):
        self.value = False
        self.KeyASCII = KeyASCII
        self.ASCII = ASCII
        self.common = common
        if keycode:
            self.keycode = int(keycode)
        else:
            self.keycode = None
        self._mode = 'hold'

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode

    def __str__(self):
        return str(vars(self))

    def set(self, value):
        if value:
            self.value = True
        else:
            self.value = False

    def keydown(self):
        self.value = True

    def keyup(self):
        self.value = False


@Pyro4.expose
class KeyManager(object):
    def __init__(self):
        self.keys = []
        with open('keys.txt', 'r') as f:
            for line in f.readlines()[1:]:
                KeyASCII=line[0:14].rstrip()
                ASCII=line[14:22].rstrip()
                common=line[22:44].rstrip()
                keycode=line[44:].rstrip()
                self.keys.append(Key(KeyASCII, ASCII, common, keycode))

    def set(self, key, value):
        key = self.lookup(key)
        key.set(value)

    def set_from_pygame_event(self, event):
        for key in self.keys:
            if event.key == pygame.__getattribute__(key.KeyASCII):
                if event.type == event.type == pygame.KEYDOWN:
                    key.keydown()
                elif event.type == event.type == pygame.KEYUP:
                    key.keyup()
                return

    def lookup(self, key):
        if isinstance(key, str):
            for _key in self.keys:
                if _key.common == key:
                    return _key
        elif isinstance(key, int):
            for _key in self.keys:
                if _key.keycode == key:
                    return _key
        raise ValueError('Could not find key {}'.format(key))

    def display(self, key):
        print(self.lookup(key))

    def get(self, key):
        return self.lookup(key).value

    def set_mode(self, key, mode):
        self.lookup(key).mode = mode

    def mode(self, key):
        return self.lookup(key).mode


@Pyro4.expose
class ROVSyncer(object):
    def __init__(self):
        self._sensor = {'temp': 0.0,
                        'pressure': 0.0,
                        'time': time.time()}
        self._keys = KeyManager()
        print('Created syncer')

    @property
    def keys(self):
        return self._keys

    @property
    def sensor(self):
        return self._sensor

    @sensor.setter
    def sensor(self, values):
        self._sensor.update(values)
        self._sensor['time'] = time.time()


@Pyro4.expose
class ROVServer(ROVSyncer):
    def __init__(self):
        self.ns_process = subprocess.Popen('pyro4-ns', shell=False)
        self.daemon = Pyro4.Daemon()
        uri = self.daemon.register(self)
        with Pyro4.locateNS() as name_server:
            name_server.register("ROVServer", uri)
        super(ROVServer, self).__init__()

    @Pyro4.oneway
    def shutdown(self):
        print('Shutting down the ROVServer')
        self.__exit__(True, True, True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ns_process.terminate()
        self.ns_process.wait()
        self.daemon.shutdown()
        self.daemon.close()

    def serve(self):
        self.daemon.requestLoop()


if __name__ == '__main__':
    # with ROVServer() as server:
    #     server.serve()
    keys = KeyManager()
    keys.display(87)
    keys.set(87, True)
    keys.display(87)
    keys.set_mode('q', 'toggle')
    print(keys.mode('q'))