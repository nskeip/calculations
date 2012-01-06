__author__ = 'Daniel Lytkin'


class Partitions:
    r"""
    Class providing iterator on partitions and size method
    """
    def __init__(self, number, **kwargs):
        self.number = number
        self.length = kwargs.get("length") or 0
        self.min_length = kwargs.get("min_length") or 1
        self.max_length = kwargs.get("max_length") or 0
        self.min_part = kwargs.get("min_part") or 1
        self.max_part = kwargs.get("max_part") or 0



    def __iter__(self):
        self.current = Partition(self.number)
        return self

    def next(self):
        nextPartition = self.current.next()
        self.current = nextPartition
        return self.current

    def size(self):
        r"""
        Returns number of partitions
        """
        # TODO
        pass

    def list(self):
        r"""
        Returns list of all partitions
        """
        return [x for x in self]


class Partition(list):
    r"""
    This class provides methods to generate partitions of natural numbers.
    """
    def __init__(self, arg):
        r"""
        When called with integer argument n, creates zero partition, which is []. By calling next() you'll get [5].
        If the argument is list, it is treated as partition
        """
        if isinstance(arg, long) or isinstance(arg, int):
            self.number = arg
            self._h = 1  # number of elements distinct from 1
            super(Partition, self).__init__()
        elif isinstance(arg, Partition):
            super(Partition, self).__init__(arg)
            self._h = arg._h
        else:
            # self.number = sum(arg) # possibly redundant
            super(Partition, self).__init__(arg)
            self._h = len(filter(lambda x: x>1, self))

    def transpose(self):
        r"""
        Transposes the partition, e. g. its Ferrers diagram.
        partition must be in descending order
        """
        transposed = []
        i = 0
        while True:
            counter = len(filter(lambda x: x-i>0, self))
            if counter:
                transposed.append(counter)
                i += 1
            else:
                break
        return Partition(transposed)


    def next(self):
        r"""
        Based on ZS1 algorithm from http://www.site.uottawa.ca/~ivan/F49-int-part.pdf
        """
        if not len(self):
            return Partition([self.number])


        if self[0] == 1:
            raise StopIteration

        x = Partition(self)
        h = x._h
        if x[h-1] == 2:
            x[h-1]=1
            x.append(1)
            h -= 1
        else:
            r = x[h-1]-1   # the last element which is greater then 1 minus 1
            t = len(x)-h+1   # number of ones + 1
            x[h-1] = r
            while t >= r:
                h += 1
                x[h-1] = r
                t -= r
            if not t:
                del x[h:]  # remove redundant ones
            else:
                if h+1 <= len(x):
                    del x[h+1:]
                else:
                    x[len(x):h+1] = [1]*(h+1-len(x))
                if t > 1:
                    h += 1
                    x[h-1] = t
        x._h = h
        return x

