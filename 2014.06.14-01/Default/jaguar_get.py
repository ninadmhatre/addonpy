__author__ = 'Ninad'


class jaguar_get(object):
    def __init__(self, logger):
        print ("Initializing " + __name__ + " module")
        log = logger

    def start(self):
        print ("Starting activity in module " + __name__)

    def stop(self):
        print ("Stopping activity in module " + __name__)

    def execute(self):
        print ("Executing activity in module " + __name__)

    def __info__(self):
        print("info for " + __name__ + " addon")

    @staticmethod
    def __addon__():
        return 'jaguar_get'
