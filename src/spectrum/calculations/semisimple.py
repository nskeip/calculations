from numeric import lcm
from spectrum.calculations.set import MaximalBoundedSets, FullBoundedSets

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
        return reduce(lcm, (q ** n + ei for n in ni))
    except TypeError:
    # for sequence ei
        return reduce(lcm, (q ** n + e for (n, e) in zip(ni, ei)))


class SemisimpleElements:
    """Generates elements of form LCM(q^{n_1} \pm 1, ..., q^{n_k} \pm 1) for
    all partitions n_1 + ... + n_k = n.
    If 'parity' is set to 1 or -1, generates elements with even or odd number
    of pluses respectively.
    If 'sign' is set to 1 or -1, generates elements of form
    LCM(q^{n_1}-sign^{n_1}, ..., q^{n_k}-sign^{n_k})
    'sign' or 'parity' arguments must be only used separately.
    """

    def __init__(self, q, n, min_length=1, parity=0, sign=0):
        self._q = q
        self._n = n
        self._min_length = min_length
        self._parity = parity
        self._sign = sign

    def _with_sign_generator(self):
        """Generates semisimple element with specified epsilon
        (for Linear and Unitary groups)
        """
        q = self._q
        n = self._n
        # [q^n_1 - 1, ..., q^n_k - 1] if sign = 1, else
        # [q^n_1 - sign^n_1, ..., q^n_k - sign^n_k]
        f = ((lambda ni: -1) if self._sign == 1 else
             lambda ni: (-1 if nk % 2 == 0 else 1 for nk in ni))
        for ni in MaximalBoundedSets(n):
            if len(ni) + n - sum(ni) < self._min_length:
                continue
            yield evaluate(q, ni, ei=f(ni))

    def _with_parity_generator(self):
        """Generates semisimple elements with even or odd number of pluses"""
        q = self._q
        n = self._n
        plusesMod = 0 if self._parity == 1 else 1
        for pluses in xrange(plusesMod, n + 1):
            for plusPartition in FullBoundedSets(pluses):
                minuses = n - pluses
                if not len(plusPartition) % 2 == plusesMod:
                    if pluses == n:
                        continue
                    plusPartition = plusPartition + [1]
                    minuses -= 1
                plusLcm = evaluate(q, plusPartition, 1) if pluses else 1
                for minusPartition in MaximalBoundedSets(minuses):
                    rest = n - pluses - sum(minusPartition)
                    if len(plusPartition) + len(
                        minusPartition) + rest < self._min_length:
                        continue
                    minusLcm = evaluate(q, minusPartition) if minuses else 1
                    yield lcm(plusLcm, minusLcm)

    def _general_generator(self):
        """Generates all semisimple elements"""
        q = self._q
        n = self._n
        for left in xrange((n + 2) // 2):
            right = n - left
            leftPartitions = MaximalBoundedSets(left)
            for lPart in leftPartitions:
                lLcms = (evaluate(q, lPart),
                         evaluate(q, lPart, ei=1)) if left else (1, 1)
                rightPartitions = MaximalBoundedSets(right)
                for rPart in rightPartitions:
                    if len(lPart) + len(rPart) < self._min_length:
                        continue
                    rLcms = (evaluate(q, rPart, ei=1),
                             evaluate(q, rPart)) if right else (1, 1)
                    yield lcm(lLcms[0], rLcms[0])
                    yield lcm(lLcms[1], rLcms[1])

    def __iter__(self):
        if self._sign:
            return self._with_sign_generator()
        if self._parity:
            return self._with_parity_generator()
        return self._general_generator()


class MixedElements:
    """Generates elements of form g(k) * LCM(q^{n_1} \pm 1, ..., q^{n_s} \pm 1)
    for all k and partitions f(k) + n_1 + ... + n_s = n, where k, s > 0.
    """

    def __init__(self, q, n, f, g, min_length=1, parity=0, sign=0):
        self._q = q
        self._n = n
        self._f = f
        self._g = g
        self._min_length = min_length
        self._parity = parity
        self._sign = sign


    def __iter__(self):
        k = 1
        while True:
            toPart = self._n - self._f(k)
            if toPart <= 0: break
            for elem in SemisimpleElements(self._q, toPart,
                min_length=self._min_length, parity=self._parity,
                sign=self._sign):
                yield elem * self._g(k)
            k += 1

