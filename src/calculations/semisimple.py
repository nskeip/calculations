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
    # TODO: doc
    def __init__(self, q, n, minus=False):
        self._q = q
        self._n = n
        self._onlyMinus = minus

    def __iter__(self):
        q = self._q
        n = self._n
        if self._onlyMinus:
            for ni in BoundedSets(n, maximal=True):
                yield evaluate(q, ni)
        else:
            for left in range((n+2)//2):
                right = n - left
                leftPartitions = BoundedSets(left, maximal=True)
                leftLcms = ((evaluate(q, ni), evaluate(q, ni, ei=1)) for ni in leftPartitions) if left else [(1,1)]
                for m in leftLcms:
                    rigthPartitions = BoundedSets(right, maximal=True)
                    rightLcms = ((evaluate(q, ni, ei=1), evaluate(q, ni)) for ni in rigthPartitions) if right else [(1,1)]
                    for p in rightLcms:
                        yield lcm(m[0], p[0])
                        yield lcm(m[1], p[1])


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