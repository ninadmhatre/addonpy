__author__ = 'Ninad'

# This file should load the python modules in Default directory and put them in dict with
# as filename => uuid if similar file is found in Hook then specific or all methods will be
# overridden. if hook contains new module specify level when to execute. no level == execute
# in end otherwise after default calls.
# Naming convention: <name>_plugin.py
#
# Default Methods:
# information - get plugin-information
# start - start action for code
# stop - stop action for code
#
# Storing and calling plugins...
# Default Order:
# Always call <test1,test2,test3>_plugin.py
# Override behaviour
#   plugin_name : {
#                    uuid : "",
#                    version: "",
#                    execute_after: "", # number
#                    override: true or false,
#                 }
# x = <AddonManager()>
# x.load_addon_config() # optional
# x.plugin_dir

import sys, os
import imp
import traceback
import pprint as pp
from importlib import import_module
import Helpers

currentdir = os.path.dirname(__file__)

def main():
    # default_plugins = load_default_plugins()
    # extra_plugins = load_extra_plugins()
    #
    # final = default_plugins.union(extra_plugins)
    #
    # parse_and_load(final)

    h = Helpers.helpers()
    def_list = h.find_default_plugins(currentdir)

    for info_file in def_list:
        pp.pprint(h.parse_manifest(info_file))



# def load_default_plugins():
#     import glob
#
#     p = set()
#
#     path_to_search = os.path.join(currentdir, "Default")
#
#     for plugin in glob.glob(path_to_search + "\*.py"):
#             p.add(plugin)
#
#     return p
#
# def load_extra_plugins():
#     import glob
#
#     p = set()
#
#     path_to_search = os.path.join(currentdir, "Hook")
#
#     for plugin in glob.glob(path_to_search + "\*.py"):
#             p.add(plugin)
#
#     return p
#
# def parse_and_load(plist):
#     import pprint as pp
#
#     for f in plist:
#         filename = os.path.basename(f)
#         dirname = os.path.basename(filename)
#         name = "{0}_{1}".format(dirname, filename)
#
#         a = load_module(name, f)
#         pp.pprint(a.load())
#
# def load_module(name, code_path):
#     try:
#         try:
#             code_dir = os.path.dirname(code_path)
#             code_file = os.path.basename(code_path)
#
#             fin = open(code_path, 'rb')
#
#             return imp.load_source(md5.new(code_path).hexdigest(), code_path, fin)
#         finally:
#             try:
#                 fin.close()
#             except:
#                 pass
#     except ImportError, x:
#         traceback.print_exc(file = sys.stderr)
#         raise
#     except:
#         traceback.print_exc(file = sys.stderr)
#         raise


if __name__ == '__main__':
    main()


