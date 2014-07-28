__author__ = 'Ninad'

import os
import shutil


def walk_dir_for_files():
    print("Getting list of all *.pyc files...")
    file_list = list()
    for abs_dir_path, dir_path, files in os.walk('.'):
        if len(files) > 0:
            for file in files:
                abs_file = os.path.join(abs_dir_path, file)
                if abs_file.endswith('.pyc'):
                    file_list.append(abs_file)

    return file_list


def walk_dir_for_dirs():
    print("Getting list of all '__pycache__' directories...")
    file_list = dict()
    for abs_dir_path, dir_path, files in os.walk('.'):
        if abs_dir_path.endswith('__pycache__'):
            file_list[abs_dir_path] = len(files)
    return file_list


def operate_on_dir(dir_list, display=True):
    for c_dir in dir_list.keys():
        if display:
            print("Directory : '{0}' Files : '{1}'".format(c_dir, dir_list[c_dir]))
        else:
            print("Going to remove '{0}' dir".format(c_dir))
            try:
                shutil.rmtree(c_dir)
            except Exception:
                print("\t...failed")
            else:
                print("\t...deleted")


cache_files = walk_dir_for_files()
for c_file in cache_files:
    try:
        os.remove(c_file)
    except Exception:
        print("Error: Failed to delete '{0}'".format(c_file))
    else:
        print("Info: Successfully deleted '{0}'".format(c_file))

cache_dirs = walk_dir_for_dirs()

if len(cache_dirs) > 0:
    operate_on_dir(cache_dirs, True)
    answer = input("Do you want to delete above directories...? ")
    print("answer is '{0}'".format(answer))
    if answer.lower() in ['y', 'yes']:
        operate_on_dir(cache_dirs, False)
else:
    print("There are no '__pycache__' directories....")