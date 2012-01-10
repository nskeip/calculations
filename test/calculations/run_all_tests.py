import unittest
import sys
sys.path.append("../../src")

__author__ = 'Daniel Lytkin'

unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('.', '*_test.py'))
