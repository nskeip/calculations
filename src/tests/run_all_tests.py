import unittest

__author__ = 'Daniel Lytkin'

unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('.', '*_test.py'))
