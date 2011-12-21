import unittest
from calculations.Partition import *

__author__ = 'Daniel Lytkin'

class PartitionsTest(unittest.TestCase):
    def test_transpose(self):
        partition = Partition([8, 8, 6,5,3,3,3,1])
        transposed = partition.transpose()
        self.assertEqual(sum(partition), sum(transposed))
        self.assertEqual(transposed, [8, 7, 7, 4, 4, 3, 2, 2])

    def test_next(self):
        allPartitions = []
        for p in Partitions(10):
            allPartitions.append(p)

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


#if __name__ == '__main__':
#    unittest.main()