# saved as greeting-client.py
import Pyro4

name = input("What is your name? ").strip()

greeting_maker = Pyro4.Proxy("PYRONAME:ROVServer")    # use name server object lookup uri shortcut
print(greeting_maker.get_fortune(name))
greeting_maker.shutdown()
greeting_maker._pyroRelease()