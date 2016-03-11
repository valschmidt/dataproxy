# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 13:32:13 2016

@author: vschmidt
"""

import os, sys
thisdir = os.path.dirname(__file__)
libdir = os.path.join(thisdir, '../lib')

if libdir not in sys.path:
    sys.path.insert(0, libdir)
