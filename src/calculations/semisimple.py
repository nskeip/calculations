from calculations.set import MaximalBoundedSets, FullBoundedSets
from numeric import lcm

__author__ = 'Daniel Lytkin'

def evaluate(q, ni, ei = -1):
    """Calculates sesmisimple element with base q, partition ni and signs ei, which is precisely
    lcm(q^ni[1] + ei[1], ..., q^ni[k] + ei[k]) where k is the length of partition.
    ei may be a single integer - in this it is considered as same sign for each element.
    """
    try:
    # for integer ei
        return reduce(lcm, (q**n + ei for n in ni))
    except TypeError:
    # for sequence ei
        return reduce(lcm, (q**n + e for (n, e) in zip(ni, ei)))


class SemisimpleElements:
    """Generates elements of form LCM(q^{n_1} \pm 1, ..., q^{n_k} \pm 1) for all partitions n_1 + ... + n_k = n.
    If optional parameter 'minus' is set to True, generates only elements with all minuses.
    If 'sign' is set to 1 or -1, generates elements with even or odd number of pluses respectively.
    """
    def __init__(self, q, n, minus=False, min_length=1, sign=0):
        self._q = q
        self._n = n
        self._onlyMinus = minus
        self._min_length = min_length
        self._sign = sign

    def __iter__(self):
        q = self._q
        n = self._n
        if self._onlyMinus:
            for ni in MaximalBoundedSets(n):
                yield evaluate(q, ni)
        else:
            if not self._sign:
                for left in xrange((n+2)//2):
                    right = n - left
                    leftPartitions = MaximalBoundedSets(left)
                    for lPart in leftPartitions:
                        lLcms = (evaluate(q, lPart), evaluate(q, lPart, ei=1)) if left else (1, 1)
                        rightPartitions = MaximalBoundedSets(right)
                        for rPart in rightPartitions:
                            if len(lPart)+len(rPart) < self._min_length:
                                continue
                            rLcms = (evaluate(q, rPart, ei=1), evaluate(q, rPart)) if right else (1, 1)
                            yield lcm(lLcms[0], rLcms[0])
                            yield lcm(lLcms[1], rLcms[1])
            else:
                plusesMod = 0 if self._sign == 1 else 1
                for pluses in xrange(n+1):
                    for plusPartition in FullBoundedSets(pluses):
                        if len(plusPartition) % 2 != plusesMod: continue
                        plusLcm = evaluate(q, plusPartition, 1) if pluses else 1
                        for minusPartition in MaximalBoundedSets(n-pluses):
                            if len(plusPartition)+len(minusPartition) < self._min_length:
                                continue
                            minusLcm = evaluate(q, minusPartition) if (n-pluses) else 1
                            yield lcm(plusLcm, minusLcm)





class MixedElements:
    """Generates elements of form g(k) * LCM(q^{n_1} \pm 1, ..., q^{n_s} \pm 1)
    for all k and partitions f(k) + n_1 + ... + n_s = n, where k, s > 0.
    """
    def __init__(self, q, n, f, g, min_length=1, sign=0):
        self._q = q
        self._n = n
        self._f = f
        self._g = g
        self._min_length = min_length
        self._sign = sign


    def __iter__(self):
        k = 1
        while True:
            toPart = self._n - self._f(k)
            if toPart <= 0: break
            for elem in SemisimpleElements(self._q, toPart, min_length=self._min_length, sign=self._sign):
                yield elem*self._g(k)
            k += 1

