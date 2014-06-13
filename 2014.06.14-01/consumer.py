__author__ = 'Ninad'

import os, sys
from AddonLoader import AddonLoader as al

t = al(verbose=True)

import pprint as pp

pp.pprint(t.config)