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
import unittest
from spectrum.tools.observers import Observable

__author__ = 'Daniel Lytkin'


class ObservableTest(unittest.TestCase):
    def setUp(self):
        self.s = Observable()

    def test_listeners(self):
        called = [False, False]# if listeners were called
        lst = list()

        def listener1(item):
            called[0] = True
            lst.append(item)

        def listener2(item):
            called[1] = True
            lst.append(item)

        self.s.add_listener(listener1)
        self.s.add_listener(listener2)
        self.assertSequenceEqual(self.s.listeners, [listener1, listener2])

        self.s.notify("42")
        self.assertTrue(called[0])
        self.assertTrue(called[1])
        self.assertSequenceEqual(lst, ["42"] * 2)

        self.s.remove_listener(listener1)
        self.assertEqual(1, len(self.s.listeners))
