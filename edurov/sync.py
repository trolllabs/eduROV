"""
Synchronizing the state of ROV and controller
"""

import os
import time

import Pyro4


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
        if self.mode == 'toggle':
            self.state = not self.state
        else:
            self.state = True

    def keyup(self):
        if self.mode != 'toggle':
            self.state = False

    def __str__(self):
        return str(vars(self))


@Pyro4.expose
class KeyManager(object):
    """Keeps control of all user input from keyboard"""

    def __init__(self):
        self.keys = {}
        cwd = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(cwd, 'keys.txt'), 'r') as f:
            for line in f.readlines()[1:]:
                KeyASCII = line[0:14].rstrip()
                ASCII = line[14:22].rstrip()
                common = line[22:44].rstrip()
                keycode = line[44:].rstrip()
                if keycode:
                    dict_key = int(keycode)
                else:
                    dict_key = KeyASCII
                self.keys.update({
                    dict_key: Key(KeyASCII, ASCII, common, keycode)})

    def set_mode(self, key, mode):
        self.get(key).mode = mode

    def set(self, key, state):
        self.get(key).state = state

    def get(self, key_idx, make_exception=True):
        key = self.keys[key_idx]
        if key:
            return key
        elif isinstance(key_idx, str):
            for dict_key in self.keys:
                if key_idx in [self.keys[dict_key].common,
                               self.keys[dict_key].KeyASCII]:
                    return self.keys[dict_key]
        if make_exception:
            raise ValueError('Could not find key {}'.format(key_idx))
        else:
            return None

    def state(self, key):
        return self.get(key).state

    def keydown(self, key, make_exception=False):
        btn = self.get(key, make_exception=make_exception)
        if btn:
            btn.keydown()

    def keyup(self, key, make_exception=False):
        btn = self.get(key, make_exception=make_exception)
        if btn:
            btn.keyup()

    @property
    def qweasd_dict(self):
        state = {
            'q': self.get(81).state,
            'w': self.get(87).state,
            'e': self.get(69).state,
            'a': self.get(65).state,
            's': self.get(83).state,
            'd': self.get(68).state,
        }
        return state

    @property
    def arrow_dict(self):
        state = {
            'up arrow': self.get(38).state,
            'down arrow': self.get(40).state,
            'left arrow': self.get(37).state,
            'right arrow': self.get(39).state,
        }
        return state


@Pyro4.expose
class ROVSyncer(object):
    """Holds all variables for ROV related to control and sensors"""

    def __init__(self):
        self._sensor = {'time': time.time()}
        self._actuator = {}
        self._run = True

    @property
    def sensor(self):
        return self._sensor

    @sensor.setter
    def sensor(self, values):
        self._sensor.update(values)
        self._sensor['time'] = time.time()

    @property
    def actuator(self):
        return self._actuator

    @actuator.setter
    def actuator(self, values):
        self._actuator.update(values)
        self._actuator['time'] = time.time()

    @property
    def run(self):
        return self._run

    @run.setter
    def run(self, bool_):
        self._run = bool_


def start_sync_classes():
    """Registers pyro classes in name server and starts request loop"""
    rov = ROVSyncer()
    keys = KeyManager()
    with Pyro4.Daemon() as daemon:
        rov_uri = daemon.register(rov)
        keys_uri = daemon.register(keys)
        with Pyro4.locateNS() as ns:
            ns.register("ROVSyncer", rov_uri)
            ns.register("KeyManager", keys_uri)
        daemon.requestLoop()


if __name__ == "__main__":
    start_sync_classes()
