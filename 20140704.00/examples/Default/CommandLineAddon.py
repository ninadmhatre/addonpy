__author__ = 'Ninad'

import os
import sys
from src.IAddonInfo import IAddonInfo
from src.addonpy import AddonLoader


class CommandLineAddon(IAddonInfo):
    def __init__(self):
        print("Initializing " + __name__ + " module")

    def start(self):
        self.curr_dir = os.path.abspath('.')
        print("Starting activity in module " + __name__ + "from dir " + self.curr_dir)
        print("Lets call another addon from here ... 'PingAddon'")
        plol = AddonLoader.get_loaded_addon_instance('PingAddon')
        if plol is not None:
            plol.start()

    def stop(self):
        print("Stopping activity in module " + __name__)

    def execute(self):
        import subprocess as sb
        print ("Executing activity in module " + __name__)

        if sys.platform.startswith('win'):
            sb.check_call(['cmd.exe', '/c', 'dir', self.curr_dir])
        else:
            sb.check_call(['ls', '-lrt', self.curr_dir])

    @staticmethod
    def __addon__():
        return 'CommandLineAddon'