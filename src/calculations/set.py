__author__ = 'Daniel Lytkin'


#def generateSets(bound, start=None, maximal=False):
#    if start is None:
#        start = bound
#    if not bound or not start: return [[]]
#    sets = []
#    for i in range(start,0, -1):
#        sets += [[i] + s for s in generateSets(bound-i, min(bound-i,i-1), maximal)]
#    return sets + [[]]*(not maximal)



class BoundedSets:
    r"""
    Generates integer sets {n_1,...,n_k}, such that n_1+...+n_k <= n
    """
    def __init__(self, bound, maximal=False):
        self._bound = bound

    def __iter__(self):
        current = BoundedSet(self._bound)
        while current is not None:
            yield current
            current = current.next()


class BoundedSet(list):

    def __init__(self, *args, **kwargs):
        if isinstance(args[0], list):
            super(BoundedSet, self).__init__(args[0])
        else:
            super(BoundedSet, self).__init__(args)
        self._bound, self._sum = (args[0]._bound, args[0]._sum) if isinstance(args[0], BoundedSet) else (sum(self),)*2
        self.next = self._nextMax if kwargs.get("maximal") else self._next

    def _next(self): # generate next set
        if self[0] == 1:
            return None

        x = BoundedSet(self)
        if x[-1] == 1: # if the last element is 1, remove it
            del x[-1]
            x._sum -= 1
        else:
            x[-1] -= 1
            x._sum -= 1
            while True:
                t = min(x[-1]-1, x._bound - x._sum)
                if not t: break
                x._sum += t
                x.append(t)

        return x

    def _nextMax(self):
        if self[0] == 1:
            return None

        x = BoundedSet(self)
        if x[-1] == 1: # if the last element is 1, remove it
            del x[-1]
            x._sum -= 1
        else:
            x[-1] -= 1
            x._sum -= 1
            while True:
                t = min(x[-1]-1, x._bound - x._sum)
                if not t: break
                x._sum += t
                x.append(t)

        return x