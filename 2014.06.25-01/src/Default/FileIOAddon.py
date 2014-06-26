__author__ = 'Ninad'

from IAddonInfo import IAddonInfo


class FileIOAddon(IAddonInfo):
    def __init__(self):
        print ("Initializing " + __name__ + " module")

    def start(self):
        print ("Starting activity in module " + __name__)

    def stop(self):
        print ("Stopping activity in module " + __name__)

    def execute(self):
        print ("Executing activity in module " + __name__)

    @staticmethod
    def __info__():
        meta = {
            'uuid': '5b2dd0d5-2bbd-40a9-8250-c21167dbb822',
            'name': 'FileIOAddon',
            'type': '0',
            'os': ['win32'],
            'description': 'File IO related operations will be done with this addon',
            'execution_seq': ['start', 'execute'],
            'stop_seq': ['stop'],
            'version': '1.0.5',
            'author': 'juguar-team',
            'help_url': 'http://www.google.com/easydep/addon/FileIOAddon.html'
        }

        return meta

    @staticmethod
    def __addon__():
        return 'FileIOAddon'
