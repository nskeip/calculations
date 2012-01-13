import unittest
from calculations import semisimple
from calculations.partition import Partitions
from calculations.semisimple import SemisimpleElements, Signs

__author__ = 'Daniel Lytkin'

class SemisimpleTest(unittest.TestCase):
    def test_evaluate(self):
        ni = [8, 4, 4, 3, 2, 1]
        ei = [1, 1, -1, 1, -1, -1]
        q = 3
        r = semisimple.evaluate(q, ni, ei)
        self.assertEqual(75331760, r)

    def test_evaluate_minuses(self):
        ni = [8,7,4,3,1]
        q = 4
        r = semisimple.evaluate(q, ni)
        rp = semisimple.evaluate(q, ni, [-1]*len(ni))
        self.assertEqual(rp, r)

    def test_minus(self):
        """
        Test elements [q^{n_1}-1, ..., q^{n_k}-1] for all n_1+...+n_k=n
        """
        n = 10
        q = 4
        ss = SemisimpleElements(q, n, onlyMinus=True)
        allElements = (semisimple.evaluate(q, ni) for ni in Partitions(n))
        for elem in allElements:
            self.assertTrue(any(x % elem == 0 for x in ss))

    def test_signs(self):
        signs = list(Signs(4))
        expected = [[-1, -1, -1, -1], [1, -1, -1, -1],
            [-1, 1, -1, -1], [1, 1, -1, -1],
            [-1, -1, 1, -1], [1, -1, 1, -1],
            [-1, 1, 1, -1], [1, 1, 1, -1],
            [-1, -1, -1, 1], [1, -1, -1, 1],
            [-1, 1, -1, 1], [1, 1, -1, 1],
            [-1, -1, 1, 1], [1, -1, 1, 1],
            [-1, 1, 1, 1], [1, 1, 1, 1]]
        self.assertSequenceEqual(expected, signs)