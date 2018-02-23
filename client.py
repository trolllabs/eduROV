import Pyro4
# using Python3.4.2

if __name__ == '__main__':
    uri = 'PYRO:TestAPI@localhost:9999'
    remote = Pyro4.Proxy(uri)
    response = remote.hello('hello')
    print('server said {}'.format(response))
    remote.shutdown()
    remote._pyroRelease()
    print('client exiting')