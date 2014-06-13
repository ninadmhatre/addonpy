__author__ = 'Ninad'

import os, sys

filename = os.path.basename(__file__)

def load():
    information = {
        'uuid': 'EEA8B330-A999-4D9F-89AB-D341330B619F',
        'description': 'This is hook_test1 module',
        'sequence': [
            'start',
            'stop'
        ],
       'version': {
            'major': 1,
            'minor': 0,
            'patch': 5,
        }
    }

    return information