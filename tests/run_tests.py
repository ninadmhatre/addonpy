import sys
import os
import glob
import subprocess

major = sys.version_info[0]
current_dir = os.path.dirname(os.path.abspath(__file__))


def runTest(test_name):

    try:
        output = subprocess.check_output(["python", test_name], stderr=subprocess.STDOUT)
        if not isinstance(output, str):
            outputx = output.decode('utf-8')
            output = outputx
    except subprocess.CalledProcessError as err:
        return None, err.returncode
    else:
        return output.split(os.linesep), 0

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

err_cnt = 0

for test in glob.glob(os.path.join(current_dir, "test_*.py")):    
    out, exit_code = runTest(test)
    print("Test: '{0}' exited with '{1}'...".format(test, exit_code))
    for o_line in out:
        if o_line.endswith('... FAIL'):
            print("\t>>>Failed: {0}".format(o_line))
            err_cnt += 1
        else:
            print(o_line)

sys.exit(err_cnt)