# Example for addon module
#
__author__ = 'Ninad'

import logging

from addonpy.addonpy import AddonLoader as loader
from addonpy.addonpyExecutor import AddonExecutor as runner
from addonpy.ILogger import ILogger


class PrintLogger(ILogger):
    """
    This is just simple demo of how to provide logger to addonpy, if you don't use
    something fancy just construct something like this and pass on.
    Note: If you don't care how addonpy displays internal messages just ignore this part
    """
    def info(self, message):
        """
        overriding default info method
        :param message: message to be displayed
        """
        print("Info: {}".format(message))

    def debug(self, message):
        """
        overriding default debug method
        :param message: message to be displayed
        """
        print("Debug: {}".format(message))

    def dummy_function(self):
        """
        Similarly override all the logging levels here...
        :return:
        """
        pass


class LogModule(ILogger):
    """
    Advance version of logger, use this if your code to log internal message from addonpy in your project specific
    format.
    Note: If you don't care how addonpy displays internal messages just ignore this part
    """
    def __init__(self):
        self.logger = self.__configure()

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def warn(self, message):
        self.logger.warn(message)

    def __configure(self):
        """
        Configuring logging for this project [Demo purpose]
        :return: console logger
        """
        logger = logging.getLogger('addon_logger')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_log = logging.StreamHandler()
        console_log.setFormatter(formatter)
        logger.addHandler(console_log)
        return logger


# ********** SETUP **********

# 1. Initialize addon loader with optional verbose & logger [not mentioned below]
#    - If logger is not specified then default print will be used as <DateTime> <Level> <Message>
#    - Verbose decides how much to log
loader_mgr = loader(verbose=True, recursive=True)

# 2. Load all addons (scans & validates) [ Read more __doc__ on '_validate_addon' in AddonLoader ]
loader_mgr.load_addons()

# ********** CALL INDIVIDUAL FUNCTIONS FROM ADDON **********

# 3. Get instance of modules

cli = loader_mgr.get_instance('CommandLineAddon')
cli.print_addon_info()

# 3.1: Call individual functions like below (Make sure to call .stop() or equivalent when you are done!)

cli.start()
cli.execute()
cli.stop()

print(loader_mgr.get_loaded_addons(list_all=True))

# ********** USE RUNNER (Transaction) **********

# 3.2: Optional. Use runner order specified at time of initialization
#      Every addon must specify certain tasks (functions), make use of that and run execution as transaction
#      there by consumer dont have to write try..except..finally block
#    - There are 3 variations of this call...

# 3.2.1: Specify <Execute> <Stop> order at the time of initialization
#        So whoever uses this run_mgr will first call addon.start(), addon.execute() and in case these raises
#        exception or runs successfully addon.stop() will be called.
# [ See example below ]

# ********** RUNNER: SEQUENCE AT INITIALIZATION **********
run_mgr = runner(['start', 'execute'], ['stop'])

# get instance of required addon

# 3.2.2: Pass the instance of addon in order to execute with order specified while initializing run_mgr
#        So, cli.start(), cli.execute() and while exiting cli.stop() will be called.
run_mgr.by_default(cli)

# ********** RUNNER: SEQUENCE AT CALLING **********

# 3.3.1: Or you can specify different <Execution> and <Stop> sequence

fileio = loader_mgr.get_instance('FileIOAddon')
fileio.print_addon_info()

# 3.3.2: Execute fileio.execute() & fileio.start() while starting up and fileio.stop() while exiting.
#        Similar to 'by_default' but changing the sequence of functions.
#        Handy if one of the case!
run_mgr.by_order(fileio, ['execute', 'start'], ['stop'])

# ********** RUNNER: SEQUENCE FROM ADDON META INFORMATION **********

# 3.3.3: Going one step ahead, how about depend upon the <Execution> & <Stop> sequence provided in meta
#        information of addon? PingAddon has below in its meta
#
#            'execution_seq': ['start', 'pause', 'execute'],
#            'stop_seq': ['stop'],

pingadd = loader_mgr.get_instance('PingAddon')
pingadd.print_addon_info()

run_mgr.by_config(pingadd)

# CHECK OUTPUT OF ABOVE IN 'example/stdout/Addonpy_With_LoggingModule.txt'  : With no logger
# CHECK OUTPUT OF ABOVE IN 'example/stdout/Addonpy_With_CustomLogger.txt'   : With custom logger
# CHECK OUTPUT OF ABOVE IN 'example/stdout/Addonpy_With_NoLogger.txt'       : With core logging module



