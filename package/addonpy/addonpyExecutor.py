__author__ = 'Ninad Mhatre'
__version__ = '0.1.0'


class AddonExecutor(object):
    """
    Addon Executor to run loaded addons in simple try..except block to make sure close action specific to addon is
    always executed and simple interface to run modules
    """
    def __init__(self, execute_order, stop_order):
        """
        Initializer for class
        :param execute_order: list, functions from addon to be executed
        :param stop_order: list, functions from addon to be executed while stopping the addon
        :return: void
        """
        self.exec_seq = execute_order
        self.stop_seq = stop_order
        self._validate_seq(execute_order, stop_order)

    @staticmethod
    def _validate_seq(e_seq, s_seq):
        """
        validate the execution and stop sequence
        :param e_seq: execution sequence as list
        :param s_seq: stop sequence as list
        :return: void
        :raises: TypeError
        """
        if not isinstance(e_seq, list):
            raise TypeError("Execute sequence should be provided as 'list'")
        if not isinstance(s_seq, list):
            raise TypeError("Stop sequence should be provided as 'list'")

    def by_order(self, addon, execute_order=None, stop_order=None):
        """
        execute addon methods with sequence as passed to this function
        :param addon: addon instance
        :param execute_order: execution sequence like transaction
        :param stop_order: stop sequence
        :return: void
        :raises: TypeError
        """
        if execute_order is None or stop_order is None:
            raise TypeError("Execute and Stop sequence not defined for module")

        self._validate_seq(execute_order, stop_order)
        self._run(addon, execute_order, stop_order)

    def by_default(self, addon):
        """
        execute addon methods with sequence specified while instantiating Executor class
        :param addon: addon instance
        :return: void
        """
        self._run(addon, self.exec_seq, self.stop_seq)

    def by_config(self, addon):
        """
        execute addon functions with order specified in __info__ section of addon
        :param addon: addon instance
        :return: void
        """
        self._validate_seq(addon.get_start_seq(), addon.get_stop_seq())
        self._run(addon, addon.get_start_seq(), addon.get_stop_seq())

    @staticmethod
    def _run(addon, exec_seq, stop_seq):
        """
        run with try .. except loop
        :param addon: addon instance
        :param exec_seq: execution sequence
        :param stop_seq: stop sequence
        :return: void
        :raises: Exception, SystemExit
        """
        try:
            for action in exec_seq:
                e_func = getattr(addon, action)
                e_func()
        except SystemExit:
            print('WARNING: DO NOT USE \'sys.exit()\' in ADDON')
        except Exception as why:
            print('Addon threw exception, make sure to catch it...' + str(why))
            raise
        finally:
            for action in stop_seq:
                s_func = getattr(addon, action)
                s_func()
