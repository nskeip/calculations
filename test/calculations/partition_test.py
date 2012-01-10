import unittest
from calculations.partition import *


__author__ = 'Daniel Lytkin'

class PartitionTest(unittest.TestCase):
    def test_transpose(self):
        partition = Partition(8, 8, 6,5,3,3,3,1)
        transposed = partition.transpose()
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

    def test_pairs(self):
        p = list(Partitions(10, length=2))
        expected = [[9,1], [8,2], [7,3], [6,4], [5,5]]
        self.assertSequenceEqual(expected, p)

    def test_length(self):
        n = 10
        k = 5
        p = list(Partitions(n, length=k))
        expected = filter(lambda x: len(x)==k, Partitions(n))
        self.assertSequenceEqual(expected, p)

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

    def test_constraints(self):
        constraints = PartitionConstraints()
        self.assertTrue(constraints.isEmpty())

        constraints = PartitionConstraints(length=5, max_part=5)
        self.assertTrue(constraints.isValid([5, 2, 1, 1, 1]))
        self.assertFalse(constraints.isValid([5, 2, 1, 1]))

        constraints = PartitionConstraints(max_slope=2)
        self.assertTrue(constraints.isValid([5,5,3,1]))
        self.assertFalse(constraints.isValid([5,2,2,1]))

        constraints = PartitionConstraints(min_slope=2)
        self.assertTrue(constraints.isValid([6,4,2]))
        self.assertFalse(constraints.isValid([5,2,2,1]))

