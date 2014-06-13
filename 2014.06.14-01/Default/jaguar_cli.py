__author__ = 'Ninad'

import os, sys
import logging as log

# def meta():
# information = {
#         'uuid': 'EEA8B330-A999-4D9F-89AB-D341330B619F',
#         'name': 'jaguar-cli',
#         'type': '1',
#         'description': 'This is hook_test1 module',
#         'sequence': [
#             'start',
#             'stop'
#         ],
#        'version': {
#             'major': 1,
#             'minor': 0,
#             'patch': 5,
#         },
#         'creator': 'jugaur-team',
#         'help': 'http://somewebsite/<name>.html'
#     }
#
#     return information
#


class jaguar_cli(object):
    def __init__(self, logger):
        print ("Initializing " + __name__ + " module")

    def start(self):
        self.curr_dir = os.path.abspath('.')
        print ("Starting activity in module " + __name__ + "from dir " + self.curr_dir )

    def stop(self):
        print ("Stopping activity in module " + __name__)

    def execute(self):
        import subprocess as sb
        print ("Executing activity in module " + __name__)
        sb.check_call(['cmd.exe', '/c', 'dir', self.curr_dir])

    def __info__(self):
        print("info for " + __name__ + " addon")

    @staticmethod
    def __addon__():
        return 'jagauar_cli'