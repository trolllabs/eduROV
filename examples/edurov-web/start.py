"""
Starts the edurov-web version.
"""

from edurov import WebMethod, KeyConnection, RovConnection
from edurov.arduino import get_serial_connection

def arduino():
    pass

def senser():
    pass

def main(video_resolution='1024x768', fps=30, server_port=8000, debug=False):
    web_method = WebMethod(
        video_resolution=video_resolution,
        fps=fps,
        server_port=server_port,
        debug=debug,
        runtime_functions = [arduino, senser]
    )
    web_method.serve_forever()

if __name__ == '__main__':
    main()