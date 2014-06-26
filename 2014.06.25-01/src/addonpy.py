__author__ = 'Ninad'

# VERSION: 20140624.01
# Changes:
#   - Option to load via ".info" files
#   - Function to recursively load other addons from another addon
#   - support for 'os' type in addon info
#   - BugFix: Search for addon-loader.info in scripts directory only

import os
import json
from imp import load_source
from glob import glob
from datetime import datetime
import sys


class AddonLoader(object):
    """
    Addon Loader class, scans, validates, loads the addons and used to get the instance of the addons
    """
    loaded_addons = dict()
    active_config = dict()
    current_platform = sys.platform

    def __init__(self, verbose=False, logger=None):
        """
        Initialize with optional verbose mode (print information) and optional logger (not implemented)
        :param verbose: print loading information
        :param logger: custom logger used in verbose mode
        :return: void
        """
        self.scanned_addons = dict()
        self.verbose = verbose
        self.logger = logger
        self.addon_dirs = []
        self.init_dir = AddonLoader._get_calling_script_dir()
        self.config = self._load_own_config()

    @staticmethod
    def get_loaded_addon_instance(addon_name):
        if addon_name.endswith("Addon"):
            if addon_name in sys.modules:
                _temp = sys.modules.get(addon_name, None)
                _temp_class = _temp.__dict__.get(addon_name)
                return _temp_class()
        else:
            return None

    @staticmethod
    def _get_calling_script_dir():
        caller = sys.argv[0]
        return os.path.dirname(caller)

    def log(self, message, level='debug'):
        """
        log messages to console
        :param message: message to log
        :param level: message level, default: debug
        :return: void
        """
        if level is None or message is None:
            return

        if not self.verbose and level.lower() == 'debug':
            return

        if self.logger is None:
            print("{0} [{1}] {2}".format(datetime.now(), level.upper(), message))
        else:
            if level == 'info':
                self.logger.info(message)
            elif level == 'debug':
                self.logger.debug(message)
            elif level == 'trace':
                self.logger.trace(message)
            elif level == 'error':
                self.logger.error(message)
            elif level == 'fatal':
                self.logger.fatal(message)

    def set_logger(self, logger):
        self.logger = logger

    def _load_own_config(self):
        """
        load AddonLoader config file or if not found set to default
        :return: config
        :rtype: dict
        """
        config_file = os.path.join(self.init_dir, 'addon-loader.info')
        self.log("Trying to read addonpy config for this project from '{0}'".format(config_file))
        addon_conf = LoaderHelper.parse_info_file(config_file)

        if addon_conf is None:
            self.log("addon-loader.info file not found/not proper, loading pre-configured addon config")
            addon_conf = {
                'required_functions': ['start', 'stop', 'execute', '__addon__', '__info__'],
                'addon_places': [os.path.abspath(os.curdir)]
            }

        for dir_name in addon_conf.get('addon_places'):
            if dir_name.startswith('.') or dir_name.startswith('..'):
                self.log("Addon directory(ies) mentioned as relative paths, converting to absolute paths...")
                _abs_temp_path = os.path.abspath(os.path.join(self.init_dir, dir_name))
            else:
                # Its not a relative path. you cannot use $ENV in loader.info file, rely on set_addon_dirs method...
                _abs_temp_path = dir_name

            if os.path.isdir(_abs_temp_path):
                self.addon_dirs.append(_abs_temp_path)

        return addon_conf

    def set_addon_dirs(self, dirs):
        """
        override the default config value to look for addons
        :param dirs: directories to search for addons as list
        :return: void
        :raises: TypeError
        """
        if not isinstance(dirs, list) or len(dirs) == 0:
            error_message = 'set_add_dirs: dirs must be a list with at least 1 directory to search'
            self.log(error_message, 'error')
            raise TypeError(error_message)

        self.addon_dirs = dirs

    def load_addons(self):
        """
        Load addons from specified directories
        - scan files
        - load them
        - validate for required methods
        - load
        :return: void (sets class level dict)
        """
        self.__scan_for_addons()
        self.__validate_addons()
        #self.log("Total '{0}' addon(s) loaded".format(len(self.scanned_addons)))

        for addon in self.scanned_addons.keys():
            self.__get_addon_class(addon)

    def get_instance(self, addon):
        """
        get instance of addon loaded by name
        :param addon: addon name for which instance will be returned
        :return: instance of loaded addon
        :rtype: class instance
        :raises: ImportWarning, NameError
        """
        if len(self.loaded_addons) == 0:
            err = 'No addon loaded, first call .load_addons()'
            self.log(err, 'error')
            raise ImportWarning(err)

        if addon not in self.loaded_addons:
            raise NameError("'{0}' addon is not loaded".format(addon))
        _instance = self.loaded_addons.get(addon)
        return _instance.get('Class')()

    def __scan_for_addons(self):
        """
        scan directories and load the addons
        :return: void ( sets class level dict with all the found addons )
        :raises: ImportError
        """
        import pprint
        pprint.pprint(self.addon_dirs)
        for dir_a in self.addon_dirs:
            if os.path.isdir(dir_a):
                self.log("Searching '{0}' for addons...".format(dir_a))

                if self.config.get('parse_from_info_file') == "True":
                    self.logger.info("Loading addons with '.info' files only")
                    matching_list = glob(os.path.join(dir_a, "*.info"))
                else:
                    self.logger.info("Loading addons with '.py' extension")
                    matching_list = glob(os.path.join(dir_a, "*.py"))

                for addon_file in matching_list:
                    addon_name, ext = addon_file.split('\\')[-1].split('.')
                    if not addon_name.endswith('Addon'):
                        self.log(">> Not loading '{0}' as file name does not end with 'Addon'".format(addon_file))
                        continue
                    self.log("> Addon file '{0}' found...".format(addon_file))

                    if self.config.get('parse_from_info_file') == "True":
                        info_content = LoaderHelper.parse_info_file(addon_file)
                        compatible_platforms = info_content.get('os')
                        if compatible_platforms is not None:
                            if self.is_compatible_for_current_platform(compatible_platforms):
                                self._load_module_from_source(addon_name, addon_file)
                            else:
                                self.logger.info(">>> Addon '{0}' not compatible with current '{1}' platform."
                                                 "supported platforms by this addon '{2}'".
                                                 format(addon_name, self.current_platform,
                                                        ','.join(compatible_platforms)))
                    else:
                        self._load_module_from_source(addon_name, addon_file)
            else:
                self.log("'{0}' directory does not exist".format(dir), 'error')

    def _load_module_from_source(self, addon_name, addon_file):

        if self.config.get('parse_from_info_file') == "True":
            addon_source_file = addon_file.replace('.info', '.py')
            if not os.path.isfile(addon_file):
                self.logger.error("Addon source file is missing, .info file found '{0}' but \n"
                                  "source file is missing".format(addon_file, addon_source_file))
                return None
            addon_file = addon_source_file

        try:
            module = load_source(addon_name, addon_file)
        except ImportError as why:
            self.log("Failed to load '{0}' from '{1}' directory".format(addon_name, dir),
                     'error')
            self.log("\t More info: {}".format(why), 'error')
        else:
            self.log("Loaded addon: '{0}'".format(addon_name))
            self.scanned_addons[addon_name] = module

    def is_compatible_for_current_platform(self, eligible_platforms):
        if self.current_platform in eligible_platforms:
            return True
        else:
            return False

    def __validate_addons(self):
        """
        validate the addon by checking if addon has required functions defined
        :return: void ( updates scanned_addon dict )
        """
        total = 0
        passed = 0
        failed = 0

        for addon in self.scanned_addons.keys():
            total += 1
            error_cnt = 0
            self.log("Validating addon: '{0}'".format(addon))
            addon_as_module = self.scanned_addons.get(addon)
            addon_functions = getattr(addon_as_module, addon_as_module.__name__)
            all_functions = addon_functions.__dict__.keys()

            for expected_function in self.config.get('required_functions'):
                if expected_function not in all_functions:
                    error_cnt += 1
                    self.log("     Required method: '{0}' not found!".format(expected_function), 'error')

            if error_cnt > 0:
                self.log("Failed! Unloading addon...".format(addon), 'error')
                self.scanned_addons.__delitem__(addon)
                failed += 1
            else:
                passed += 1
                self.log('Passed...')

        self.log("Total '{0}' addons found. passed validation: {1} failed validations: {2}".
                 format(total, passed, failed))

    def __get_addon_class(self, addon):
        """
        Get addon class from loaded module
        :param addon: addon to get
        :return: void ( creates new dict() with class )
        """
        _temp = self.scanned_addons.get(addon)
        self.loaded_addons[addon] = {'Class': None, 'Meta': None}
        self.loaded_addons[addon]['Class'] = _temp.__dict__.get(addon)
        # TODO: Implement other search types and filters
        # self.loaded_addons[addon]['Meta'] = self.loaded_addons[addon]['Class']().get_addon_info()

    def get_loaded_addons(self, type_filter, search_pattern=None):
        t_filter = type_filter.lower()

        valid_types = ('name', 'version', 'type', 'type_desc', 'uuid', '*')

        if t_filter not in valid_types:
            self.logger.debug("Invalid '{0}' filter type specified, valid ones: name, type, type_desc, uuid & '*'".
                              format(t_filter))
            return None

        if t_filter == '*':
            return self.loaded_addons.keys()

        # TODO: Implement other search types and filters


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

    def execute_with_order(self, addon, execute_order=None, stop_order=None):
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
        self.__run(addon, execute_order, stop_order)

    def execute_with_default(self, addon):
        """
        execute addon methods with sequence specified while instantiating Executor class
        :param addon: addon instance
        :return: void
        """
        self.__run(addon, self.exec_seq, self.stop_seq)

    def execute_with_config(self, addon):
        """
        execute addon functions with order specified in __info__ section of addon
        :param addon: addon instance
        :return: void
        """
        self._validate_seq(addon.get_start_seq(), addon.get_stop_seq())
        self.__run(addon, addon.get_start_seq(), addon.get_stop_seq())

    @staticmethod
    def __run(addon, exec_seq, stop_seq):
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
            print('Addon thrown exception, better catch it ...' + str(why))
            raise
        finally:
            for action in stop_seq:
                s_func = getattr(addon, action)
                s_func()


class LoaderHelper(object):
    """
    Small utility class to read json and info files
    """
    @staticmethod
    def parse_info_file(filename):
        """
        parse .info file for addon
        :param filename: absolute file path to read
        :return: info file contents
        :rtype: dict
        """
        if os.path.isfile(filename):
            contents = LoaderHelper.parse_json(LoaderHelper.read_file(filename))
        else:
            return None
        return contents

    @staticmethod
    def parse_json(file_contents):
        """
        parse json string
        :param file_contents: string with json data
        :return: dict with parsed data
        :rtype: dict
        :raises: ValueError
        """
        try:
            contents = json.loads(file_contents)
        except ValueError as why:
            print('read_json_file: failed to parse json file contents. Info: {0}'.format(why.message))
            return None
        return contents

    @staticmethod
    def read_file(file_name):
        """
        read file and return string
        :param file_name: file to read with absolute path
        :return: file contents as string
        :rtype: str
        """
        with open(file_name, 'r') as f:
            data = f.read()
        return data


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