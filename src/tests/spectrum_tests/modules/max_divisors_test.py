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
from spectrum.modules.max_divisors import first_primes, primes_less_than, is_prime

__author__ = 'Daniel Lytkin'

class MaxDivisorsTest(unittest.TestCase):
    def test_first_primes(self):
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        for i in range(1, 13):
            self.assertEqual(expected[:i], first_primes(i))

    def test_primes_less_than(self):
        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        self.assertEqual(expected[:-1], primes_less_than(35))
        self.assertEqual(expected, primes_less_than(40))

    def test_is_prime(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        for p in primes:
            self.assertTrue(is_prime(p))

        non_primes = [4, 6, 8, 10, 27, 82]
        for n in non_primes:
            self.assertFalse(is_prime(n))