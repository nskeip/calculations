import unittest
from calculations.partition import Partitions
from calculations.set import *

__author__ = 'Daniel Lytkin'

class SetTest(unittest.TestCase):
    @staticmethod
    def filterContained(sets):
        """
        Returns only those sets, that are not contained in any other set
        """
        return filter(lambda x: not any(set(x)<set(y) for y in sets), sets)

    def test_next_bounded_set(self):
        expected = [4, 3, 2, 1]
        self.assertSequenceEqual(expected, BoundedSets.next([5], 10))

    def test_next_maximal_set(self):
        expected = [4, 3, 2, 1]
        self.assertSequenceEqual(expected, BoundedSets.nextMaximal([5, 2, 1], 10))

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
        """
        Maximal sets are exactly the sets that are not contained in any other
        """
        n = 20
        sets = list(BoundedSets(n, maximal=True))
        expected = self.filterContained(list(BoundedSets(n)))
        self.assertSequenceEqual(expected, sets)

    def test_containing_partitions(self):
        """
        Every partition must have the set of its parts contained in some bounded set for the same n.
        We only need sets that are maximal by containment
        """
        n = 20
        minusPartitions = list(BoundedSets(n, maximal=True))
        allPartitions = list(Partitions(n))

        # every partition must have every its element contained in some minus-partition
        self.assertTrue(all(
            any(set(partition)<=set(mPartition) for mPartition in minusPartitions)
            for partition in allPartitions))

    def test_zero_bound(self):
        sets = list(BoundedSets(0))
        self.assertSequenceEqual([[]], sets)