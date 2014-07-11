__author__ = 'Ninad Mhatre'
__version__ = '1.0.0'


class ILogger(object):
    """
    Use this as a base class for logger module while and override all methods
    in class with each mapping to proper levels in your logger.
    """
    def debug(self, message):
        """
        log debug messages
        :return: void
        """
        pass

    def trace(self, message):
        """
        log trace messages
        :return: void
        """
        pass

    def warn(self, message):
        """
        log warning messages
        :return: void
        """
        pass

    def error(self, message):
        """
        log errors messages
        :return: void
        """
        pass

    def fatal(self, message):
        """
        log fatal messages
        :return: void
        """
        pass