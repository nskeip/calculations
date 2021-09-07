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

from spectrum.calculations.partition import *
from spectrum_tests.parametric import parametrized, parameters

__author__ = 'Daniel Lytkin'

@parametrized
class PartitionTest(unittest.TestCase):
    def test_transpose(self):
        partition = [8, 8, 6, 5, 3, 3, 3, 1]
        transposed = Partitions.transpose(partition)
        self.assertEqual(sum(partition), sum(transposed))
        self.assertEqual(transposed, [8, 7, 7, 4, 4, 3, 2, 2])

    def test_partition(self):
        allPartitions = list(Partitions(10))

        expected = [[10], [9, 1], [8, 2], [8, 1, 1], [7, 3],
            [7, 2, 1], [7, 1, 1, 1], [6, 4], [6, 3, 1],
            [6, 2, 2], [6, 2, 1, 1], [6, 1, 1, 1, 1],
            [5, 5], [5, 4, 1], [5, 3, 2], [5, 3, 1, 1],
            [5, 2, 2, 1], [5, 2, 1, 1, 1], [5, 1, 1, 1, 1, 1],
            [4, 4, 2], [4, 4, 1, 1], [4, 3, 3], [4, 3, 2, 1],
            [4, 3, 1, 1, 1], [4, 2, 2, 2], [4, 2, 2, 1, 1],
            [4, 2, 1, 1, 1, 1], [4, 1, 1, 1, 1, 1, 1],
            [3, 3, 3, 1], [3, 3, 2, 2], [3, 3, 2, 1, 1],
            [3, 3, 1, 1, 1, 1], [3, 2, 2, 2, 1],
            [3, 2, 2, 1, 1, 1], [3, 2, 1, 1, 1, 1, 1],
            [3, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2],
            [2, 2, 2, 2, 1, 1], [2, 2, 2, 1, 1, 1, 1],
            [2, 2, 1, 1, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        self.assertSequenceEqual(expected, allPartitions)

    @parameters(
        list(filter(lambda pair: pair[0] > pair[1], itertools.combinations(range(1, 10), 2))))
    def test_first_fixed_length_partition(self, params):
        n, k = params
        p = next(Partitions(n, length=k).__iter__())
        expected = [n - k + 1] + [1] * (k - 1)
        self.assertSequenceEqual(p, expected)


    def test_pairs(self):
        p = list(Partitions(10, length=2))
        expected = [[9, 1], [8, 2], [7, 3], [6, 4], [5, 5]]
        self.assertSequenceEqual(expected, p)

    @parameters(
        list(filter(lambda pair: pair[0] > pair[1], itertools.combinations(range(1, 10), 2))))
    def test_length(self, params):
        # self.maxDiff = None
        n, k = params
        p = list(Partitions(n, length=k))
        expected = [x for x in Partitions(n) if len(x) == k]
        self.assertSequenceEqual(expected, p)

    def test_invalid_length(self):
        n = 10
        k = 11
        p = list(Partitions(n, length=k))
        self.assertSequenceEqual([], p)

    def test_max_part(self):
        p = list(Partitions(10, max_part=5))
        expected = [[5, 5], [5, 4, 1], [5, 3, 2],
            [5, 3, 1, 1], [5, 2, 2, 1], [5, 2, 1, 1, 1],
            [5, 1, 1, 1, 1, 1], [4, 4, 2], [4, 4, 1, 1],
            [4, 3, 3], [4, 3, 2, 1], [4, 3, 1, 1, 1],
            [4, 2, 2, 2], [4, 2, 2, 1, 1],
            [4, 2, 1, 1, 1, 1], [4, 1, 1, 1, 1, 1, 1],
            [3, 3, 3, 1], [3, 3, 2, 2], [3, 3, 2, 1, 1],
            [3, 3, 1, 1, 1, 1], [3, 2, 2, 2, 1],
            [3, 2, 2, 1, 1, 1], [3, 2, 1, 1, 1, 1, 1],
            [3, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2],
            [2, 2, 2, 2, 1, 1], [2, 2, 2, 1, 1, 1, 1],
            [2, 2, 1, 1, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.assertSequenceEqual(expected, p)

    def test_min_part(self):
        p = list(Partitions(10, min_part=3))
        expected = [[10], [7, 3], [6, 4], [5, 5], [4, 3, 3]]
        self.assertSequenceEqual(expected, p)

    def test_max_length(self):
        p = list(Partitions(10, max_length=3))
        expected = [[10], [9, 1], [8, 2], [8, 1, 1], [7, 3],
            [7, 2, 1], [6, 4], [6, 3, 1], [6, 2, 2], [5, 5],
            [5, 4, 1], [5, 3, 2], [4, 4, 2], [4, 3, 3]]
        self.assertSequenceEqual(expected, p)

    def test_min_length(self):
        p = list(Partitions(10, min_length=8))
        expected = [[3, 1, 1, 1, 1, 1, 1, 1],
            [2, 2, 1, 1, 1, 1, 1, 1],
            [2, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.assertSequenceEqual(expected, p)

    def test_max_slope(self):
        p = list(Partitions(10, max_slope=2))
        expected = [[5, 3, 2], [5, 3, 1, 1], [4, 4, 2],
            [4, 3, 2, 1], [4, 3, 1, 1, 1], [4, 2, 2, 2],
            [4, 2, 2, 1, 1], [4, 2, 1, 1, 1, 1],
            [3, 3, 3, 1], [3, 3, 2, 2], [3, 3, 2, 1, 1],
            [3, 3, 1, 1, 1, 1], [3, 2, 2, 2, 1],
            [3, 2, 2, 1, 1, 1], [3, 2, 1, 1, 1, 1, 1],
            [3, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2],
            [2, 2, 2, 2, 1, 1], [2, 2, 2, 1, 1, 1, 1],
            [2, 2, 1, 1, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.assertSequenceEqual(expected, p)

    def test_min_slope(self):
        p = list(Partitions(10, min_slope=2))
        expected = [[10], [8, 2], [7, 3], [6, 4]]
        self.assertSequenceEqual(expected, p)
