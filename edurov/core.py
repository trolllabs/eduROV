import os
import subprocess
import time
from multiprocessing import Process

from edurov.sync import start_sync_classes
from edurov.utils import warning, preexec_function, detect_pi
from edurov.web import start_http_server

if detect_pi():
    import Pyro4

class WebMethod(object):
    """
    Starts a video streaming from the rasparry pi and a webserver that can
    handle user input and other requests.

    Parameters
    ----------
    index_file : str
        Absolute path to the frontpage of the webpage, must be called
        ``index.html``. For more information, see
        :ref:`Displaying-the-video-feed`.
    video_resolution : str, optional
        A string representation of the wanted video resolution in the format
        WIDTHxHEIGHT.
    fps : int, optional
        Wanted framerate, may not be achieved depending on available resources
        and network.
    server_port : int, optional
        The web page will be served at this port
    debug : bool, optional
        If set True, additional information will be printed for debug
        purposes.
    runtime_functions : callable or list, optional
        Should be a callable function or a list of callable functions, will be
        started as independent processes automatically. For more information,
        see :ref:`Controlling-motors-(or-anything)`.
    custom_response : callable, optional
        If set, this function will be called if default web server is not able
        to handle a GET request, should return a str or None. If returned value
        starts with ``redirect=`` followed by a path, the server will redirect
        the browser to this path. The callable must accept two parameters
        whereas the second one is the requested path. For more information, see
        :ref:`Custom-Responses`.

    Examples
    --------
    >>> import os
    >>> from edurov import WebMethod
    >>>
    >>> file = os.path.join(os.path.dirname(__file__), 'index.html', )
    >>> web_method = WebMethod(index_file=file)
    >>> web_method.serve()
    """
    def __init__(self, index_file, video_resolution='1024x768', fps=30,
                 server_port=8000, debug=False, runtime_functions=None,
                 custom_response=None):

        self.res = video_resolution
        self.fps = fps
        self.server_port = server_port
        self.debug = debug
        self.run_funcs = self._valid_runtime_functions(runtime_functions)
        self.cust_resp = self._valid_custom_response(custom_response)
        self.index_file = self._valid_index_file(index_file)

    def _valid_custom_response(self, custom_response):
        if custom_response:
            if not callable(custom_response):
                warning('custom_response parameter has to be a callable '
                        'function, not type {}'.format(type(custom_response)))
                return None
        return custom_response

    def _valid_runtime_functions(self, runtime_functions):
        if runtime_functions:
            if callable(runtime_functions):
                runtime_functions = [runtime_functions]
            elif isinstance(runtime_functions, list):
                for f in runtime_functions:
                    if not callable(f):
                        warning(
                            'Parameter runtime_functions has to be a function '
                            'or a list of functions, not {}'.format(type(f)))
            else:
                warning('Parameter runtime_functions has to be a function '
                        'or a list of functions, not {}'
                        .format(type(runtime_functions)))
        return runtime_functions

    def _valid_index_file(self, file_path):
        if not 'index.html' in file_path:
            warning('The index files must be called "index.html')
        if os.path.isfile(file_path):
            return os.path.abspath(file_path)
        else:
            warning('Could not find "{}", needs absolute path'
                    .format(file_path))
        return None

    def serve(self, timeout=None):
        """
        Will start serving the web page defined by the index_file parameter

        Parameters
        ----------
        timeout : int, optional
            if set, the web page will only be served for that many seconds
            before it automatically shuts down

        Notes
        -----
        This method will block the rest of the script.
        """
        start = time.time()
        name_server = subprocess.Popen('pyro4-ns', shell=False,
                                       preexec_fn=preexec_function)
        time.sleep(2)
        pyro_classes = Process(target=start_sync_classes)
        pyro_classes.start()
        time.sleep(4)
        web_server = Process(
            target=start_http_server,
            args=(self.res, self.fps, self.server_port, self.index_file,
                  self.debug, self.cust_resp))
        web_server.daemon = True
        web_server.start()
        processes = []
        if self.run_funcs:
            for f in self.run_funcs:
                p = Process(target=f)
                p.daemon = True
                p.start()
                processes.append(p)

        with Pyro4.Proxy("PYRONAME:ROVSyncer") as rov:
            try:
                while rov.run:
                    if timeout:
                        if time.time() - start >= timeout:
                            break
            except KeyboardInterrupt:
                pass
            finally:
                print('Shutting down')
                web_server.terminate()
                rov.run = False
                if self.run_funcs:
                    for p in processes:
                        p.join(3)
                pyro_classes.terminate()
                name_server.terminate()
