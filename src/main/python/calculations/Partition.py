__author__ = 'Daniel Lytkin'


class PartitionConstraints:
    __defaultConstraints = {"length" : 0,
                            "min_length" : 1, "max_length" : 0,
                            "min_part" : 1, "max_part" : 0,
                            "min_slope" : 0, "max_slope" : 0}

    def __init__(self, **kwargs):
        d = PartitionConstraints.__defaultConstraints
        self.constraints = dict([(key, kwargs.get(key) or d[key]) for key in d.iterkeys()])

    def isEmpty(self):
        d = PartitionConstraints.__defaultConstraints
        return all(self.constraints.get(key) == d.get(key) for key in d.iterkeys())

    def isValid(self, partition):
        length = self.constraints.get("length")
        if length and len(partition) != length: return False

        if len(partition) < self.constraints.get("min_length"): return False

        max_length  = self.constraints.get("max_length")
        if max_length and len(partition) > max_length: return False

        min_part = self.constraints.get("min_part")
        if min_part > 1 and any(x < min_part for x in partition): return False

        max_part = self.constraints.get("max_part")
        if max_part and any(x > max_part for x in partition): return False

        slopes = map(lambda x,y: x-y, partition, partition[1:] + [0])

        min_slope = self.constraints.get("min_slope")
        if min_slope and any(x < min_slope for x in slopes): return False

        max_slope = self.constraints.get("max_slope")
        if max_slope and any(x > max_slope for x in slopes): return False

        return True


class Partitions:
    r"""
    Class providing iterator on partitions and size method
    """
    def __init__(self, number, **kwargs):
        self.number = number
        self.constraints = PartitionConstraints(**kwargs)



    def __iter__(self):
        number = self.number
        if self.constraints.isEmpty():
            class PartitionsIterator:
                def __init__(self):
                    self.current = Partition(number)

                def next(self):
                    self.current = self.current.next()
                    return self.current
            return PartitionsIterator()
        else:
            constraints = self.constraints
            class PartitionsConstrainedIterator:
                def __init__(self):
                    self.current = Partition(number)

                def next(self):
                    while True:
                        self.current = self.current.next()
                        if constraints.isValid(self.current): break
                    return self.current
            return PartitionsConstrainedIterator()


    def size(self):
        r"""
        Returns number of partitions
        """
        # TODO
        pass



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

        x = Partition(self)  # make a copy of this partition
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

