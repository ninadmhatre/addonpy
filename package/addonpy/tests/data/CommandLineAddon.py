__author__ = 'Ninad'

from IAddonInfo import IAddonInfo


class CommandLineAddon(IAddonInfo):
    def start(self):
        print("Start from " + __name__)

    def stop(self):
        print("Stop from " + __name__)

    def execute(self):
        print("Execute from " + __name__)

    @staticmethod
    def __addon__():
        return 'CommandLineAddon'