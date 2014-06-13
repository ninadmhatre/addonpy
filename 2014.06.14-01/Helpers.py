__author__ = 'Ninad'

import sys
import os
import imp
import traceback
import json
import glob

class helpers(object):

    def __init__(self):
        print("Inside Helper")

    def load_module(self, code_path):
        code_dir = os.path.dirname(code_path)
        code_file = os.path.basename(code_path)

        try:
            try:
                fin = open(code_path, 'rb')
                return imp.load_source(md5.new(code_path).hexdigest(), code_path, fin)
            finally:
                try:
                    fin.close()
                except:
                    pass
        except (ImportError):
            traceback.print_exc(file = sys.stderr)
            raise
        except:
            traceback.print_exc(file = sys.stderr)
            raise

    def parse_manifest(self, code_path):
        if code_path.endswith(".info"):
            print ("Considering {0} file...".format(code_path))
            data = self.read_file_as_binary(code_path)
            parsed_data = {}
            if data is not None:
                parsed_data = json.loads(data)
                return parsed_data

    def read_file_as_binary(self, file):
        if os.path.isfile(file):
            with open(file, 'r') as f_handler:
                f_contents = f_handler.read()
            return f_contents
        else:
            print("file not found: " + file)
            return None

    def find_default_plugins(self, base_dir):
        default_info_file = set()

        path_to_search = os.path.join(base_dir, "Default")

        for plugin in glob.glob(path_to_search + "\*.info"):
                default_info_file.add(plugin)

        return default_info_file
