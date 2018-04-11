"""
Different utility functions
"""

import ctypes
import os
import platform
import signal
import socket
import struct
import subprocess
import warnings


def detect_pi():
    if 'Linux' in platform.platform():
        return True
    else:
        return False


if detect_pi():
    import serial
    import fcntl

STANDARD_RESOLUTIONS = ['160x120', '240x160', '640x360', '640x480', '960x540',
                        '960x640', '1024x576', '1024x600', '1024x768',
                        '1152x864', '1280x720', '1296x972', '1640x1232',
                        '1920x1080']


def is_int(number):
    if isinstance(number, int):
        return True
    else:
        try:
            if isinstance(int(number), int):
                return True
        except ValueError:
            pass
    return False


def resolution_to_tuple(resolution):
    if 'x' not in resolution:
        raise ValueError('Resolution must be in format WIDTHxHEIGHT')
    screen_size = tuple([int(val) for val in resolution.split('x')])
    if len(screen_size) is not 2:
        raise ValueError('Error in parsing resolution, len is not 2')
    return screen_size


def preexec_function():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def valid_resolution(resolution):
    if 'x' in resolution:
        w, h = resolution.split('x')
        if is_int(w) and is_int(h):
            return resolution
        else:
            warning('Resolution must be WIDTHxHEIGHT or an integer')
    elif is_int(resolution):
        idx = int(resolution)
        if idx in range(0, len(STANDARD_RESOLUTIONS)):
            return STANDARD_RESOLUTIONS[idx]
        else:
            warning('Resolution index must be inr range 0-{}, not {}'
                    .format(len(STANDARD_RESOLUTIONS), idx))
    else:
        warning('Resolution must be WIDTHxHEIGHT or an integer')


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
            warning('Camera not enabled or connected properly')


def send_arduino(msg, serial_connection):
    if not isinstance(msg, bytes):
        msg = str(msg).encode()
    length = "{0:#0{1}x}".format(len(msg), 6).encode()
    data = length + msg
    serial_connection.write(data)


def receive_arduino(serial_connection):
    if serial_connection.inWaiting():
        msg = serial_connection.readline().decode().rstrip()
        if len(msg) >= 6:
            try:
                length = int(msg[:6], 0)
                data = msg[6:]
                if length == len(data):
                    return data
                else:
                    warning('Received incomplete serial string: {}'
                            .format(data), 'default')
            except ValueError:
                pass
    return None


def serial_connection(port='/dev/ttyACM0', baudrate=115200, timeout=0.05):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        ser.close()
        ser.open()
        return ser
    except FileNotFoundError:
        pass
    except serial.serialutil.SerialException:
        pass
    except ValueError:
        pass
    warning(message='Could not establish serial connection at {}'
            .format(port), filter='default')
    return None


def warning(message, filter='error', category=UserWarning):
    warnings.simplefilter(filter, category)
    warnings.formatwarning = warning_format
    warnings.warn(message)


def warning_format(message, category, filename, lineno,
                   file=None, line=None):
    return 'WARNING:\n  {}: {}\n  File: {}:{}\n'.format(
        category.__name__, message, filename, lineno)


def free_drive_space():
    """Return folder/drive free space (in megabytes)."""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p('/'),
                                                   None, None,
                                                   ctypes.pointer(free_bytes))
        mb = free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs('/')
        mb = st.f_bavail * st.f_frsize / 1024 / 1024

    if mb >= 1000:
        return '{:.2f} GB'.format(mb / 1000)
    else:
        return '{:.0f} MB'.format(mb)
