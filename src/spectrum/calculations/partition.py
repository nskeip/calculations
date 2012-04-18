__author__ = 'Daniel Lytkin'

class Partitions(object):
    """Class providing iterator on partitions
    Required parameter:
        number - the number to partition
    Optional parameters:
        length - if specified, generates only partitions of fixed length
        min_length, max_length - minimal and maximal length of partitions
        min_part, max_part - minimum and maximum for partition elements
        min_slope, max_slope - minimum and maximum for numbers a[i]-a[i+1] for
        i=0..n-1 and a[i] for i=n
    """

    @staticmethod
    def transpose(partition):
        """Transposes the partition, e. g. its Ferrers diagram.
        partition must be in descending order
        """
        transposed = []
        i = 0
        while True:
            counter = len(filter(lambda x: x - i > 0, partition))
            if counter:
                transposed.append(counter)
                i += 1
            else:
                break
        return transposed

    @staticmethod
    def _slope(seq):
        return map(lambda x, y: x - y, seq, seq[1:] + [0])

    def _isValid(self, seq):
        return all(func(seq) for func in self._validators)

    def __init__(self, number, length=None, min_length=None, max_length=None,
                 min_part=None, max_part=None, min_slope=None, max_slope=None):
        self._number, self._length = number, length
        validators = [(min_length, lambda seq: len(seq) >= min_length),
            (max_length, lambda seq: len(seq) <= max_length),
            (min_part, lambda seq: all(x >= min_part for x in seq)),
            (max_part, lambda seq: all(x <= max_part for x in seq)),
            (min_slope,
             lambda seq: all(x >= min_slope for x in Partitions._slope(seq))),
            (max_slope,
             lambda seq: all(x <= max_slope for x in Partitions._slope(seq)))]
        self._validators = [func for (c, func) in validators if c is not None]


    _h = 0

    @staticmethod
    def _next(partition):
        r"""
        Based on ZS1 algorithm from http://www.site.uottawa.ca/~ivan/F49-int-part.pdf
        """
        if partition[0] <= 1:
            return None

        # not a really good idea;
        # needed to simplify iterator definition
        h = Partitions._h
        x = list(partition)  # make a copy of this partition
        if x[h - 1] == 2:
            x[h - 1] = 1
            x.append(1)
            h -= 1
        else:
            r = x[
                h - 1] - 1   # the last element which is greater then 1 minus 1
            t = len(x) - h + 1   # number of ones + 1
            x[h - 1] = r
            while t >= r:
                h += 1
                x[h - 1] = r
                t -= r
            if not t:
                del x[h:]  # remove redundant ones
            else:
                m = h + 1 - len(x)
                if m <= 0:
                    del x[h + 1:]
                else:
                    x[len(x):] = [1] * m
                if t > 1:
                    h += 1
                    x[h - 1] = t
        Partitions._h = h
        return x

    @staticmethod
    def _nextFixedLength(partition):
        smallest = partition[-1]
        i = 1
        try:
            while partition[-i - 1] - smallest < 2:
                i += 1
        except IndexError:
            return None

        x = list(partition)
        x[-i - 1] -= 1
        s = sum(x[-i:]) + 1
        while i > 0:
            x[-i] = min(x[-i - 1], s - i + 1)
            s -= x[-i]
            i -= 1

        return x

    def __iter__(self):
        l = self._length
        n = self._number
        if self._length is None:
            # we use class variable to generalize next() function
            Partitions._h = 1
            nextPartition = Partitions._next
            current = [n]
        else:
            nextPartition = Partitions._nextFixedLength
            current = [n - l + 1] + [1] * (l - 1) if l <= n else None

        if not self._validators:
            while current is not None:
                yield current
                current = nextPartition(current)
        else:
            while current is not None:
                if self._isValid(current): yield current
                current = nextPartition(current)
