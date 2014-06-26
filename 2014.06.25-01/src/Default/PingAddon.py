__author__ = 'Ninad'

import time

from IAddonInfo import IAddonInfo


class PingAddon(IAddonInfo):
    def __init__(self):
        print ("Initializing " + __name__ + " module")

    def start(self):
        print("starting loop till 10....")

        for i in range(0, 10):
            print("Pinging Server: Attempt {0}{1}".format(i, '.' * i))
            time.sleep(1)

    def stop(self):
        print ("Stopping activity in module " + __name__)

    def pause(self):
        print("just a pause b/w the setup & actual execution but i will throw exception..")

        for i in range(0, 10):
            print("Pinging Server: Attempt {0}{1}".format(i, '.' * i))
            time.sleep(0.4)
            if i > 4:
                raise ArithmeticError("This can not be more than 4!!!!!")

    def execute(self):
        import subprocess as sb
        print ("Executing activity in module " + __name__)
        sb.check_call(['cmd.exe', '/c', 'dir', self.curr_dir])

    def __info__(self):
        meta = {
            'uuid': '9d28d505-27ac-435e-8e8c-0f7ddfaa8236',
            'name': 'PingAddon',
            'type': '2',
            'description': 'Run in finitie loop and throw exception...just for fun',
            'execution_seq': ['start', 'pause', 'execute'],
            'stop_seq': ['stop'],
            'version': '1.0.0.1',
            'author': 'juguar-team',
            'help_url': 'http://www.google.com/easydep/addon/PingAddon.html'
        }

        return meta

    @staticmethod
    def __addon__():
        return 'PingAddon'