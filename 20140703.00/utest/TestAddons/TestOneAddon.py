__author__ = 'Ninad'

from src.IAddonInfo import IAddonInfo


class TestOneAddon(IAddonInfo):
    def __init__(self):
        return "Initializing " + __name__ + " module"

    def start(self):
        return "starting " + __name__ + " module"

    def stop(self):
        return "Stopping activity in module " + __name__

    def execute(self):
        return "Executing " + __name__ + "..."

    @staticmethod
    def __info__():
        meta = {
            'uuid': 'EEA8B330-A999-4D9F-89AB-D341330B619F',
            'name': 'CommandLineAddon',
            'type': '1',
            'description': 'Command line addon for client, this is supposed to provide CLI validation',
            "os": ["linux", "win32"],
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