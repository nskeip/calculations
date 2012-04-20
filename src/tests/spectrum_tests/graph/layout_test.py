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
from spectrum.graph.geometry import Point
from spectrum.graph.graph import Graph
from spectrum.graph.layout import Layout

__author__ = 'Daniel Lytkin'

class LayoutTest(unittest.TestCase):
    def setUp(self):
        self.graph = Graph(range(5))
        self.graph.add_edges({(0, 1), (1, 2), (1, 3), (2, 3), (3, 4), (2, 4)})
        self.layout = Layout(self.graph, default_location=(0.42, 0.42))

    def test_setLocation(self):
        self.assertEquals((0.42, 0.42), self.layout[0])
        self.layout[1] = Point(1, 1)
        self.assertEquals((1, 1), self.layout[1])

        self.layout.reset()
        self.assertEquals((0.42, 0.42), self.layout[1])
