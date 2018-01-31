import subprocess

STANDARD_PORTS = ['eth0', 'lo', 'wlan0']

def get_port_dict():
    port_dict = {}
    proc = subprocess.Popen('ifconfig', stdout=subprocess.PIPE)
    blocks = proc.stdout.read().split(b'\n\n')
    for port, block in zip(STANDARD_PORTS, blocks):
        lines = block.split(b'\n')
        for line in lines:
            parts = line.decode().replace('  ', ' ').strip().split(' ')
            if parts[0] == 'inet':
                port_dict.update({port: {'inet': parts[1], 'netmask': parts[3]}})
                break
            else:
                port_dict.update({port: None})
    return port_dict


def possible_ips(hostname, netmask):
    masks = [int(val) == 0 for val in netmask.split('.')]
    ips = hostname.split('.')
    if masks[3]:
        for last in range(0, 256):
            if masks[2]:
                for third in range(0, 256):
                    if masks[1]:
                        for second in range(0, 256):
                            yield ('{}.{}.{}.{}'
                                   .format(ips[0], second, third, last))
                    yield ('{}.{}.{}.{}'
                           .format(ips[0], ips[1], third, last))
            yield ('{}.{}.{}.{}'
                   .format(ips[0], ips[1], ips[2], last))
    else:
        yield hostname


def find_server():
    ports = get_port_dict()
    if ports['eth0']:
        ips_to_check = possible_ips(hostname=ports['eth0']['inet'],
                                    netmask=ports['eth0']['netmask'])
    elif ports['wlan0']:
        ips_to_check = possible_ips(hostname=ports['wlan0']['inet'],
                                    netmask=ports['wlan0']['netmask'])
    else:
        raise(ConnectionAbortedError,
              'Not possible to connect, not connected to ethernet or WiFi.')
