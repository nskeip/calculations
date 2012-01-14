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
        n = 20
        q = 5
        ss = SemisimpleElements(q, n, minus=True)
        for ni in Partitions(n):
            elem = semisimple.evaluate(q, ni)
            self.assertTrue(any(x % elem == 0 for x in ss), msg=str(ni))

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

    def test_all_semisimple(self):
        # very slow! For every partition of size n it calculates 2^n sign tuples.
        n = 12
        q = 5
        ss = list(SemisimpleElements(q, n))

        for ni in Partitions(n):
            for ei in Signs(len(ni)):
                elem = semisimple.evaluate(q, ni, ei)
                self.assertTrue(any(x % elem == 0 for x in ss),
                    msg="element with base {}, partition {} and signs {} = {} " \
                        "doesn't divide any of {}".format(str(q), str(ni), str(ei), str(elem), str(ss)))