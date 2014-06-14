__author__ = 'Ninad'

import os
import sys
from AddonLoader import AddonLoader as loader
from AddonLoader import AddonExecutor as runner

# first get load all the addons
loader_mgr = loader(verbose=True)
loader_mgr.load_addons()

# second setup runner instance
run_mgr = runner(['start', 'execute'], ['stop'])

# get instance of required addon

cli = loader_mgr.get_instance('CommandLineAddon')
cli.print_addon_info()
run_mgr.execute_with_default(cli)

# otherwise you can call methods as require

fileio = loader_mgr.get_instance('FileIOAddon')
fileio.print_addon_info()
run_mgr.execute_with_order(fileio, ['execute', 'start'], ['stop'])

pingadd = loader_mgr.get_instance('PingAddon')
pingadd.print_addon_info()
run_mgr.execute_with_config(pingadd)
print("I am stil alive ...")


#import pprint as pp
# pp.pprint(t.config)