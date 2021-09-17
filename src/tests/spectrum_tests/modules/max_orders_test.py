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

from spectrum_tests.parametric import parametrized, parameters

from spectrum.calculations import numeric
from spectrum.calculations.groups import ClassicalGroup
from spectrum.modules import max_orders

__author__ = 'Daniel Lytkin'

def max_elements(set, num_elements=1):
    set = list(set)
    set.sort(reverse=True)
    return set[:num_elements]


def maximal_orders(group, num_elements=1):
    return max_elements(group.apex(), num_elements=num_elements)


@parametrized
class MaxOrdersTest(unittest.TestCase):
    @parameters(list(range(3, 26)))
    def test_symplectic(self, n):
        group = ClassicalGroup("Sp", 2 * n, 2)
        max_elems = max_orders.maximal_orders(group)
        max_elems_2 = maximal_orders(group, 2)
        self.assertEqual(max_elems[0], max_elems_2[0])
        self.assertEqual(max_elems[1], max_elems_2[1])

    @parameters(list(range(3, 100)))
    def test_symplectic_gcd(self, n):
        max_elems = max_orders.symplectic_2(n)
        expected = numeric.gcd(*max_elems)
        self.assertEqual(expected, max_orders.symplectic_2_gcd(n))