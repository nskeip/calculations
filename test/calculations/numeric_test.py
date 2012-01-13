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