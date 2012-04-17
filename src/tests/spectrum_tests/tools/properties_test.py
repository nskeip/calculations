from Tkinter import StringVar, Tk
import unittest
from spectrum.tools.tools import Properties

__author__ = 'Daniel Lytkin'


class PropertiesTest(unittest.TestCase):
    def setUp(self):
        Tk()
        self.properties = Properties()


    def test_variable(self):
        var = StringVar()
        self.properties.add_variable('var', var, initial="42")
        self.assertEqual("42", var.get())
        self.assertEqual("42", self.properties['var'])

        var.set("test")
        self.assertEqual("test", self.properties['var'])

        self.properties['var'] = "test2"
        self.assertEqual("test2", var.get())

    def test_non_variable(self):
        self.properties['test'] = 42
        self.assertEqual(42, self.properties['test'])

        with self.assertRaises(KeyError):
            print self.properties['missing']

