from Partition import Partition
import unittest

__author__ = 'Daniel Lytkin'

class PartitionsTest(unittest.TestCase):
    def test_transpose(self):
        partition = [8, 8, 6,5,3,3,3,1]
        transposed = Partition.transpose(partition)
        self.assertEqual(sum(partition), sum(transposed))
        self.assertEqual(transposed, [8, 7, 7, 4, 4, 3, 2, 2])



if __name__ == '__main__':
    unittest.main()