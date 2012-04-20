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

__author__ = 'Daniel Lytkin'

class PointTest(unittest.TestCase):
    def test_sum(self):
        x1, y1 = 42, 24
        x2, y2 = 0.1, -0.3
        a = Point(x1, y1)
        b = Point(x2, y2)

        self.assertEqual((x1 + x2, y1 + y2), a + b)

    def test_diff(self):
        x1, y1 = 42, 24
        x2, y2 = 0.1, -0.3
        a = Point(x1, y1)
        b = Point(x2, y2)

        self.assertEqual((x1 - x2, y1 - y2), a - b)

    def test_neg(self):
        x, y = 1, 2
        a = Point(x, y)
        self.assertEqual((-x, -y), -a)

    def test_mult(self):
        x, y = 4.2, 2.4
        a = Point(x, y)
        c = 10

        self.assertEqual((float(x) * c, float(y) * c), a * c)
        self.assertEqual((float(x) * c, float(y) * c), c * a)

    def test_scalar_product(self):
        a = Point(2, 3)
        b = Point(0.1, 0.2)

        self.assertEqual(a.x * b.x + a.y * b.y, a * b)

    def test_div(self):
        x, y = 3, 4
        a = Point(x, y)
        c = 2

        self.assertEqual((float(x) / c, float(y) / c), a / c)

    def test_square(self):
        a = Point(4, 5)
        self.assertEqual(a.x * a.x + a.y * a.y, a.square())

