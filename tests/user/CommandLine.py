__author__ = 'Ninad'

from addonpy.IAddonInfo import IAddonInfo


class CommandLine(IAddonInfo):
    def start_user(self):
        print("Start from " + __name__)

    def stop_user(self):
        print("Stop from " + __name__)

    def execute_user(self):
        print("Execute from " + __name__)

    @staticmethod
    def __addon__():
        return 'CommandLine'