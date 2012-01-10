import unittest
from calculations.partition import Partitions
from calculations.set import *

__author__ = 'Daniel Lytkin'

class SetTest(unittest.TestCase):
    def test_sets(self):
        sets = list(BoundedSets(10))
        expected = [[10], [9, 1], [9], [8, 2], [8, 1], [8], [7, 3], [7, 2, 1],
            [7, 2], [7, 1], [7], [6, 4], [6, 3, 1], [6, 3], [6, 2, 1], [6, 2],
            [6, 1], [6], [5, 4, 1], [5, 4], [5, 3, 2], [5, 3, 1], [5, 3],
            [5, 2, 1], [5, 2], [5, 1], [5], [4, 3, 2, 1], [4, 3, 2], [4, 3, 1],
            [4, 3], [4, 2, 1], [4, 2], [4, 1], [4], [3, 2, 1], [3, 2], [3, 1],
            [3], [2, 1], [2], [1]]
        self.assertSequenceEqual(expected, sets)

    def test_maximal_sets(self):
        sets = list(BoundedSets(10, maximal=True))
        expected = [[10], [9, 1], [8, 2], [8, 1], [7, 3], [7, 2, 1],
                    [6, 4], [6, 3, 1], [6, 2, 1],
                    [5, 4, 1], [5, 3, 2], [5, 3, 1],
                    [5, 2, 1], [4, 3, 2, 1]]
        self.assertSequenceEqual(expected, sets)

    def test_minus_partitions(self):
        n = 20
        minusPartitions = list(BoundedSets(n, maximal=True))
        allPartitions = list(Partitions(n))

        # every partition must have every its element contained in some minus-partition
        self.assertTrue(all(
            any(set(partition)<=set(mPartition) for mPartition in minusPartitions)
            for partition in allPartitions))
