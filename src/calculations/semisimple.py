from calculations.numeric import lcm
from calculations.set import BoundedSet

__author__ = 'Daniel Lytkin'

def evaluate(q, ni, ei = None):
    """Calculates sesmisimple element with base q, partition ni and signs ei, which is precisely
    lcm(q^ni[1] + ei[1], ..., q^ni[k] + ei[k]) where k is the length of partition.
    """
    try:
        return reduce(lcm, (q**n + e for (n, e) in zip(ni, ei)))
    except TypeError:
        return reduce(lcm, (q**n - 1 for n in ni))


class SemisimpleElements:
    # TODO: doc
    def __init__(self, q, n, onlyMinus=False):
        self._q = q
        self._n = n
        self._onlyMinus = onlyMinus

    def __iter__(self):
        if self._onlyMinus:
            return (evaluate(self._q, ni) for ni in BoundedSet(self._n, maximal=True))



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