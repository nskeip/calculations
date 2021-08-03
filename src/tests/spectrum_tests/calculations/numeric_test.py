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
import itertools
import unittest

from spectrum_tests.parametric import parametrized, parameters

from spectrum.calculations.numeric import *

__author__ = 'Daniel Lytkin'

@parametrized
class NumericTest(unittest.TestCase):
    @parameters(itertools.combinations(range(1, 30), 2))
    def test_gcd(self, params):
        a, b = params
        c = gcd(a, b)
        # c must divide both a and b
        self.assertTrue(a % c == 0)
        self.assertTrue(b % c == 0)
        # and must be the greatest divisor
        self.assertTrue(
            all(a % t > 0 or b % t > 0 for t in range(c + 1, min(a, b) + 1)))

    @parameters(itertools.combinations(range(1, 30), 2))
    def test_lcm(self, params):
        a, b = params
        c = lcm(a, b)
        # c must me divisible by both a and b
        self.assertTrue(c % a == 0)
        self.assertTrue(c % b == 0)
        self.assertTrue(
            all(t % a > 0 or t % b > 0 for t in range(max(a, b), c)))

    def test_primePart(self):
        self.assertEqual(13, prime_part(26, 6))
        self.assertEqual(12, prime_part(60, 25))
        self.assertEqual(1, prime_part(125, 5))

    def test_filterDivisors_reversed(self):
        a = filter_divisors([10, 9, 7, 6, 5, 4, 3], reverse=True)
        expected = [10, 9, 7, 6, 4]
        self.assertSequenceEqual(expected, a)

    def test_filterDivisors(self):
        a = filter_divisors([10, 9, 7, 6, 5, 4, 3])
        expected = [4, 6, 7, 9, 10]
        self.assertSequenceEqual(expected, a)

    def test_sortAndFilter(self):
        a = [9, 8, 21, 7, 12, 6, 5, 15, 10, 5, 4, 12, 4, 4, 3, 6, 3, 6, 3, 2, 2
            , 1]
        expected = [21, 15, 12, 10, 9, 8]
        self.assertSequenceEqual(expected, sort_and_filter(a, reverse=True))

    def test_first_divisor(self):
        self.assertEqual(3, first_divisor(9))
        self.assertEqual(41, first_divisor(41))

    def test_next_odd_divisor(self):
        self.assertEqual(13, next_odd_divisor(13, 1))
        self.assertEqual(5, next_odd_divisor(35, 3))
        self.assertEqual(7, next_odd_divisor(49, 3))

    def test_factors(self):
        expected = Counter({2: 10, 3: 7, 5: 3, 7: 1, 11: 1, 23: 1})
        i = Integer(495766656000)
        i.factorize()
        self.assertEqual(expected, i.factors)

    def test_product(self):
        expected = 495766656000
        product = int(Integer((2, 10), (3, 7), (5, 3), 7, 11, 23))
        self.assertEqual(expected, product)

    def test_mult(self):
        expected = 495766656000
        a = Integer((2, 10), (3, 7), 11, 23)
        b = Integer((5, 3), 7)
        a *= b
        self.assertEqual(expected, int(a))

    #    def test_div(self):
    #        expected = 9504
    #        a = Integer(495766656000)
    #        b = Integer(52164000)
    #        c = a / b
    #        self.assertEqual(expected, c)

    def test_div_by_prime(self):
        a = Integer((525, 2), 244, 2, 32)
        expected1 = Integer((525, 2), 244, 32)
        expected2 = Integer((525, 2), 122, 2, 32)
        a.div_by_prime(2)
        self.assertEqual(expected1, a)
        self.assertEqual(expected2, a)

    def test_is_prime(self):
        expected = {2: True, 3: True, 4: False, 5: True, 3569: False,
                    3571: True, 27644437: True, 27644439: False,
                    15485863: True}
        for number, value in expected.items():
            self.assertEqual(value, is_prime(number), msg=number)

    def test_is_prime_power(self):
        expected = {2: True, 3: True, 4: True, 5: True, 6: False, 128: True,
                    81: True, 82: False}
        for number, value in expected.items():
            self.assertEqual(value, is_prime_power(number), msg=number)

    def test_closest_prime(self):
        expected = {2: 2, 3: 3, 4: 3, 95: 97}
        for number, value in expected.items():
            self.assertEqual(value, closest_prime(number), msg=number)

    def test_closest_prime_power(self):
        expected = {2: 2, 3: 3, 4: 4, 6: 5, 95: 97, 130: 131, 34: 32}
        for number, value in expected.items():
            self.assertEqual(value, closest_prime_power(number), msg=number)

    def test_binary_expansion(self):
        expected = [32, 8, 4, 1]
        self.assertEqual(expected, binary_expansion(45))

    def test_mod(self):
        a = Integer((2, 2), 3)
        b = 7
        self.assertEqual(5, a % b)

    def test_getExponent(self):
        values = {(36, 6): 2,
                  (128, 2): 7,
                  (12, 2): None,
                  (42, 1): None,
                  (13, 13): 1,
                  (1, 42): 0
        }
        for key, value in values.iteritems():
            self.assertTrue(get_exponent(*key) == value)

    def test_is_power_of_two(self):
        values = {1: True,
                  2: True,
                  3: False,
                  4: True,
                  5: False,
                  7: False,
                  8: True,
                  1024: True,
                  2050: False}
        for key, value in values.iteritems():
            self.assertEqual(value, is_power_of_two(key))

    def test_constraints(self):
        c = Constraints(min=5, primality=PRIME)
        self.assertTrue(c.is_valid(5))
        self.assertFalse(c.is_valid(6))
        self.assertFalse(c.is_valid(3))
        self.assertEqual(7, c.closest_valid(8))

        c = Constraints(min=20, primality=PRIME_POWER)
        self.assertTrue(c.is_valid(25))
        self.assertFalse(c.is_valid(19))
        self.assertFalse(c.is_valid(26))

        c = Constraints(min=5, primality=PRIME, parity=1)
        self.assertTrue(c.closest_valid(5) is None)

        c = Constraints(min=8, primality=PRIME_POWER, parity=1)
        self.assertEqual(8, c.closest_valid(5))