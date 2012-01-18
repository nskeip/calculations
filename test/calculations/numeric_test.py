from collections import Counter
import unittest
from calculations.numeric import *

__author__ = 'Daniel Lytkin'

class NumericTest(unittest.TestCase):
    def test_gcd(self):
        a, b = 30, 12
        c = gcd(a, b)
        # c must divide both a and b
        self.assertTrue(a % c == 0)
        self.assertTrue(b % c == 0)
        # and must be the greatest divisor
        self.assertTrue(all(a % t > 0 or b % t > 0 for t in range(c+1, min(a,b)+1)))

    def test_lcm(self):
        a, b = 30, 12
        c = lcm(a, b)
        # c must me divisible by both a and b
        self.assertTrue(c % a == 0)
        self.assertTrue(c % b == 0)
        self.assertTrue(all(t % a > 0 or t % b > 0 for t in range(max(a, b), c)))

    def test_filterDivisors(self):
        a = filterDivisors([10, 9, 7, 6, 5, 4, 3])
        expected = [10, 9, 7, 6, 4]
        self.assertSequenceEqual(expected, a)

    def test_filterDivisors_reversed(self):
        a = filterDivisors([10, 9, 7, 6, 5, 4, 3], reverse=True)
        expected = [4, 6, 7, 9, 10]
        self.assertSequenceEqual(expected, a)

    def test_first_divisor(self):
        self.assertEqual(3, firstDivisor(9))
        self.assertEqual(41, firstDivisor(41))

    def test_next_odd_divisor(self):
        self.assertEqual(13, nextOddDivisor(13, 1))
        self.assertEqual(5, nextOddDivisor(35, 3))
        self.assertEqual(7, nextOddDivisor(49, 3))

    def test_factors(self):
        expected = Counter({2:10, 3:7, 5:3, 7:1, 11:1, 23:1})
        factors = Integer(495766656000).factors()
        self.assertEqual(expected, factors)

    def test_product(self):
        expected = 495766656000
        product = int(Integer((2, 10), (3, 7), (5, 3), 7, 11, 23))
        self.assertEqual(expected, product)