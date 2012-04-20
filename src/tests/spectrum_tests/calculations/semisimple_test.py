import unittest
import itertools
from spectrum.calculations import numeric
from spectrum.calculations.partition import Partitions
from spectrum.calculations.semisimple import SemisimpleElements, MixedElements, SpectraElement
from spectrum_tests.parametric import parameters, parametrized

__author__ = 'Daniel Lytkin'

def evaluate(q, ni, ei=-1):
    """Calculates sesmisimple element with base q, partition ni and signs ei,
    which is precisely
    lcm(q^ni[1] + ei[1], ..., q^ni[k] + ei[k]) where k is the length of
    partition.
    ei may be a single integer - in this it is considered as same sign for each
    element.
    """
    try:
    # for integer ei
        return reduce(numeric.lcm, (q ** n + ei for n in ni))
    except TypeError:
    # for sequence ei
        return reduce(numeric.lcm, (q ** n + e for (n, e) in zip(ni, ei)))


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


class SpectraElementTest(unittest.TestCase):
    def test_str(self):
        elem = SpectraElement(3, 2, [2, 3, 4], [1, -1, 1])
        expected = "3 * [2^4 + 1, 2^3 - 1, 2^2 + 1]"
        self.assertEqual(expected, elem.str_verbose())

        elem = SpectraElement(3)
        self.assertEqual("3", elem.str_verbose())

        elem = SpectraElement(q=2, partition=[2, 3, 4], signs=[1, -1, 1])
        expected = "[2^4 + 1, 2^3 - 1, 2^2 + 1]"
        self.assertEqual(expected, elem.str_verbose())

        elem = SpectraElement(q=2, partition=[1, 1, 4], signs=[1, -1, 1])
        expected = "[2^4 + 1, 2 + 1, 2 - 1]"
        self.assertEqual(expected, elem.str_verbose())

        elem = SpectraElement(q=2, partition=[1], signs=[1])
        expected = "2 + 1"
        self.assertEqual(expected, elem.str_verbose())

        elem = SpectraElement(quotient=2, q=2, partition=[1], signs=[1])
        expected = "2 * (2 + 1)"
        self.assertEqual(expected, elem.str_verbose())


    def test_lcm(self):
        elem1 = SpectraElement(q=2, partition=[2, 3], signs=[1, -1])
        elem2 = SpectraElement(q=2, partition=[3, 4], signs=[1, -1])
        expected = "[2^4 - 1, 2^3 + 1, 2^3 - 1, 2^2 + 1]"
        self.assertEqual(expected, elem1.lcm(elem2).str_verbose())

    def test_mult(self):
        elem = SpectraElement(q=2, partition=[2, 3], signs=[1, -1])
        expected = "2 * [2^3 - 1, 2^2 + 1]"
        self.assertEqual(expected, (elem * 2).str_verbose())


@parametrized
class SemisimpleTest(unittest.TestCase):
    def test_evaluate(self):
        ni = [8, 4, 4, 3, 2, 1]
        ei = [1, 1, -1, 1, -1, -1]
        q = 3
        r = evaluate(q, ni, ei)
        self.assertEqual(75331760, r)

    def test_evaluate_minuses(self):
        ni = [8, 7, 4, 3, 1]
        q = 4
        r = evaluate(q, ni)
        rp = evaluate(q, ni, [-1] * len(ni))
        self.assertEqual(rp, r)

    @parameters(itertools.combinations(range(2, 15), 2))
    def test_minus(self, params):
        """
        Test elements [q^{n_1}-1, ..., q^{n_k}-1] for all n_1+...+n_k=n
        """
        n, q = params
        ss = SemisimpleElements(q, n, sign=1, verbose=False)

        divisible = set()
        for ni in Partitions(n):
            elem = evaluate(q, ni)
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

    def all_semisimple(self, n, q, min_length=1, parity=0, sign=0):
        # very slow! For every partition of size n it calculates 2^n parity tuples.
        ss = list(
            SemisimpleElements(q, n, min_length=min_length, parity=parity,
                sign=sign, verbose=False))
        signsMod = 0 if parity == 1 else 1

        divisible = set()
        for ni in Partitions(n, min_length=min_length):
            if sign:
                signs = [[-sign ** nk for nk in ni]]
            else:
                signs = Signs(len(ni))
            for ei in signs:
                # skip needless signs
                if parity and ei.count(1) % 2 != signsMod: continue
                elem = evaluate(q, ni, ei)
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

    @parameters(itertools.combinations(range(2, 15), 2))
    def test_all_semisimple(self, params):
        self.all_semisimple(*params)

    @parameters(filter(lambda (n, q, l): n > l,
        itertools.combinations(range(2, 15), 3)))
    #[(n, q, l) for n, q, l in combinations(range(2, 15), 3) if n > l])
    def test_min_length(self, params):
        n, q, l = params
        self.all_semisimple(n, q, min_length=l)

    def test_mixed(self):
        n = 3
        q = 9
        p = 3
        f = lambda k: (p ** (k - 1) + 1) // 2
        g = lambda k: p ** k

        mixed = list(MixedElements(q, n, f, g))
        expected = [246, 240, 30, 24, 120, 120, 90, 72]
        self.assertSetEqual(set(mixed), set(expected))

    @parameters(itertools.product(range(2, 10), range(2, 15), (-1, 1)))
    def test_semisimple_parity(self, params):
        n, q, p = params
        self.all_semisimple(n, q, parity=p)
        self.all_semisimple(n, q, parity=p, min_length=10)

    @parameters(itertools.product(range(2, 15), range(2, 15), (-1, 1)))
    def test_semisimple_sign(self, params):
        n, q, p = params
        self.all_semisimple(n, q, sign=p)
        self.all_semisimple(n, q, sign=p, min_length=10)