__author__ = 'Ninad'

import os
import sys
from IAddonInfo import IAddonInfo
from addonpy import AddonLoader


class CommandLineAddon(IAddonInfo):
    def __init__(self):
        print ("Initializing " + __name__ + " module")

    def start(self):
        self.curr_dir = os.path.abspath('.')
        print("Starting activity in module " + __name__ + "from dir " + self.curr_dir)
        print("Lets call another addon from here ... 'PingAddon'")
        p_ad = AddonLoader.get_loaded_addon_instance('FileIOAddon')
        p_ad.print_addon_info()
        p_ad.start()

    def stop(self):
        print ("Stopping activity in module " + __name__)

    def execute(self):
        import subprocess as sb
        print ("Executing activity in module " + __name__)

        if sys.platform.startswith('win'):
            sb.check_call(['cmd.exe', '/c', 'dir', self.curr_dir])
        else:
            sb.check_call(['ls', '-lrt', self.curr_dir])

    def __info__(self):
        meta = {
            'uuid': 'EEA8B330-A999-4D9F-89AB-D341330B619F',
            'name': 'CommandLineAddon',
            'type': '1',
            'description': 'Command line addon for client, this is supposed to provide CLI validation',
            'execution_seq': ['start', 'execute'],
            'stop_seq': ['stop'],
            'version': '1.0.5',
            'author': 'juguar-team',
            'help_url': 'http://www.google.com/easydep/addon/CommandLineAddon.html'
        }

        return meta

    @staticmethod
    def __addon__():
        return 'CommandLineAddon'