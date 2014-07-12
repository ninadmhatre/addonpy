__author__ = 'Ninad Mhatre'
__version__ = '1.0.0'

import json
import os
import sys


class AddonHelper(object):
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
            contents = AddonHelper.parse_json(AddonHelper.read_file(filename))
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
            print('read_json_file: failed to parse json file contents. Info: {0}'.format(why))
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

    @staticmethod
    def walk_dir(directory, ext=None, recursive=False, skip_list=list()):
        """
        walk directory path to look for file with specific extension while optionally ignoring specific files
        :param directory: directory path to walk
        :param ext: file extension to get (if no extension, then its returned)
        :param recursive: only consider current directory, do not walk recursively
        :param skip_list: skip files mentioned in this list
        :return: list of file paths matching criteria
        """

        depth = 0
        file_list = list()
        for abs_dir_path, dir_path, files in os.walk(directory):
            if not recursive and depth > 0:
                break

            if len(files) > 0:
                for file in files:
                    if file in skip_list:
                        continue

                    if ext is None:
                        # append all files
                        file_list.append(os.path.join(abs_dir_path, file))
                    else:
                        if file.endswith(ext):
                            file_list.append(os.path.join(abs_dir_path, file))
            depth += 1

        return file_list

    @staticmethod
    def add_to_module_search_dir(file_path):
        """
        add dirpath path of file given so that file can be loaded with importlib
        :param file_path: file which is to be loaded with importlib
        :return: absolute dirname of file if found, None otherwise
        """

        dir_path = os.path.dirname(file_path)

        if os.path.isdir(dir_path) and dir_path not in sys.path:
            sys.path.insert(0, dir_path)
            return dir_path
        else:
            return None

    @staticmethod
    def convert_string_to_boolean(val):
        """
        Convert given string to bool
        :param val: string
        :return: boolean
        :rtype: bool
        """
        if val is None:
            return False
        elif val.lower() in ('true', '1', 'yes', 'y'):
            return True
        else:
            return False

    @staticmethod
    def get_basename_and_ext(file_path):
        """
        split the filepath in file name and extension. dirpath is stripped
        :param file_path: absolute file path
        :return: list with basename of file and extension
        """
        return os.path.basename(file_path).split('.', 2)

    @staticmethod
    def is_compatible_for_current_platform(eligible_platforms):
        """
        check if current platform is one listed in supplied platforms
        :param eligible_platforms: supplied platform list
        :return: true or false
        :rtype: bool
        """

        return sys.platform in eligible_platforms