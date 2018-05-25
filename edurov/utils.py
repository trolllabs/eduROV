"""
Different utility functions practical for ROV control
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
    return platform.linux_distribution()[0].lower() == 'debian'


if detect_pi():
    import serial
    import fcntl


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
    warning('Resolution must be WIDTHxHEIGHT')


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
            return False
        else:
            return True
    else:
        warning('eduROV only works on a raspberry pi')
        return False


def send_arduino(msg, serial_connection):
    """
    Send the *msg* over the *serial_connection*

    Adds a hexadecimal number of 6 bytes to the start of the message before
    sending it. "hello there" -> "0x000bhello there"

    Parameters
    ----------
    msg : str or bytes
        the message you want to send
    serial_connection : object
        the :code:`serial.Serial` object you want to use for sending
    """
    if not isinstance(msg, bytes):
        msg = str(msg).encode()
    length = "{0:#0{1}x}".format(len(msg), 6).encode()
    data = length + msg
    serial_connection.write(data)


def receive_arduino(serial_connection):
    """
    Returns a message received over *serial_connection*

    Expects that the message received starts with a 6 bytes long number
    describing the size of the remaining data. "0x000bhello there" -> "hello
    there".

    Parameters
    ----------
    serial_connection : object
        the :code:`serial.Serial` object you want to use for receiving

    Returns
    -------
    msg : str or None
        the message received or None
    """
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


def send_arduino_simple(msg, serial_connection):
    """
    Send the *msg* over the *serial_connection*

    Same as :code:`send_arduino`, but doesn't add anything to the message
    before sending it.

    Parameters
    ----------
    msg : str or bytes
        the message you want to send
    serial_connection : object
        the :code:`serial.Serial` object you want to use for sending
    """
    if not isinstance(msg, bytes):
        msg = str(msg).encode()
    serial_connection.write(msg)


def receive_arduino_simple(serial_connection, min_length=1):
    """
    Returns a message received over *serial_connection*

    Same as :code:`receive_arduino` but doesn't expect that the message starts
    with a hex number.

    Parameters
    ----------
    serial_connection : object
        the :code:`serial.Serial` object you want to use for receiving
    min_length : int, optional
        if you only want that the function to only return the string if it is
        at least this long.

    Returns
    -------
    msg : str or None
        the message received or None
    """
    if serial_connection.inWaiting():
        msg = serial_connection.readline().decode().rstrip()
        if len(msg) >= min_length:
            return msg
        else:
            return None


def serial_connection(port='/dev/ttyACM0', baudrate=115200, timeout=0.05):
    """
    Establishes a serial connection

    Parameters
    ----------
    port : str, optional
        the serial port you want to use
    baudrate : int, optional
        the baudrate of the serial connection
    timeout : float, optional
        read timeout value

    Returns
    -------
    connection : class or None
        a :code:`serial.Serial` object if successful or None if not
    """
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
    warning(message="""Could not establish serial connection at {}\n
    Try running 'ls /dev/*tty*' to find correct port"""
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


def free_drive_space(as_string=False):
    """
    Checks and returns the remaining free drive space

    Parameters
    ----------
    as_string : bool, optional
        set to True if you want the function to return a formatted string.
        4278 -> 4.28 GB

    Returns
    -------
    space : float or str
        the remaining MB in float or as string if *as_string=True*
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p('/'),
                                                   None, None,
                                                   ctypes.pointer(free_bytes))
        mb = free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs('/')
        mb = st.f_bavail * st.f_frsize / 1024 / 1024

    if as_string:
        if mb >= 1000:
            return '{:.2f} GB'.format(mb / 1000)
        else:
            return '{:.0f} MB'.format(mb)
    else:
        return mb


def cpu_temperature():
    """
    Checks and returns the on board CPU temperature

    Returns
    -------
    temperature : float
        the temperature
    """
    cmds = ['/opt/vc/bin/vcgencmd', 'measure_temp']
    response = subprocess.check_output(cmds).decode()
    return float(response.split('=')[1].split("'")[0].rstrip())
