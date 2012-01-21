from numeric import lcm
from set import  BoundedSets

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
    If optional parameter 'minus' is set to True, generates only elements with all minuses

    """
    def __init__(self, q, n, minus=False, min_length=1):
        self._q = q
        self._n = n
        self._onlyMinus = minus
        self._min_length = min_length

    def __iter__(self):
        q = self._q
        n = self._n
        if self._onlyMinus:
            for ni in BoundedSets(n, maximal=True):
                yield evaluate(q, ni)
        else:
            for left in xrange((n+2)//2):
                right = n - left
                leftPartitions = BoundedSets(left, maximal=True)
                # leftLcms = ((evaluate(q, ni), evaluate(q, ni, ei=1)) for ni in leftPartitions) if left else [(1,1)]
                for lPart in leftPartitions:
                    lLcms = (evaluate(q, lPart), evaluate(q, lPart, ei=1)) if left else (1, 1)
                    rightPartitions = BoundedSets(right, maximal=True)
                    # rightLcms = ((evaluate(q, ni, ei=1), evaluate(q, ni)) for ni in rigthPartitions) if right else [(1,1)]
                    for rPart in rightPartitions:
                        if len(lPart)+len(rPart) < self._min_length:
                            continue
                        rLcms = (evaluate(q, rPart, ei=1), evaluate(q, rPart)) if right else (1, 1)
                        yield lcm(lLcms[0], rLcms[0])
                        yield lcm(lLcms[1], rLcms[1])

class MixedElements:
    """Generates elements of form p^k * LCM(q^{n_1} \pm 1, ..., q^{n_s} \pm 1)
    for all partitions f(k) + n_1 + ... + n_s = n, where k, s > 0.
    """
    def __init__(self, q, n, p, f):
        self._q = q
        self._n = n
        self._p = p
        self._f = lambda k: f(self._p, k)

    def __iter__(self):
        k = 1
        while True:
            toPart = self._n - self._f(k)
            if toPart <= 0: break
            for elem in SemisimpleElements(self._q, toPart):
                yield elem*(self._p**k)
            k += 1

class Signs:
    """
    Generates all n-tuples with elements {-1, 1}
    """
    def __init__(self, n):
        self._number = n

    def __iter__(self):
        current = [-1]*self._number
        yield current
        try:
            while True:
                current = list(current)
                i = 0
                while current[i]==1:
                    current[i]=-1
                    i += 1
                current[i]=1
                yield current

        except IndexError:
            pass