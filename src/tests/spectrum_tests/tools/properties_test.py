"""
Copyright 2012 Daniel Lytkin.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""
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

