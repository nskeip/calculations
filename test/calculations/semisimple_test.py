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

        divisible = set()
        for ni in Partitions(n):
            elem = semisimple.evaluate(q, ni)
            found = False
            for x in ss:
                if x % elem == 0:
                    if x==elem:
                        divisible.add(x)
                    found = True
            self.assertTrue(found,
                    msg="element with base {}, partition {} = {} " \
                        "doesn't divide any of {}".format(str(q), str(ni), str(elem), str(ss)))
        self.assertSetEqual(divisible, set(ss))

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

    def all_semisimple(self, n, q, min_length=1):
        # very slow! For every partition of size n it calculates 2^n sign tuples.
        ss = list(SemisimpleElements(q, n, min_length=min_length))

        divisible = set()
        for ni in Partitions(n, min_length=min_length):
            for ei in Signs(len(ni)):
                elem = semisimple.evaluate(q, ni, ei)
                # every element must divide at least one of items in ss
                # also every item in ss must be equal to at least one element
                found = False
                for x in ss:
                    if x % elem == 0:
                        if x==elem:
                            divisible.add(x)
                        found = True
                #self.assertTrue(any(x % elem == 0 for x in ss),
                self.assertTrue(found,
                    msg="element with base {}, partition {} and signs {} = {} " \
                        "doesn't divide any of {}".format(str(q), str(ni), str(ei), str(elem), str(ss)))

        self.assertSetEqual(divisible, set(ss))

    def test_all_semisimple(self):
        self.all_semisimple(11, 5)

    def test_min_length(self):
        self.all_semisimple(11, 5, min_length=2)