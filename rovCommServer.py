import subprocess
import Pyro4

nsProcess = subprocess.Popen('python -m Pyro4.naming', shell=False)

@Pyro4.expose
class GreetingMaker(object):
    def get_fortune(self, name):
        return "Hello, {0}. Here is your fortune message:\n" \
               "Tomorrow's lucky number is 12345678.".format(name)

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(GreetingMaker)   # register the greeting maker as a Pyro object
ns.register("example.greeting", uri)   # register the object with a name in the name server

print("Ready.")
try:
    daemon.requestLoop()
except KeyboardInterrupt:
    print('whaat')
finally:
    print('Shutting down server')
    nsProcess.terminate()
    nsProcess.wait()
