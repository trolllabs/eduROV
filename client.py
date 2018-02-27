import Pyro4


if __name__ == '__main__':
    with Pyro4.Proxy("PYRONAME:ROVServer") as rov:
        rov.keys.add_item()
        rov.keys.add_item()
        # rov.keys.set('r', False)
        # print(rov.keys.state('r'))
        # rov.keys.set('r', True)
        # print(rov.keys.state('r'))