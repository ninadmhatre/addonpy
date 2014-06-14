__author__ = 'Ninad'

import os
import json
from imp import load_source
from glob import glob
from datetime import datetime


class AddonLoader(object):
    def __init__(self, verbose=False, logger=None):
        self.scanned_addons = dict()
        self.verbose = verbose
        self.logger = logger
        self.loaded_addons = dict()
        self.addon_dirs = []
        self.init_dir = os.path.join(os.path.abspath('.'))
        self.config = self._load_own_config()

    def log(self, message, level='debug'):
        if level is None or message is None:
            return

        if not self.verbose and level.lower() == 'debug':
            return

        if self.logger is None:
            print("{0} [{1}] {2}".format(datetime.now(), level.upper(), message))
            # else:
            #    if level == 'info':

    def _load_own_config(self):
        config_file = os.path.join(self.init_dir, 'addon-loader.info')

        addon_conf = LoaderHelper.parse_info_file(config_file)

        if addon_conf is None:
            addon_conf = {
                'required_functions': ['start', 'stop', 'execute', '__addon__', '__info__'],
                'addon_places': [os.path.abspath(os.curdir)]
            }

        self.addon_dirs = addon_conf.get('addon_places')

        return addon_conf

    def set_addon_dirs(self, dirs):
        if not isinstance(dirs, list) or len(dirs) == 0:
            error_message = 'set_add_dirs: dirs must be a list with at least 1 directory to search'
            self.log(error_message, 'error')
            raise TypeError(error_message)

        self.addon_dirs = dirs

    def load_addons(self):
        self.__scan_for_addons()
        os.chdir(self.init_dir)
        self.__validate_addons()
        self.log("Total '{0}' addon(s) loaded".format(len(self.scanned_addons)))

        for addon in self.scanned_addons.keys():
            self.__get_addon_class(addon)

    def get_instance(self, addon):
        if len(self.loaded_addons) == 0:
            err = 'No addon loaded, first call .load_addons()'
            self.log(err, 'error')
            raise ImportWarning(err)

        if addon not in self.loaded_addons:
            raise NameError("'{0}' addon is not loaded".format(addon))
        _instance = self.loaded_addons.get(addon)
        return _instance()

    def __scan_for_addons(self):
        for dir_a in self.addon_dirs:
            if os.path.isdir(dir_a):
                self.log("Searching '{0}' for addons...".format(os.path.abspath(os.path.curdir)))
                for addon_file in glob(os.path.join(dir_a, "*.py")):
                    addon_name, ext = addon_file.split('\\')[-1].split('.')
                    if not addon_name.endswith('Addon'):
                        self.log("  - Not loading '{0}' as file name does not end with 'Addon'".format(addon_file))
                        continue
                    self.log("  - Addon file '{0}' found...".format(addon_file))
                    try:
                        module = load_source(addon_name, addon_file)
                    except ImportError as why:
                        self.log("Failed to load '{0}' from '{1}' directory".format(addon_name, dir),
                                 'error')
                        self.log("\t More info: {}".format(why), 'error')
                    else:
                        self.log("   - Loaded addon: '{0}'".format(addon_name))
                        self.scanned_addons[addon_name] = module
            else:
                self.log("'{0}' directory does not exist".format(dir), 'error')

    def __validate_addons(self):
        for addon in self.scanned_addons.keys():
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
            else:
                self.log('Passed...')

    def __get_addon_class(self, addon):
        _temp = self.scanned_addons.get(addon)
        self.loaded_addons[addon] = _temp.__dict__.get(addon)


class AddonExecutor(object):
    def __init__(self, execute_order, stop_order):
        self.exec_seq = execute_order
        self.stop_seq = stop_order
        self._validate_seq(execute_order, stop_order)

    @staticmethod
    def _validate_seq(e_seq, s_seq):
        if not isinstance(e_seq, list):
            raise TypeError("Execute sequence should be provided as 'tuple'")
        if not isinstance(s_seq, list):
            raise TypeError("Stop sequence should be provided as 'tuple'")

    def execute_with_order(self, addon, execute_order=None, stop_order=None):
        if execute_order is None or stop_order is None:
            raise TypeError("Execute and Stop sequence not defined for module")

        self._validate_seq(execute_order, stop_order)
        self.__run(addon, execute_order, stop_order)

    def execute_with_default(self, addon):
        self.__run(addon, self.exec_seq, self.stop_seq)

    def execute_with_config(self, addon):
        self._validate_seq(addon.get_start_seq(), addon.get_stop_seq())
        self.__run(addon, addon.get_start_seq(), addon.get_stop_seq())

    @staticmethod
    def __run(addon, exec_seq, stop_seq):
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
    @staticmethod
    def parse_info_file(filename):
        if os.path.isfile(filename):
            contents = LoaderHelper.read_json_file(LoaderHelper.read_file(filename))
        else:
            return None
        return contents

    @staticmethod
    def read_json_file(file_contents):
        try:
            contents = json.loads(file_contents)
        except ValueError as why:
            print('read_json_file: failed to parse json file contents. Info: {0}'.format(why.message))
            return None
        return contents

    @staticmethod
    def read_file(file_name):
        with open(file_name, 'r') as f:
            data = f.read()
        return data
