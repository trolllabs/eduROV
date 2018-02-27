import Pyro4
import subprocess
import time
import pygame


@Pyro4.expose
class Key(object):
    """Manages the state of a specific key on the keyboard"""
    def __init__(self, KeyASCII, ASCII, common, keycode, mode='hold'):
        self._state = 'what'
        self._KeyASCII = KeyASCII
        self._ASCII = ASCII
        self._common = common
        if keycode:
            self._keycode = int(keycode)
        else:
            self._keycode = None
        self._mode = self._valid_mode(mode)

    @property
    def keycode(self):
        return self._keycode

    @property
    def KeyASCII(self):
        return self._KeyASCII

    @property
    def ASCII(self):
        return self._ASCII

    @property
    def common(self):
        return self._common

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def set(self, state):
        self._state = state

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = self._valid_mode(mode)

    def keydown(self):
        if self._mode == 'toggle':
            self._state = not self._state
        else:
            self._state = True

    def keyup(self):
        if self._mode != 'toggle':
            self._state = False

    def _valid_mode(self, mode):
        if mode in ['hold', 'toggle']:
            return mode
        else:
            raise ValueError('Key mode has to be hold or toggle, not {}'
                             .format(mode))

    def __str__(self):
        print_dict = {}
        for key in vars(self):
            print_dict.update({key.lstrip('_'): vars(self)[key]})
        return str(print_dict)


@Pyro4.expose
class KeyManager(object):
    """Keeps control of all user input from keyboard"""
    def __init__(self):
        self._keys = []
        with open('keys.txt', 'r') as f:
            for line in f.readlines()[1:]:
                KeyASCII = line[0:14].rstrip()
                ASCII = line[14:22].rstrip()
                common = line[22:44].rstrip()
                keycode = line[44:].rstrip()
                self._keys.append(Key(KeyASCII, ASCII, common, keycode))

    @property
    def keys(self):
        return self._keys

    def set(self, key, value):
        print('set {} = {}'.format(key, value))
        # self.get(key).state = value
        self.get(key).set(value)

    def set_from_pygame_event(self, event):
        for key in self._keys:
            if event.key == pygame.__getattribute__(key.KeyASCII):
                if event.type == pygame.KEYDOWN:
                    key.keydown()
                elif event.type == pygame.KEYUP:
                    key.keyup()
                return

    def set_from_js_dict(self, js_dict):
        for key in self._keys:
            if key.keycode == js_dict['keycode']:
                if js_dict['event'] == 'KEYDOWN':
                    key.keydown()
                elif js_dict['event'] == 'KEYUP':
                    key.keyup()
                return

    def get(self, key_idx):
        if isinstance(key_idx, str):
            for key in self._keys:
                if key.common == key_idx or key.KeyASCII == key_idx:
                    return key
        elif isinstance(key_idx, int):
            for key in self._keys:
                if key.keycode == key_idx:
                    return key
        raise ValueError('Could not find key {}'.format(key_idx))

    def state(self, key):
        print('state {} = {}'.format(key, self.get(key).state))
        return self.get(key).state


@Pyro4.expose
class ROVSyncer(object):
    """Holds all variables for ROV related to control and sensors"""
    def __init__(self):
        self._sensor = {'temp': 0.0,
                        'pressure': 0.0,
                        'time': time.time()}
        self._keys = KeyManager()

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


if __name__ == '__main__':
    with ROVServer() as server:
        server.serve()
    # rov = ROVSyncer()
    # print(rov.keys.get('w'))
    # rov.keys.get('w').state = True
    # print(rov.keys.get('w'))
