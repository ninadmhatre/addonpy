__author__ = 'Ninad'

from addonpy.IAddonInfo import IAddonInfo


class FileIOAddon(IAddonInfo):
    def start(self):
        print ("Starting from " + __name__)

    def stop(self):
        print ("Stopping from " + __name__)

    def execute(self):
        print ("Executing from " + __name__)

    @staticmethod
    def __addon__():
        return 'FileIOAddon'
