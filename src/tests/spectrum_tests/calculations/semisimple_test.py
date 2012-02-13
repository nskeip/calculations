from itertools import combinations
import unittest
from spectrum.calculations import semisimple
from spectrum.calculations.partition import Partitions
from spectrum.calculations.semisimple import SemisimpleElements, MixedElements
from spectrum_tests.parametric import parameters, parametrized

__author__ = 'Daniel Lytkin'


class Signs:
    """
    Generates all n-tuples with elements {-1, 1}
    """

    def __init__(self, n):
        self._number = n

    @staticmethod
    def _next(signs):
        current = list(signs)
        i = 0
        while current[i] == 1:
            current[i] = -1
            i += 1
        current[i] = 1
        return current

    def __iter__(self):
        current = [-1] * self._number
        yield current
        try:
            while True:
                current = Signs._next(current)
                yield current
        except IndexError:
            pass


@parametrized
class SemisimpleTest(unittest.TestCase):
    def test_evaluate(self):
        ni = [8, 4, 4, 3, 2, 1]
        ei = [1, 1, -1, 1, -1, -1]
        q = 3
        r = semisimple.evaluate(q, ni, ei)
        self.assertEqual(75331760, r)

    def test_evaluate_minuses(self):
        ni = [8, 7, 4, 3, 1]
        q = 4
        r = semisimple.evaluate(q, ni)
        rp = semisimple.evaluate(q, ni, [-1] * len(ni))
        self.assertEqual(rp, r)

    @parameters(combinations(range(2, 20), 2))
    def test_minus(self, params):
        """
        Test elements [q^{n_1}-1, ..., q^{n_k}-1] for all n_1+...+n_k=n
        """
        n, q = params
        ss = SemisimpleElements(q, n, minus=True)

        divisible = set()
        for ni in Partitions(n):
            elem = semisimple.evaluate(q, ni)
            found = False
            for x in ss:
                if x % elem == 0:
                    if x == elem:
                        divisible.add(x)
                    found = True
            self.assertTrue(found,
                msg="element with base {}, partition {} = {} "\
                    "doesn't divide any of {}".format(str(q), str(ni),
                    str(elem), str(ss)))
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

    def all_semisimple(self, n, q, min_length=1, sign=0):
        # very slow! For every partition of size n it calculates 2^n sign tuples.
        ss = list(SemisimpleElements(q, n, min_length=min_length, sign=sign))
        signsMod = 0 if sign == 1 else 1

        divisible = set()
        for ni in Partitions(n, min_length=min_length):
            for ei in Signs(len(ni)):
                # skip needless signs
                if sign and ei.count(1) % 2 != signsMod: continue
                elem = semisimple.evaluate(q, ni, ei)
                # every element must divide at least one of items in ss
                # also every item in ss must be equal to at least one element
                found = False
                for x in ss:
                    if x % elem == 0:
                        if x == elem:
                            divisible.add(x)
                        found = True
                        #self.assertTrue(any(x % elem == 0 for x in ss),
                self.assertTrue(found,
                    msg="element with base {}, partition {} and signs {} = {} "\
                        "doesn't divide any of {}".format(str(q), str(ni),
                        str(ei), str(elem), str(ss)))

        self.assertSetEqual(divisible, set(ss))

    @parameters(combinations(range(2, 15), 2))
    def test_all_semisimple(self, params):
        self.all_semisimple(*params)

    @parameters(
        [(n, q, l) for n, q, l in combinations(range(2, 15), 3) if n > l])
    def test_min_length(self, params):
        self.all_semisimple(11, 5, min_length=2)

    def test_mixed(self):
        n = 3
        q = 9
        p = 3
        f = lambda k: (p ** (k - 1) + 1) // 2
        g = lambda k: p ** k

        mixed = list(MixedElements(q, n, f, g))
        expected = [246, 240, 30, 24, 120, 120, 90, 72]
        self.assertSetEqual(set(mixed), set(expected))

    @parameters(combinations(range(2, 15), 2))
    def test_semisimple_with_signs(self, params):
        n, q = params
        self.all_semisimple(n, q, sign=1)
        self.all_semisimple(n, q, sign=-1)
