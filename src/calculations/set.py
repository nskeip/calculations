__author__ = 'Daniel Lytkin'



class BoundedSets:
    """Generates integer sets {n_1,...,n_k}, such that n_1+...+n_k <= n.
    If optional parameter 'maximal' is set to True, then generates only those sets that
    are maximal under containment relation.
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
                t = min(x[-1]-1, bound - sum)
                if not t: break
                sum += t
                x.append(t)
        return x, sum

    @staticmethod
    def next(sequence, bound):
        """Returns next bounded set after sequence in reversed lexicographical order
        """
        return BoundedSets._next(sequence, bound, sum(sequence))[0]

    @staticmethod
    def _nextMaximal(sequence, bound, sum):
        if sequence[0] <= 1:
            return None, None

        x = list(sequence)
        try:
            i = 1
            while x[-1] == i: # if tail is [N, i, i-1, i-2, ..., 1], remove it ant set to [N-1]
                i+=1
                sum -= x[-1]
                del x[-1]
        except IndexError:
        # this means that sequence is [i, i-1, i-2, ..., 1] thus it is the last possible maximal set
            return None, None

        x[-1] -= 1
        sum -= 1
        while True:
            t = min(x[-1]-1, bound - sum)
            if not t: break
            sum += t
            x.append(t)
        return x, sum

    @staticmethod
    def nextMaximal(sequence, bound):
        """Returns next maximal bounded set after sequence in reversed lexicographical order.
        Input sequence itself must be maximal, otherwise output will be incorrect.
        """
        return BoundedSets._nextMaximal(sequence, bound, sum(sequence))[0]

    def __init__(self, bound, maximal=False):
        self._bound = bound
        self._maximal = maximal

    def __iter__(self):
        current = [self._bound]
        sum = self._bound
        nextSet = BoundedSets._nextMaximal if self._maximal else BoundedSets._next
        while current is not None:
            yield current
            current, sum = nextSet(current, self._bound, sum)


