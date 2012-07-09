"""
Copyright 2012 Daniel Lytkin.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""
from spectrum.calculations import numeric
from spectrum.calculations.groups import ClassicalGroup
from spectrum.tools.tools import StringViewFormatter

__author__ = 'Daniel Lytkin'

def _max_elements(set, num_elements=1):
    set = list(set)
    set.sort(reverse=True)
    return set[:num_elements]


def maximal_orders(group):
    if group.field.order == 2 and group._name in ("Sp", "PSp"):
        return symplectic_2(group._dim // 2)

    return _max_elements(group.apex(), num_elements=2)


def _is_power_of_two_by_three(n):
    """Returns whether n is a power of 2 multiplied by 3
    """
    return n % 3 == 0 and numeric.is_power_of_two(n // 3)


def symplectic_2(n):
    """Returns tuple with two maximal orders for Sp(2n, 2)
    """
    if n == 3:
        return 15, 12
    if n == 4:
        return 30, 24
    if n == 5:
        return 60, 51
    if n == 6:
        return 120, 105
    if n >= 7 and numeric.is_power_of_two(n + 1):
        return 2 ** (n + 1) - 1, 2 * (2 ** ((n + 1) // 2) - 1) * (
            2 ** ((n - 1) // 2) - 1)
    if n >= 8 and numeric.is_power_of_two(n):
        return 2 ** (n + 1) - 2, (2 ** (n // 2) - 1) * (2 ** (n // 2 + 1) - 1)
    if n >= 9 and numeric.is_power_of_two(n - 1):
        return 2 ** (n + 1) - 4, 2 * (2 ** ((n + 1) // 2) - 1) * (
            2 ** ((n - 1) // 2) - 1)
    if n >= 10 and numeric.is_power_of_two(n - 2):
        return 2 ** (n + 1) - 8, (2 ** (n // 2 - 1) - 1) * (
            2 ** (n // 2 + 2) - 1)
    if n >= 11 and _is_power_of_two_by_three(n + 1):
        return (2 ** ((2 * n + 2) // 3) + 1) * (2 ** ((n + 1) // 3) - 1), 2 * (
            2 ** ((n + 1) // 3) - 1) * (2 ** ((2 * n - 1) // 3) - 1)
    if n >= 12 and _is_power_of_two_by_three(n):
        return (2 ** (2 * n // 3) - 1) * (2 ** (n // 3 + 1) - 1), 2 * (
            2 ** (n // 3) - 1) * (2 ** (2 * n // 3) + 1)
    if n >= 13 and _is_power_of_two_by_three(n - 1):
        return 2 * (2 ** ((2 * n - 2) // 3) - 1) * (
            2 ** ((n + 2) // 3) - 1), 4 * (2 ** ((n - 1) // 3) - 1) * (
            2 ** ((2 * n - 2) // 3) + 1)
    if n >= 14 and _is_power_of_two_by_three(n - 2):
        return (2 ** ((2 * n - 4) // 3) - 1) * (2 ** ((n + 7) // 3) - 1), 4 * (
            2 ** ((2 * n - 4) // 3) - 1) * (2 ** ((n + 1) // 3) - 1)
    if n % 2 == 1:
        two_p = 2 ** (((n - 1) // 3).bit_length())
        return 2 * (2 ** two_p - 1) * (2 ** (n - two_p) - 1), 8 * (
            2 ** two_p - 1) * (2 ** (n - two_p - 2) - 1)
    if n % 2 == 0:
        two_p = 2 ** ((n // 3).bit_length())
        return (2 ** two_p - 1) * (2 ** (n + 1 - two_p) - 1), 4 * (
            2 ** two_p - 1) * (2 ** (n - 1 - two_p) - 1)


def symplectic_2_gcd(n):
    """Returns GCD(m_1(G), m_2(G)) for G=Sp(2n, 2)
    """
    if n == 3:
        return 3
    if n == 4:
        return 6
    if n == 5:
        return 3
    if n == 6:
        return 15
    if n >= 7 and numeric.is_power_of_two(n + 1):
        return 2 ** ((n + 1) // 2) - 1
    if n >= 8 and numeric.is_power_of_two(n):
        return 2 ** (n // 2) - 1
    if n >= 9 and numeric.is_power_of_two(n - 1):
        return 2 * (2 ** ((n - 1) // 2) - 1)
    if n >= 10 and numeric.is_power_of_two(n - 2):
        return 2 ** (n // 2 - 1) - 1
    if n >= 11 and _is_power_of_two_by_three(n + 1):
        return 2 ** ((n + 1) // 3) - 1
    if n >= 12 and _is_power_of_two_by_three(n):
        return 2 ** (n // 3) - 1
    if n >= 13 and _is_power_of_two_by_three(n - 1):
        return 2 * (2 ** ((n - 1) // 3) - 1)
    if n >= 14 and _is_power_of_two_by_three(n - 2):
        return 2 ** ((2 * n - 4) // 3) - 1
    if n % 2 == 1:
        two_p = 2 ** (((n - 1) // 3).bit_length())
        return 2 * (2 ** two_p - 1)
    if n % 2 == 0:
        two_p = 2 ** ((n // 3).bit_length())
        return 2 ** two_p - 1


#def max_elements(set, num_elements=1):
#    set = list(set)
#    set.sort(reverse=True)
#    return set[:num_elements]
#
#
#def max_orders(group, num_elements=1):
#    return max_elements(group.apex(), num_elements=num_elements)
#
#
def max_orders_wrapped(group,
                       mode=StringViewFormatter.VERBOSE):
    format = lambda elem: StringViewFormatter(elem, mode=mode)
    return map(format, maximal_orders(group))

#
#
#def is_max_order_semisimple(group):
#    """Returns whether maximal order of given group is semisimple.
#    """
#    max_order = max(group.apex())
#    return isinstance(max_order, SpectraElement) and max_order.quotient == 1
#
#
def print_max_elems():
    for dimension in xrange(4, 36):
        group = ClassicalGroup("Omega+", 2 * dimension, 4)
        dim_expansion = " + ".join(
            [str(x) for x in numeric.binary_expansion(dimension)])
        print "{}:".format(group).ljust(12),
        print "n = {} = {}".format(dimension, dim_expansion).ljust(30)
        print
        for elem in max_orders_wrapped(group, StringViewFormatter.VERBOSE):
            print str(elem).ljust(len(str(elem)) + 5).rjust(60), sorted(
                elem.object.partition, reverse=True)
        print

print_max_elems()
#
#
#def print_max_mixed_elements():
#    for n in map(lambda x: 2 * x, range(2, 34)):
#        print ("n = " + str(n)).ljust(10),
#        elements = max_elements(MixedElements(2, n, lambda k: 2 ** k + 1,
#            lambda k: 2 ** (k + 2)))
#        max_elem = elements[0]
#        print max_elem.str_verbose()
#
#
#def max_semisimple_2(dimension):
#    """Returns two maximal semisimple elements with q=2 and given n
#    """
#    return max_elements(SemisimpleElements(2, dimension), 2)
#
#
#def print_groups_with_semisimple_max_element():
#    for dimension in xrange(2, 40):
#        group = ClassicalGroup("Sp", 2 * dimension, 2)
#        if is_max_order_semisimple(group):
#            partition = " + ".join(numeric.binary_expansion(dimension))
#            print "{}: n = {} = {}".format(group, dimension, partition)
#            #print "\t" + StringViewFormatter(max_order).str_mixed()


