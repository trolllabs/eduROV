import subprocess
import time
from multiprocessing import Process

import Pyro4

from edurov.sync import start_sync_classes
from edurov.utils import warning, preexec_function
from edurov.web.servers import start_http_server


class WebMethod(object):
    def __init__(self, video_resolution='1024x768', fps=30, server_port=8000,
                 debug=False, runtime_functions=None, index_file=None):
        if callable(runtime_functions):
            runtime_functions = [runtime_functions]
        elif isinstance(runtime_functions, list):
            for f in runtime_functions:
                if not callable(f):
                    warning('Parameter runtime_functions has to be a function '
                            'or a list of functions, not {}'.format(type(f)))
        else:
            warning('Parameter runtime_functions has to be a function '
                    'or a list of functions, not {}'
                    .format(type(runtime_functions)))

        self.res = video_resolution
        self.fps = fps
        self.server_port = server_port
        self.debug = debug
        self.run_funcs = runtime_functions
        if index_file:
            self.index_file = index_file
        else:
            self.index_file = 'index.html'

    def serve(self, timeout=None):
        start = time.time()
        name_server = subprocess.Popen('pyro4-ns', shell=False,
                                       preexec_fn=preexec_function)
        time.sleep(2)
        pyro_classes = Process(target=start_sync_classes)
        pyro_classes.start()
        time.sleep(4)
        web_server = Process(
            target=start_http_server,
            args=(self.res, self.fps, self.server_port, self.debug,
                  self.index_file))
        web_server.start()
        processes = []
        for f in self.run_funcs:
            p = Process(target=f)
            p.start()
            processes.append(p)

        with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
            try:
                while rov.run:
                    if timeout:
                        if time.time()-start >= timeout:
                            break
            except KeyboardInterrupt:
                pass
            finally:
                print('Shutting down')
                web_server.terminate()
                rov.run = False
                for p in processes:
                    p.join(3)
                pyro_classes.terminate()
                name_server.terminate()


class KeyConnection(object):
    def __init__(self):
        pass


class RovConnection(object):
    def __init__(self):
        pass
