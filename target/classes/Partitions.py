__author__ = 'Daniel Lytkin'


class Partitions:
    """ This class provides methods to generate partitions of natural numbers.
    """
    @staticmethod
    def transpose(partition):
        """ Transposes the partition, e. g. its Ferrers diagram.
        partition should be ordered high-to-low
        """
        transposed = []
        i = 0
        while True:
            counter = len(filter(lambda x: x-i>0, partition))
            if counter:
                transposed.append(counter)
                i += 1
            else:
                break
        return transposed


  