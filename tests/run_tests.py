import sys
import os
import glob

major = sys.version_info[0]
current_dir = os.path.dirname(os.path.abspath(__file__))

if len(sys.argv) == 2 and sys.argv[1] == 'local':
    local_src = os.path.abspath(os.path.join(current_dir, '..', '..'))
    print("Running test build from current directory '{0}'".format(local_src))
    #sys.path.insert(0, local_src)
    os.environ['PYTHONPATH'] = local_src
    sys.path.insert(0, local_src)

import addonpy.addonpy as ap
print("running with addonpy version: {0}".format(ap.get_version()))

if major == 3:
    print("Running tests on: python 3")
elif major == 2:
    print("Running tests on: python 2")

exit_count = 0
    
for test in glob.glob(os.path.join(current_dir, "test_*.py")):
    exit_code = os.system("python {0}".format(test))
    exit_count += 1

sys.exit(exit_count)