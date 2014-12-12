__author__ = 'Ninad Mhatre'

import os
import importlib
from datetime import datetime
import sys

try:
    from addonpy.addonpyHelpers import AddonHelper
except ImportError:
    # Hack for Py2
    from .addonpyHelpers import  AddonHelper


def get_version():
    return AddonHelper.get_version()


class AddonLoader(object):
    """
    Addon Loader class, scans, validates, loads the addons and used to get the instance of the addons
    """

    ext = '.info'
    current_platform = AddonHelper.get_os()

    # Initializer

    def __init__(self, verbose=None, logger=None, recursive=None, lazy_load=None):
        """
        Initialize with optional verbose mode (print information) and optional logger (not implemented)
        :param verbose: print loading information
        :param logger: custom logger used in verbose mode
        :param recursive: recursively search for addons
        :param lazy_load: scan first load when called
        :return: void
        """

        # Instance variables
        self.scanned_addons = dict()
        self.loaded_addons = dict()
        self.active_config = dict()
        self.addon_id = "Addon"
        self.ignore_addon_id = False
        self.current_dir = os.path.abspath('.')

        # Required variables supplied by caller
        self.verbose = verbose
        self.logger = logger
        self.addon_dirs = []
        self.recursive_search = recursive
        self.lazy_load = lazy_load

        # Setting up module
        self.init_dir = AddonLoader._get_calling_script_dir()
        self._load_own_config()
        self._apply_config()
        self.print_current_config()

    # Setters

    def _apply_config(self):
        """
        apply given configuration
        :return: void
        """
        self.set_addon_dirs(self.active_config.get('addon_places'))

        recursive_from_config = self.active_config.get('recursive')
        lazy_load_from_config = self.active_config.get('lazy_load')
        verbose_from_config = self.active_config.get('verbose')

        if self.recursive_search is None:
            if recursive_from_config:
                self.log("Picking 'recursive' search value from config...", "info")
                self.recursive_search = AddonHelper.convert_string_to_boolean(recursive_from_config)
            else:
                self.recursive_search = False

        if self.lazy_load is None:
            if lazy_load_from_config:
                self.log("Picking 'lazy_load' value from config...", "info")
                self.lazy_load = AddonHelper.convert_string_to_boolean(lazy_load_from_config)
            else:
                self.lazy_load = False

        if self.verbose is None:
            if verbose_from_config:
                self.log("Picking 'verbose' setting from config...", "info")
                self.verbose = AddonHelper.convert_string_to_boolean(verbose_from_config)
            else:
                self.verbose = False

    def print_current_config(self):
        """
        prints current configuration recursive & lazy load mode status, if On or Off
        :return: void
        """
        self.log("Recursive addon search is: {0}".format('On' if self.recursive_search else 'Off'))
        self.log("Lazy load mode is: {0}".format('On' if self.lazy_load else 'Off'))

    def set_logger(self, logger):
        """
        set logger for addonpy explicitly once module is initialized
        :param logger: logger instance
        """
        self.logger = logger

    def set_lazy_load(self, state):
        """
        Change lazy_load mode. Recommended: Either set while initializing or leave it default
        :param state: true or false
        :return: void
        """
        self.lazy_load = AddonHelper.convert_string_to_boolean(state)

    def set_recursive_search(self, state):
        """
        Change recursive search mode for addons, Recommended: Either set while initializing or leave it default
        :param state: true or false
        :return: void
        """
        self.recursive_search = AddonHelper.convert_string_to_boolean(state)

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

        self.addon_dirs = list()

        for dir_name in dirs:
            _abs_temp_path = self._get_abspath(dir_name, True)
            if os.path.isdir(_abs_temp_path):
                self.addon_dirs.append(_abs_temp_path)

    def set_addon_identifier(self, identifier, ignore_suffix=False):
        """
        Set what should be suffix of addon, till 0.9.2 default suffix was "Addon"
        :param identifier: Specify suffix such as Plugin, Module etc.. Can be "None" if ignore_suffix = True
        :param ignore_suffix: if True, ignore suffix all .info file would be loaded.
        """

        if identifier is None and ignore_suffix:
            self.log("Setting Identifier to None, i.e. all .info files will be considered as Addons")
            self.addon_id = None
            self.ignore_addon_id = True
        else:
            if identifier is None:
                self.log("Setting Identifier to Default i.e. 'Addon', Invalid identifier provided", 'warn')
                self.addon_id = "Addon"
                self.ignore_addon_id = False
            else:
                self.log("Setting Identifier to '{0}'".format(identifier))
                self.addon_id = identifier
                self.ignore_addon_id = False

    def set_addon_methods(self, method_list):
        """
        Specify required methods in Addon
        :param method_list: list of required methods
        """
        if not isinstance(method_list, list) or len(method_list) == 0:
            error_message = 'set_addon_methods: methods must be a list with at least 1 method'
            self.log(error_message, 'error')
            raise TypeError(error_message)

        # There no way to find if user will provide right list here, so applying it as is.
        # This overrides the info in "addon-loader.info" file

        self.log("Overwriting 'required_functions' with list specified by user", 'warn')
        self.active_config['required_functions'] = method_list

    # Private

    # Getters

    @staticmethod
    def get_loaded_addon_instance(addon_name, addon_identifier='Addon'):
        """
        Use to for nested addon calls.
        :param addon_name: addon to load
        :return: addon instance
        """
        if addon_name.endswith(addon_identifier):
            if addon_name in sys.modules:
                _temp = sys.modules.get(addon_name, None)
                if _temp is not None:
                    _temp_class = _temp.__dict__.get(addon_name)
                    return _temp_class()
                else:
                    return None
            else:
                print("** Are you running this with Lazy load? make sure all modules are already loaded! **")
                return None  # silent
        else:
            return None

    # Public

    def load_addons(self):
        """
        Load addons from specified directories
        - scan files
        - load them
        - validate for required methods
        - load
        :return: void (sets class level dict)
        """
        self._scan_for_addons()
        self._validate_addons()

        for addon in self.scanned_addons.keys():
            self._get_addon_class(addon, self.lazy_load)

    def get_instance(self, addon):
        """
        get instance of specific addon loaded by addonpy.
        :param addon: addon name for which instance will be returned
        :return: instance of loaded addon
        :rtype: class instance
        :raises: ImportWarning, NameError
        """

        if len(self.loaded_addons) == 0 and not self.lazy_load:
            err = 'No addon loaded, first call .load_addons() or no addons found in given directory'
            self.log(err, 'error')
            raise ImportError(err)

        if addon not in self.scanned_addons:
            raise ImportError('{0} is not available for loading, no such addon found'.format(addon))

        # addon must be already part of scanned addon list
        source_file = ''
        if addon in self.scanned_addons:
            source_file = self.scanned_addons[addon]['FILE']

        if self.scanned_addons[addon]['MODULE'] is None:
            if self.lazy_load:
                self._load_module_from_source(addon, source_file, False)
                if self._validate_addon(addon):
                    self.log("'{0}' addon validated successfully".format(addon))
                else:
                    self.log("'{0}' addon failed validation".format(addon), 'error')
                    raise ImportError("Addon failed validation, please check log file")

                self._get_addon_class(addon, lazy_load=False)

        if addon not in self.loaded_addons:
            raise NameError("'{0}' addon is not loaded".format(addon))
        _instance = self.loaded_addons.get(addon)
        return _instance.get('CLASS')()

    def get_loaded_addons(self, by_type=None, list_all=False):
        """
        get addons based on specific user specified type. will show only loaded modules, if lazy_load is set it will
        return 0 at start and as addons are requested this will be populated
        :param by_type: type name
        :param list_all: list all loaded modules
        :return: list of loaded addons
        """
        if list_all:
            return self.loaded_addons.keys()

        if by_type is None:
            return

        result = list()

        for addon in self.loaded_addons.keys():
            meta = self.loaded_addons[addon]['META']

            if isinstance(meta, dict):
                if 'type' in meta and meta.get('type') in by_type:
                    result.append(addon)

        return result

    @staticmethod
    def _get_calling_script_dir():
        """
        Get the directory of script using this module
        :return: directory path
        """
        caller = sys.argv[0]
        return os.path.dirname(caller)

    def _get_addon_class(self, addon, lazy_load):
        """
        Get addon class from loaded module
        :param addon: addon to get
        :param lazy_load: if set, return otherwise get class instance from loaded module
        :return: void ( creates new dict() with class )
        """
        if lazy_load:
            return

        _temp = self.scanned_addons[addon]['MODULE']
        _temp_class = _temp.__dict__.get(addon)
        _temp_class.__info__ = self.scanned_addons[addon]['META']
        self.loaded_addons[addon] = {'CLASS': None, 'META': None, 'FILE': None}
        self.loaded_addons[addon]['CLASS'] = _temp_class
        self.loaded_addons[addon]['META'] = self.scanned_addons[addon]['META']
        self.loaded_addons[addon]['FILE'] = self.scanned_addons[addon]['FILE']

    def _load_own_config(self):
        """
        load AddonLoader config file or if not found set to default
        :return: config
        :rtype: dict
        """
        config_file = os.path.join(self.init_dir, 'addon-loader.info')
        self.log("Trying to read addonpy config for this project from '{0}'".format(config_file))
        addon_conf = AddonHelper.parse_info_file(config_file)

        if addon_conf is None:
            self.log("addon-loader.info file not found/not proper, loading pre-configured addon config")
            addon_conf = dict(required_functions=['start', 'stop', 'execute', '__addon__'],
                              addon_places=[os.path.abspath(os.curdir)],
                              recursive='False',
                              verbose='False',
                              lazy_load='False')
            self.active_config = addon_conf
            return

        addon_places = addon_conf.get('addon_places')

        if addon_places is not None:
            for dir_name in addon_conf.get('addon_places'):
                _abs_temp_path = self._get_abspath(dir_name, True)
                if os.path.isdir(_abs_temp_path):
                    self.addon_dirs.append(_abs_temp_path)
        else:
            self.addon_dirs.append(os.path.abspath(os.path.curdir))

        addon_conf['addon_places'] = self.addon_dirs
        self.active_config = addon_conf

    def _get_abspath(self, fpath, verbose):
        """
        get absolute path from relative path
        :param fpath: relative path
        :param verbose: print info to screen?
        :return: absolute path
        """
        if fpath.startswith('.') or fpath.startswith('..'):
            if verbose:
                self.log("Addon directory mentioned as relative, converting '{0}' as absolute path...".format(fpath))
            _abs_temp_path = os.path.abspath(os.path.join(self.init_dir, fpath))
            self.log("absolute path '{0}'".format(_abs_temp_path))
        else:
            _abs_temp_path = fpath
        return _abs_temp_path

    def _scan_for_addons(self):
        """
        scan directories and load the addons
        :return: void ( sets class level dict with all the found addons )
        :raises: ImportError
        """
        possible_addons = self._search_for_addons()

        if len(possible_addons) > 0:
            for addon_file in possible_addons:
                addon_name, ext = AddonHelper.get_basename_and_ext(addon_file)

                if not self.ignore_addon_id and not addon_name.endswith(self.addon_id):
                    self.log(">> Not loading '{0}' as file name does not end with '{0}'".format(addon_file,
                                                                                                self.addon_id))
                    continue

                self.log("> Addon file '{0}' found...".format(addon_file))

                addon_info = AddonHelper.parse_info_file(addon_file)
                compatible_platforms = addon_info.get('os')

                if compatible_platforms is not None:
                    if AddonHelper.is_compatible_for_current_platform(self.current_platform, compatible_platforms):
                        # Add in scanned_addons
                        self._update_scanned_addon_list(addon_name, addon_file, addon_info)
                        self._load_module_from_source(addon_name, addon_file, self.lazy_load)
                    else:
                        self.log(">>> Addon '{0}' not compatible with current '{1}' platform."
                                 "supported platforms by this addon '{2}'".
                                 format(addon_name, self.current_platform, ', '.join(compatible_platforms)), "info")
                else:
                    # Add in scanned_addons
                    self._update_scanned_addon_list(addon_name, addon_file, addon_info)
                    self._load_module_from_source(addon_name, addon_file, self.lazy_load)
        else:
            self.log("No addons found", "error")

    def _search_for_addons(self):
        """
        Get file list of matching addons by their extension
        :return: list with possible addon files
        :rtype: list
        """

        matching_list = list()

        for dir_a in self.addon_dirs:
            if os.path.isdir(dir_a):
                self.log("Searching '{0}' for addons with extension {1}...".format(dir_a, self.ext))
                m_list = AddonHelper.walk_dir(dir_a, self.ext, self.recursive_search)
                matching_list.extend(m_list)

        return matching_list

    def _update_scanned_addon_list(self, addon_name, addon_path, addon_info):
        """
        Add addon to scanned addon list with basic module information
        :param addon_name: addon name
        :param addon_path: absolute addon file path
        :param addon_info: addon info dict()
        :return: void
        """
        if addon_name in self.scanned_addons:
            return
        if addon_path.endswith('.info'):
            file_path = addon_path.replace('.info', '.py')
            addon_path = file_path

        self.scanned_addons[addon_name] = {'FILE': addon_path, 'META': addon_info, 'MODULE': None}

    def _load_module_from_source(self, addon_name, addon_file, lazy_load):
        """
        load addon in sys.modules
        :param addon_name: addon name
        :param addon_file: addon absolute file path
        :param lazy_load: True, load module straight away. False, Load when required.
        :return: void
        """

        if lazy_load:  # used when lazy_load == True, load when required
            return

        base_dir = AddonHelper.add_to_module_search_dir(addon_file)

        try:
            module = importlib.import_module(addon_name)
        except (ImportError, SystemError) as why:
            self.log("Failed to load '{0}' from '{1}' directory".format(addon_name, base_dir), 'error')
            self.log("\t More info: {}".format(why), 'error')
        else:
            self.log("addon loaded: '{0}'".format(addon_name))
            self.scanned_addons[addon_name]['MODULE'] = module

    def _validate_addons(self):
        """
        validate the addons by checking if addon has required functions defined
        :return: void ( updates scanned_addon dict )
        """

        if self.lazy_load:
            self.log("skipping validation as lazy_load mode is set, validation will be performed while loading...")
            return

        total = 0
        passed = 0
        failed = 0

        failed_list = list()

        for addon in self.scanned_addons.keys():
            total += 1
            if self._validate_addon(addon):
                passed += 1
            else:
                failed += 1
                failed_list.append(addon)

        if len(failed_list) > 0:
            [self.scanned_addons.pop(_addon, None) for _addon in failed_list]

        self.log("Total '{0}' addons found. passed validation: {1} failed validations: {2}".
                 format(total, passed, failed))

    def _validate_addon(self, addon):
        """
        Validate single addon"s" relies on this to validate single addon
        :param addon: addon to validate
        :return: True or False
        :rtype: bool
        """

        error_cnt = 0
        self.log("Validating addon: '{0}'".format(addon))
        addon_as_module = self.scanned_addons[addon]['MODULE']
        addon_functions = getattr(addon_as_module, addon_as_module.__name__)
        all_functions = addon_functions.__dict__.keys()

        for expected_function in self.active_config.get('required_functions'):
            if expected_function not in all_functions:
                error_cnt += 1
                self.log("     {0} : Required method: '{1}' not found!".format(addon, expected_function), 'error')

        if error_cnt > 0:
            self.log("Failed! Unloading addon...".format(addon), 'error')
            # self.scanned_addons.pop(addon, None)
            return False
        else:
            self.log('Passed...')
            return True

    # Logger

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
            elif level == 'warn':
                self.logger.warn(message)
            elif level == 'trace':
                self.logger.trace(message)
            elif level == 'error':
                self.logger.error(message)
            elif level == 'fatal':
                self.logger.fatal(message)


if __name__ == '__main__':
    print("use this as module, basic help: import addonpy")