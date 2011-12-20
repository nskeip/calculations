__author__ = 'Daniel Lytkin'




class Partition(list):
    r"""
    This class provides methods to generate partitions of natural numbers.
    """
    def __init__(self, arg):
        r"""
        When called with integer argument n, creates first partition, which is [n]
        If the argument is list, it is treated as partition
        """
        if isinstance(arg, int):
            super(Partition, self).__init__([arg])
        else:
            super(Partition, self).__init__(arg)

    def transpose(self):
        r"""
        Transposes the partition, e. g. its Ferrers diagram.
        partition should be in descending order
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
        x = list(self)
        if x[0] == 1:
            raise StopIteration

        h = len(filter(lambda x: x>1, x))
        if x[h-1] == 2:
            x[h-1]=1
            x.append(1)
        else:
            r = x[h-1]-1   # the last element which is greater then 1 minus 1
            t = len(x)-h+1   # number of ones + 1
            x[h-1] = r
            while t >= r:
                h += 1
                x[h-1] = r
                t = t - r
            if not t:
                if h<=len(x):
                    del x[h:]
                else:
                   x[len(x):h] = [1 for i in range(len(x), h)]
            else:
                if h+1<=len(x):
                    del x[h+1:]
                else:
                    x[len(x):h+1] = [1 for i in range(len(x), h+1)]
                if t > 1:
                    h += 1
                    x[h-1] = t
        return Partition(x)

