import sys

STANDARD_RESOLUTIONS = ['160x120', '240x160', '640x360', '640x480', '960x540',
                        '960x640', '1024x576', '1024x600', '1024x768',
                        '1152x864', '1280x720', '1296x972', '1640x1232',
                        '1920x1080']

KEYCODES = {}


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
    sys.exit()
