__author__ = 'Ninad'

from addonpy.IAddonInfo import IAddonInfo


class FileIOPlugin(IAddonInfo):
    def method_a(self):
        print ("Starting from " + __name__)

    def method_b(self):
        print ("Stopping from " + __name__)

    def method_c(self):
        print ("Executing from " + __name__)

    @staticmethod
    def __addon__():
        return 'FileIOPlugin'
