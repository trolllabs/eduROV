"""
Different utility functions
"""

import platform
import socket
import struct
import subprocess
import warnings
warnings.formatwarning = warning_format


def detect_pi():
    if 'Linux' in platform.platform():
        return True
    else:
        return False


if detect_pi():
    import fcntl

STANDARD_RESOLUTIONS = ['160x120', '240x160', '640x360', '640x480', '960x540',
                        '960x640', '1024x576', '1024x600', '1024x768',
                        '1152x864', '1280x720', '1296x972', '1640x1232',
                        '1920x1080']


def valid_resolution(resolution):
    if 'x' in resolution:
        if len(resolution.split('x')) is 2:
            return resolution
        else:
            raise ValueError('Resolution must be WIDTHxHEIGHT or an integer')
    try:
        idx = int(resolution)
        if idx in range(0, len(STANDARD_RESOLUTIONS)):
            return STANDARD_RESOLUTIONS[idx]
        else:
            raise ValueError('Resolution index must be inr range 0-{}, not {}'
                             .format(len(STANDARD_RESOLUTIONS), idx))
    except ValueError:
        raise ValueError('Resolution must be WIDTHxHEIGHT or an integer')


def args_resolution_help():
    print('{:<8} {:<10}'.format('Number', 'Resolution'))
    for idx, res in enumerate(STANDARD_RESOLUTIONS):
        print('{:<8} {:<10}'.format(idx, res))


def server_ip(port):
    online_ips = []
    for interface in [b'eth0', b'wlan0']:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            ip = socket.inet_ntoa(fcntl.ioctl(
                sock.fileno(),
                0x8915,
                struct.pack('256s', interface[:15])
            )[20:24])
            online_ips.append(ip)
        except OSError:
            pass
        sock.close()
    return ' or '.join(['{}:{}'.format(ip, port) for ip in online_ips])


def check_requirements():
    if detect_pi():
        camera = subprocess.check_output(['vcgencmd',
                                          'get_camera']).decode().rstrip()
        if '0' in camera:
            warnings.simplefilter('error', UserWarning)
            warnings.warn('Camera not enabled or connected properly')


def send_arduino(msg, serial_connection):
    if not isinstance(msg, bytes):
        msg = str(msg).encode()
    length = "{0:#0{1}x}".format(len(msg), 6).encode()
    data = length + msg
    serial_connection.write(data)


def receive_arduino(serial_connection):
    if serial_connection.inWaiting():
        msg = serial_connection.readline()
        if len(msg) >= 6:
            length = int(msg[:6], 0)
            data = msg[6:]
            if length == len(data):
                return data.decode()
            else:
                warnings.simplefilter('default', UserWarning)
                warnings.warn('Received incomplete serial string')
    return None

def warning_format(message, category, filename, lineno,
                        file=None, line=None):
    return '-> {}:{}: {}:{}'.format(
        filename, lineno, category.__name__, message)