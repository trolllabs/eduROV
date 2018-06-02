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
    """
    Keeps control of all user input from keyboard.

    Examples
    --------
    >>> import Pyro4
    >>>
    >>> with Pyro4.Proxy("PYRONAME:KeyManager") as keys:
    >>> with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
    >>>     keys.set_mode(key='l', mode='toggle')
    >>>     while rov.run:
    >>>         if keys.state('up arrow'):
    >>>             print('You are pressing the up arrow')
    >>>         if keys.state('l'):
    >>>             print('light on')
    >>>         else:
    >>>             print('light off')

    Note
    ----
    When using the methods below a **key identifier** must be used. Either the
    keycode (int) or the KeyASCII or Common Name (str) from the table further
    down on this page can be used. Using keycode is faster.
    """

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
        """
        Set the press mode for the key to *hold* or *toggle*

        Parameters
        ----------
        key : int or str
            key identifier as described above
        mode : str
            *hold* or *toggle*
        """
        self._get(key).mode = mode

    def set(self, key, state):
        """
        Set the state of the key to True or False

        Parameters
        ----------
        key : int or str
            key identifier as described above
        state : bool
            *True* or *False*
        """
        self._get(key).state = bool(state)

    def _get(self, key_idx, make_exception=True):
        """
        Returns the Key object identified by *key_idx*

        Parameters
        ----------
        key_idx : int or str
            key identifier as described above
        make_exception : bool, optional
            As default an exception is raised if the key is not found, this
            behavior can be changed be setting it to *False*

        Returns
        -------
        key : Key object
            list items is *namedtuple* of type *LiItem*
        """
        if key_idx in self.keys:
            return self.keys[key_idx]
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
        """
        Returns the state of *key*

        Parameters
        ----------
        key : int or str
            key identifier as described above

        Returns
        -------
        state : bool
            *True* or *False*
        """
        return self._get(key).state

    def keydown(self, key, make_exception=False):
        """
        Call to simulate a keydown event

        Parameters
        ----------
        key : int or str
            key identifier as described above
        make_exception : bool, optional
            As default an exception is raised if the key is not found, this
            behavior can be changed be setting it to *False*
        """
        btn = self._get(key, make_exception=make_exception)
        if btn:
            btn.keydown()

    def keyup(self, key, make_exception=False):
        """
        Call to simulate a keyup event

        Parameters
        ----------
        key : int or str
            key identifier as described above
        make_exception : bool, optional
            As default an exception is raised if the key is not found, this
            behavior can be changed be setting it to *False*
        """
        btn = self._get(key, make_exception=make_exception)
        if btn:
            btn.keyup()

    @property
    def qweasd_dict(self):
        """
        Dictionary with the state of the letters q, w, e, a, s and d
        """
        state = {
            'q': self._get(81).state,
            'w': self._get(87).state,
            'e': self._get(69).state,
            'a': self._get(65).state,
            's': self._get(83).state,
            'd': self._get(68).state,
        }
        return state

    @property
    def arrow_dict(self):
        """
        Dictionary with the state of the keys *up arrow*, *down arrow*,
        *left arrow* and *right arrow*
        """
        state = {
            'up arrow': self._get(38).state,
            'down arrow': self._get(40).state,
            'left arrow': self._get(37).state,
            'right arrow': self._get(39).state,
        }
        return state


@Pyro4.expose
class ROVSyncer(object):
    """
    Holds all variables for ROV related to control and sensors

    Examples
    --------
    >>> import Pyro4
    >>>
    >>> with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
    >>>   while rov.run:
    >>>       print('The ROV is still running')
    """

    def __init__(self):
        self._sensor = {'time': time.time()}
        self._actuator = {}
        self._run = True

    @property
    def sensor(self):
        """
        Dictionary holding sensor values

        :getter: Returns sensor values as dict
        :setter: Update sensor values with dict
        :type: dict
        """
        return self._sensor

    @sensor.setter
    def sensor(self, values):
        self._sensor.update(values)
        self._sensor['time'] = time.time()

    @property
    def actuator(self):
        """
        Dictionary holding actuator values

        :getter: Returns actuator values as dict
        :setter: Update actuator values with dict
        :type: dict
        """
        return self._actuator

    @actuator.setter
    def actuator(self, values):
        self._actuator.update(values)
        self._actuator['time'] = time.time()

    @property
    def run(self):
        """
        Bool describing if the ROV is still running

        :getter: Returns bool describing if the ROV is running
        :setter: Set to False if the ROV should stop
        :type: bool
        """
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
