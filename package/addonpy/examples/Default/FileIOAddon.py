__author__ = 'Ninad'

from addonpy.IAddonInfo import IAddonInfo


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
    def __addon__():
        return 'FileIOAddon'
