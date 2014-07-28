#
# This is pretty beta stage of this script. It works if you are not trying to break it :)
# Requires: addonpy to be installed
# - Very little testing done
# - No test cases...
# - Find any issue? report on GitHub

# Changes:
#   0.1 : 18-Jul-2014 : Initial version
#   0.2 : 23-Jul-2014 : Added support for user specific templates
#                       Bit of documentation

__author__ = 'Ninad Mhatre'
__version__ = '0.2.0'

import os
from os.path import abspath, join, dirname
import sys
import argparse
from addonpy.addonpyHelpers import AddonHelper as helper

INFO_TEMPLATE = """{
    "uuid": "$UUID",
    "name": "$ADDON_NAME",
    "type": "$TYPE",
    "description": "$DESCRIPTION",
    "execution_seq": $START_SEQUENCE,
    "stop_seq": $STOP_SEQUENCE,
    "version": "$VERSION",
    "author": "$AUTHOR",
    "help_url": "$HELP_URL"
}
"""

ADDON_TEMPLATE = """__author__ = '$AUTHOR'

from addonpy.IAddonInfo import IAddonInfo


class $ADDON_NAME(IAddonInfo):
    def $START_FUNCTION(self):
        raise NotImplemented

    def $STOP_FUNCTION(self):
        raise NotImplemented

    def $EXECUTE_FUNCTION(self):
        raise NotImplemented

    @staticmethod
    def __addon__():
        return '$ADDON_NAME'
"""

parser = argparse.ArgumentParser()

parser.add_argument('--name', '-n', help="Provide name for Addon e.g 'Test' or 'TestAddon'")
parser.add_argument('--conf', '-c', help="Provide path to config file")
parser.add_argument('--noinfo', '-ni', help="[Optional] Do not generate .info file for addon", action='store_true')
parser.add_argument('--info-template', '-it', help="[Optional] Path to info template file")
parser.add_argument('--addon-template', '-at', help="[Optional] Path to addon template file")
parser.add_argument('--type', '-t', help="[Optional] Override Type specified in config file")
parser.add_argument('--desc', '-d', help="[Optional] Override Description specified in config file")
parser.add_argument('--author', '-a', help="[Optional] Override Author specified in config file")
parser.add_argument('--outdir', '-o', help="[Optional] Provide where to create files. Default: current directory",
                    default=abspath('.'))
parser.add_argument('--version', '-v', help="[Optional] Provide version number for addon. Default: 1.0.0")
parser.add_argument('--fullhelp', '-fh', help="Show help with some examples", action='store_true')

options = parser.parse_args()


def main():
    validate()
    config = parse_config()
    addon = generate_addon(config)
    info = generate_info(config)
    create(addon, info)


def create(addon, info):
    if addon is not None:
        file_name = join(options.outdir, '{0}.py'.format(options.name))
        _create_file(file_name, addon)
        print("created addon file: {0}".format(file_name))

    if info is not None:
        file_name = join(options.outdir, '{0}.info'.format(options.name))
        _create_file(file_name, info)
        print("created addon info file: {0}".format(file_name))


def _create_file(file_name, contents):
    with open(file_name, 'w') as write:
        write.write(contents)


def display_help():
    x = 'addon_generator'

    print("""

    Desc  : Generate addon from given or default template (VERSION : {1})

    Usage : Run '{0} -h' for parameters related info

    E.g.  :

    1. {0} -n Test -c ./template.conf
       - Create 'TestAddon.py' and 'TestAddon.info' in current directory with 'DEFAULT' templates using values specified
         in 'template.conf' in current file.

    2. {0} -n Test -c ./template.conf -o /tmp
       - Same as #1, but files are created in /tmp

    3. {0} -n Test -c ./template.conf -ni
       - Same as #1, but .info file is not created

    4. {0} -n Test -c ./template.conf --type X --desc 'Abcd X' --author 'X-1 Team' --version '1.0-beta'
       - Same as #1, but overrides Type, Author & Version values from '.conf' file. '--desc' is always picked from
         argument.

    5. {0} -n Test -c ./template.conf -ni -it /tmp/info.template -at /tmp/addon.x
       - Same as #1, but info template and addon template are specified by user. User can choose to specify either, both
       or none.

    Note: Template extensions DO NOT matter!

    Variables:

       Common for Addon & .info:
            $ADDON_NAME
            $AUTHOR

       Addon Template:
            $AUTHOR
            $START_FUNCTION
            $STOP_FUNCTION
            $EXECUTE_FUNCTION
            OTHER_FUNCTIONS - Defined in template.conf as CSV and these will be created as functions in generated file.

       Info Templates:
            $UUID  - Auto generated
            $HELP_URL - Can have '$ADDON_NAME' as part of URL
            $TYPE
            $DESCRIPTION
            $START_SEQUENCE
            $STOP_SEQUENCE
            $VERSION
    """.format(x, __version__))


