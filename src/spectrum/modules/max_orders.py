from spectrum.calculations import numeric
from spectrum.calculations.groups import ClassicalGroup
from spectrum.calculations.semisimple import SpectraElement
from spectrum.tools.tools import StringViewFormatter

__author__ = 'Daniel Lytkin'

def max_orders(group, num_elements=1):
    apex = group.apex()
    apex.sort(reverse=True)
    return apex[:num_elements]


def max_orders_wrapped(group, num_elements=1,
                       mode=StringViewFormatter.VERBOSE):
    format = lambda elem: StringViewFormatter(elem, mode=mode)
    return map(format, max_orders(group, num_elements))


def is_max_order_semisimple(group):
    """Returns whether maximal order of given group is semisimple.
    """
    max_order = max(group.apex())
    return isinstance(max_order, SpectraElement) and max_order.quotient == 1


def print_max_elems():
    for dimension in map(lambda x: 2 * x + 1, range(1, 20)):
        group = ClassicalGroup("Sp", 2 * dimension, 2)
        dim_expansion = " + ".join(
            [str(x) for x in numeric.binary_expansion(dimension)])
        print "{}:".format(group).ljust(10),
        print "n = {} = {}".format(dimension, dim_expansion).ljust(30),
        for elem in max_orders_wrapped(group, 1, StringViewFormatter.VERBOSE):
            print "\t" + str(elem)


def print_groups_with_semisimple_max_element():
    for dimension in xrange(2, 40):
        group = ClassicalGroup("Sp", 2 * dimension, 2)
        if is_max_order_semisimple(group):
            partition = " + ".join(numeric.binary_expansion(dimension))
            print "{}: n = {} = {}".format(group, dimension, partition)
            #print "\t" + StringViewFormatter(max_order).str_mixed()

print_max_elems()
