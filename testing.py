__author__ = 'alexey.nakoryakov'
"""
This file is just for testing purposes. In blender text window in test scene input something like
import bpy
import sys
import os

# This for relative import
dirname = path\\to\\module
if dirname not in sys.path:
    sys.path.append(dirname)

filename = os.path.join(dirname, "testing.py")
exec(compile(open(filename).read(), filename, 'exec'))
"""

import Bargool_1D_tools
import imp

imp.reload(Bargool_1D_tools)

Bargool_1D_tools.register()