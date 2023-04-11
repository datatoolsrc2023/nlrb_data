import os, sys
# Basically a multiplatform version of sys.path.append(os.getcwd() + '/..')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# We uppercase the Common/ package to avoid a conflict here
# If we lower-cased, then the common.py module (common) would instead try to import itself.
from Common import *
