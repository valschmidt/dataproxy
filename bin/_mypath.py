# Python Path Fixing
#
# Makes the local libraries accessible to scripts in this directory.
# 
# add 'import _mypath' to each file.
#
# See: 
# http://intermediate-and-advanced-software-carpentry.readthedocs.org/en/latest/structuring-python.html
#
# Val Schmidt
# Center for Coastal and Ocean Mapping
# University of New Hampshire
# 2016

import os, sys
thisdir = os.path.dirname(__file__)
libdir = os.path.join(thisdir, '../lib')

if libdir not in sys.path:
    sys.path.insert(0, libdir)