def validate():

    if options.fullhelp:
        display_help()
        sys.exit(0)

    if options.name is None:
        parser.print_help()
        sys.exit(9)

    if not options.name.endswith('Addon'):
        options.name += "Addon"

    if options.conf is None or not os.path.isfile(options.conf):
        print("Error: Please provide config file argument! or mentioned file does not exist!")
        sys.exit(9)

    if options.outdir is not None and not os.path.isdir(options.outdir):
        print("Error: Output directory '{0}' does not exist".format(options.outdir))
        sys.exit(9)

    if options.info_template:
        if not os.path.isfile(options.info_template):
            print("Error: Info file template '{0}' mentioned not found".format(options.info_template))
            sys.exit(9)
        else:
            global INFO_TEMPLATE
            INFO_TEMPLATE = helper.read_file(options.info_template)
    else:
        options.info_template = "Default"

    if options.addon_template:
        if not os.path.isfile(options.addon_template):
            print("Error: Info file template '{0}' mentioned not found".format(options.addon_template))
            sys.exit(9)
        else:
            global ADDON_TEMPLATE
            ADDON_TEMPLATE = helper.read_file(options.addon_template)
    else:
        options.addon_template = "Default"

    print("""
    Validation Finished...

    Addon Name          : {0}
    Description         : {1}
    Generate .info file : {2}
    config file         : {3}
    Output directory    : {4}
    .info template      : {5}
    addon template      : {6}
    """.format(options.name,
               options.desc,
               "Yes" if not options.noinfo else "No",
               options.conf,
               options.outdir,
               options.info_template,
               options.addon_template))


def parse_config():

    try:
        config = helper.parse_info_file(options.conf)
    except ValueError:
        print("Error: Invalid config file '{0}' please make sure config is valid JSON".format(options.conf))
        sys.exit(9)

    return config


def generate_addon(cf):
    """
    addon templatizer. Supports following variables
    $AUTHOR, $ADDON_NAME, $START_FUNCTION, $STOP_FUNCTION, $EXECUTE_FUNCTION
    :param cf: config file
    :return: text replaced file with values from config file
    """
    addon_template = ADDON_TEMPLATE
    addon_template = addon_template.replace('$AUTHOR', _get_author(cf))
    addon_template = addon_template.replace('$ADDON_NAME', options.name)
    addon_template = addon_template.replace('$START_FUNCTION', cf.get('START_FUNCTION', '<INVALID>'))
    addon_template = addon_template.replace('$STOP_FUNCTION', cf.get('STOP_FUNCTION', '<INVALID>'))
    addon_template = addon_template.replace('$EXECUTE_FUNCTION', cf.get('EXECUTE_FUNCTION', '<INVALID>'))

    text = "\n\n    def {0}(self):\n        raise NotImplemented"

    if cf.get('OTHER_FUNCTIONS'):
        for function in cf.get('OTHER_FUNCTIONS').split(','):
            addon_template += text.format(function)

    #print(addon_template)
    return addon_template


def generate_info(cf):
    """
    addon template, supports following variables
    $UUID, $HELP_URL, $ADDON_NAME, $TYPE, $DESCRIPTION, $START_SEQUENCE, $STOP_SEQUENCE, $VERSION, $AUTHOR
    :param cf: config file with values for above variables
    :return: templatized file.
    """
    if options.noinfo:
        print("Info file will not be generated...")
        return None

    info_template = INFO_TEMPLATE
    import uuid
    uid = uuid.uuid4().urn.split(':')[2]
    info_template = info_template.replace('$UUID', uid)
    info_template = info_template.replace('$HELP_URL', _get_help_url(cf))
    info_template = info_template.replace('$ADDON_NAME', options.name)
    info_template = info_template.replace('$TYPE', _get_type(cf))
    info_template = info_template.replace('$DESCRIPTION', _get_desc())
    info_template = info_template.replace('$START_SEQUENCE', _get_sequence(cf, 'first'))
    info_template = info_template.replace('$STOP_SEQUENCE', _get_sequence(cf, 'last'))
    info_template = info_template.replace('$VERSION', _get_version())
    info_template = info_template.replace('$AUTHOR', _get_author(cf))
    # os_info = _get_os(cf)
    # if os_info != 'ALL':
    #     info_template = info_template.replace('}', '')
    #     info_template += ('    "OS": {0}\n'.format(os_info))
    #     info_template += '}'

    #print(info_template)
    return info_template


def _get_os(cf):
    val = cf.get('OS', 'ALL')
    if val != 'ALL':
        return _convert_to_list_str(val)
    else:
        return val


def _get_author(cf):
    import getpass
    val = options.author
    if val and val is not None:
        return val
    else:
        return cf.get('AUTHOR', getpass.getuser())


def _get_type(cf):
    val = options.type
    if val and val is not None:
        return val
    else:
        return cf.get('TYPE', "BASIC")


def _get_desc():
    val = options.desc
    if val and val is not None:
        return val
    else:
        return "<Please add some description!>"


def _get_version():
    val = options.version
    if val and val is not None:
        return val
    else:
        return '1.0.0'


def _get_help_url(cf):
    val = cf.get('HELP_URL', 'please create one!')
    if val and val is not None:
        return val


def _get_sequence(cf, which):
    if which == 'first':
        val = cf.get('START_SEQUENCE', 'start, execute')
    else:
        val = cf.get('STOP_SEQUENCE', 'stop')

    if val and val is not None:
        return _convert_to_list_str(val)


def _convert_to_list_str(sequence):
    x = '['
    for i in sequence.split(','):
        x += '"{0}", '.format(i.lstrip())
    x = x.rstrip(', ')
    x += ']'
    return x

if __name__ == '__main__':
    main()