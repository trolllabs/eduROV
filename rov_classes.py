import subprocess
import time

import Pyro4
import pygame


class Key(object):
    """Manages the state of a specific key on the keyboard"""

    def __init__(self, KeyASCII, ASCII, common, keycode, mode='hold'):
        self.state = False
        self.KeyASCII = KeyASCII
        self.ASCII = ASCII
        self.common = common
        self.mode = mode
        if keycode:
            self.keycode = int(keycode)
        else:
            self.keycode = None

    def keydown(self):
        print('{} keydown'.format(self.common))
        if self.mode == 'toggle':
            self.state = not self.state
        else:
            self.state = True

    def keyup(self):
        print('{} keyup'.format(self.common))
        if self.mode != 'toggle':
            self.state = False

    def __str__(self):
        return str(vars(self))


@Pyro4.expose
class KeyManager(object):
    """Keeps control of all user input from keyboard"""

    def __init__(self):
        self.keys = []
        with open('keys.txt', 'r') as f:
            for line in f.readlines()[1:]:
                KeyASCII = line[0:14].rstrip()
                ASCII = line[14:22].rstrip()
                common = line[22:44].rstrip()
                keycode = line[44:].rstrip()
                self.keys.append(Key(KeyASCII, ASCII, common, keycode))

    def set(self, key, state):
        self.get(key).state = state

    def set_from_pygame_event(self, event):
        for key in self.keys:
            if event.key == pygame.__getattribute__(key.KeyASCII):
                if event.type == pygame.KEYDOWN:
                    key.keydown()
                elif event.type == pygame.KEYUP:
                    key.keyup()
                return

    def set_from_js_dict(self, js_dict):
        for key in self.keys:
            if key.keycode == js_dict['keycode']:
                if js_dict['event'] == 'KEYDOWN':
                    key.keydown()
                elif js_dict['event'] == 'KEYUP':
                    key.keyup()
                return

    def get(self, key_idx):
        if isinstance(key_idx, str):
            for key in self.keys:
                if key.common == key_idx or key.KeyASCII == key_idx:
                    return key
        elif isinstance(key_idx, int):
            for key in self.keys:
                if key.keycode == key_idx:
                    return key
        raise ValueError('Could not find key {}'.format(key_idx))

    def state(self, key):
        return self.get(key).state

    def keydown(self, key):
        self.get(key).keydown()

    def keyup(self, key):
        self.get(key).keyup()

    def variable(self):
        return 45


class ROVSyncer(object):
    """Holds all variables for ROV related to control and sensors"""

    def __init__(self):
        self._sensor = {'temp': 0.0,
                        'pressure': 0.0,
                        'time': time.time()}

    @property
    def sensor(self):
        return self._sensor

    @sensor.setter
    def sensor(self, values):
        self._sensor.update(values)
        self._sensor['time'] = time.time()


@Pyro4.expose
class ROVServer(ROVSyncer):
    """Extends ROVSyncer such that it can be accessed on multiple machines"""

    def __init__(self):
        self.ns_process = subprocess.Popen('pyro4-ns', shell=False)
        self.daemon = Pyro4.Daemon()
        rov_server_uri = self.daemon.register(self)
        key_manager_uri = self.daemon.register(KeyManager)
        with Pyro4.locateNS() as name_server:
            name_server.register("ROVServer", rov_server_uri)
            name_server.register("KeyManager", key_manager_uri)
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


def start_variable_server():
    with ROVServer() as server:
        server.serve()
