__author__ = 'Daniel Lytkin'

"""
Module providing methods to calculate GCD and LCM etc.
"""

def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

def lcm(a, b):
    return a/gcd(a, b) * b

def filterDivisors(iterable):
    """
    Removes all elements, which divide any other.
    Input argument must be in decreasing order
    """
    ret = []
    for element in iterable:
        if not any(x % element == 0 for x in ret):
            ret.append(element)

    return ret