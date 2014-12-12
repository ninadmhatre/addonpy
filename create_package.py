__author__ = 'Ninad'


# rename existing package directory
# copy files...
# -- src/*.py
# -- example/
#  -- docs/
#  -- tests/
#  -- setup.py

import os
import sys
import shutil
import time

from src.addonpyHelpers import AddonHelper


if len(sys.argv) == 1:
    version_user = input("Please enter version #: ").rstrip()
else:
    version_user = sys.argv[1].rstrip()

x_time = time.localtime()
_SUFFIX = "{0}{1}{2}-{3:02d}{4:02d}{5:02d}".format(x_time.tm_year,
                                                   x_time.tm_mon,
                                                   x_time.tm_mday,
                                                   x_time.tm_hour,
                                                   x_time.tm_min,
                                                   x_time.tm_sec)

PACKAGE_DIR = 'package-{0}'.format(_SUFFIX)

CURR_DIR = os.path.abspath('.')
PKG_DIR = os.path.join(CURR_DIR, PACKAGE_DIR, 'addonpy')
SRC_DIR = os.path.join(CURR_DIR, 'src')
EXG_DIR = os.path.join(CURR_DIR, 'examples')
TST_DIR = os.path.join(CURR_DIR, 'tests')
DOC_DIR = os.path.join(CURR_DIR, 'docs')
SRPT_DIR = os.path.join(CURR_DIR, 'scripts')

if os.path.isdir(PKG_DIR):
    base_dir = os.path.dirname(PKG_DIR)
    backup_name = base_dir + '.old'
    if os.path.isdir(backup_name):
        shutil.rmtree(backup_name)
    os.rename(base_dir, backup_name)

os.makedirs(PKG_DIR)
print("Created fresh package directory...")

src_list = AddonHelper.walk_dir(SRC_DIR, 'py')

for file in src_list:
    shutil.copy2(file, PKG_DIR)

current_time = time.gmtime()
v_info = "{0}|[{1}-{2}-{3} {4}:{5}:{6} UTC]".format(version_user,
                                                    current_time.tm_year,
                                                    current_time.tm_mon,
                                                    current_time.tm_mday,
                                                    current_time.tm_hour,
                                                    current_time.tm_min,
                                                    current_time.tm_sec)

print("Package directory .... '{0}'".format(PACKAGE_DIR))
print("Copied source files...")

with open(os.path.join(PKG_DIR, '.version'), 'w') as v:
    v.write(v_info + "\n")

print("Created version file")

shutil.copytree(EXG_DIR, os.path.join(PKG_DIR, 'examples'))
print("Copied 'examples' dir...")

shutil.copytree(TST_DIR, os.path.join(PKG_DIR, 'tests'))
print("Copied 'tests' dir...")

shutil.copytree(DOC_DIR, os.path.join(PKG_DIR, 'docs'))
print("Copied 'doc' dir...")

shutil.copy2('setup.py', os.path.dirname(PKG_DIR))
print("Copied setup file")

shutil.copytree(SRPT_DIR, os.path.join(PKG_DIR, 'scripts'))
print("Copied script file")

os.chdir(PKG_DIR)

# pyc_list = AddonHelper.walk_dir(PKG_DIR, ext=['pyc'], recursive=True)
# for i in pyc_list:
# print("\t removing " + str(i))
# os.remove(i)

print("Running tests... locally")
os.system("python tests/run_tests.py local > tests/test.out 2>&1")

os.chdir('..')
print("Create package...")
os.system("python setup.py sdist")

print("Install package...")
os.system("python setup.py install")






