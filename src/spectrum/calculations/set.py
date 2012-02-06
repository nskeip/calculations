__author__ = 'Daniel Lytkin'


class BoundedSets(object):
    """Generates integer sets {n_1,...,n_k}, such that n_1+...+n_k <= n.
    """

    @staticmethod
    def _next(sequence, bound, sum):
        if sequence[0] <= 1:
            return None, None

        x = list(sequence)
        sum -= 1
        if x[-1] == 1: # if the last element is 1, remove it
            del x[-1]
        else:
            x[-1] -= 1
            while True:
                t = min(x[-1] - 1, bound - sum)
                if not t: break
                sum += t
                x.append(t)
        return x, sum

    @classmethod
    def next(cls, sequence, bound):
        """Returns next bounded set after sequence in reversed lexicographical order
        """
        return cls._next(sequence, bound, sum(sequence))[0]


    def __init__(self, bound):
        self._bound = bound
        self._next = BoundedSets._next

    def __iter__(self):
        if self._bound:
            current = [self._bound]
            sum = self._bound
            while current is not None:
                yield current
                current, sum = type(self)._next(current, self._bound, sum)
        else:
            yield []


class MaximalBoundedSets(BoundedSets):
    """Generates integer sets {n_1,...,n_k}, such that n_1+...+n_k <= n,  maximal under containment relation.
    """

    @staticmethod
    def _next(sequence, bound, sum):
        if sequence[0] <= 1:
            return None, None

        x = list(sequence)
        try:
            i = 1
            while x[
                  -1] == i: # if tail is [N, i, i-1, i-2, ..., 1], remove it ant set to [N-1]
                i += 1
                sum -= x[-1]
                del x[-1]
        except IndexError:
            # if we're here then our sequence is [i, i-1, i-2, ..., 1], thus it is the last possible maximal set
            return None, None

        x[-1] -= 1
        sum -= 1
        while True:
            t = min(x[-1] - 1, bound - sum)
            if not t: break
            sum += t
            x.append(t)
        return x, sum


class FullBoundedSets(BoundedSets):
    """Generates integer sets {n_1,...,n_k}, such that n_1+...+n_k = n, which are precisely all partitions with distinct parts.
    """

    @staticmethod
    def _next(sequence, bound, sum):
        x = sequence
        while True:
            x, sum = MaximalBoundedSets._next(x, bound, sum)
            if sum == bound or x is None: break
        return x, sum
