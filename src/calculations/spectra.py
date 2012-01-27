from itertools import chain
from calculations.numeric import lcm, firstDivisor, Integer, getExponent, sortAndFilter
from calculations.partition import Partitions
from calculations.semisimple import SemisimpleElements, MixedElements
from calculations.tools import doc_inherit

__author__ = 'Daniel Lytkin'

class Field:
    """Finite field.
    Can be created as Field(order) or Field(base, pow) where base**pow is the order of the field.
    'order' must be a prime power, otherwise the wrong field will be created.
    """
    def __init__(self, *arg):
        if len(arg)==1:
            if arg[0] <= 1:
                raise ValueError("Field order must be at least 2")
            self._base = firstDivisor(arg[0])
            self._pow = 1
            self._order = self._base
            while self._order < arg[0]:
                self._pow += 1
                self._order *= self._base
        elif len(arg)==2:
            self._base, self._pow = arg[0], arg[1]
            if self._pow < 1 or self._base < 2:
                raise ValueError("Field order must be at least 2")
            self._order = self._base ** self._pow

    def order(self):
        """Returns field order."""
        return self._order
    def char(self):
        """Returns field characteristic."""
        return self._base
    def pow(self):
        """Returns k, such that q = p^k, where q is field order and p is field characteristic."""
        return self._pow

class Group(object):
    """Interface for finite groups with method to calculate their spectra
    """
    def apex(self):
        """Returns apex of the group, which is the set of its element orders with all divisors filtered out.
        """
        raise NotImplementedError()

    def order(self):
        """Returns group order.
        """
        raise NotImplementedError()

class SporadicGroup(Group):
    _groups = {
        "M11" : (( 5, 6, 8, 11 ), Integer((2, 4), (3,2), 5, 11)),
        "M12" : (( 6, 8, 10, 11 ), Integer((2, 6), (3, 3), 5, 11)),
        "M22" : (( 5, 6, 7, 8, 11 ), Integer((2, 7), (3, 2), 5, 7, 11)),
        "M23" : (( 6, 8, 11, 14, 15, 23 ), Integer((2, 7), (3, 2), 5, 7, 11, 23)),
        "M24" : (( 8, 10, 11, 12, 14, 15, 21, 23 ), Integer((2, 10), (3, 3), 5, 7, 11, 23)),
        "J1" : (( 6, 7, 10, 11, 15, 19 ), Integer((2, 3), 3, 5, 7, 11, 19)),
        "J2" : (( 7, 8, 10, 12, 15 ), Integer((2, 7), (3, 3), (5, 2), 7)),
        "J3" : (( 8, 9, 10, 12, 15, 17, 19 ), Integer((2, 7), (3, 5), 5, 17, 19)),
        "J4" : (( 16, 23, 24, 28, 29, 30, 31, 35, 37, 40, 42, 43, 44, 66 ),
                Integer((2, 21), (3, 3), 5, 7, (11, 3), 23, 29, 31, 37, 43)),
        "Co1" : (( 16, 22, 23, 24, 26, 28, 33, 35, 36, 39, 40, 42, 60 ),
                 Integer((2, 21), (3, 9), (5, 4), (7, 2), 11, 13, 23)),
        "Co2" : (( 11, 16, 18, 20, 23, 24, 28, 30 ), Integer((2, 18), (3, 6), (5, 3), 7, 11, 23)),
        "Co3" : (( 14, 18, 20, 21, 22, 23, 24, 30 ), Integer((2, 10), (3, 7), (5, 3), 7, 11, 23)),
        "Fi22" : (( 13, 14, 16, 18, 20, 21, 22, 24, 30 ), Integer((2, 17), (3, 9), (5, 2), 7, 11, 13)),
        "Fi23" : (( 16, 17, 22, 23, 24, 26, 27, 28, 35, 36, 39, 42, 60 ),
                  Integer((2, 18), (3, 13), (5, 2), 7, 11, 13, 17, 23)),
        "Fi24'" : (( 16, 17, 22, 23, 24, 26, 27, 28, 29, 33, 35, 36, 39, 42, 45, 60 ),
                   Integer((2, 21), (3, 16), (5, 2), (7, 3), 11, 13, 17, 23, 29)),
        "HS" : (( 7, 8, 11, 12, 15, 20 ), Integer((2, 9), (3, 2), (5, 3), 7, 11)),
        "McL" : (( 8, 9, 11, 12, 14, 30 ), Integer((2, 7), (3, 6), (5, 3), 7, 11)),
        "He" : (( 8, 10, 12, 15, 17, 21, 28 ), Integer((2, 10), (3, 3), (5, 2), (7, 3), 17)),
        "Ru" : (( 14, 15, 16, 20, 24, 26, 29 ), Integer((2, 14), (3, 3), (5, 3), 7, 13, 29)),
        "Suz" : (( 11, 13, 14, 15, 18, 20, 21, 24 ), Integer((2, 13), (3, 7), (5, 2), 7, 11, 13)),
        "O'N" : (( 11, 12, 15, 16, 19, 20, 28, 31 ), Integer((2, 9), (3, 4), 5, (7, 3), 11, 19, 31)),
        "HN" : (( 9, 12, 14, 19, 21, 22, 25, 30, 35, 40 ), Integer((2, 14), (3, 6), (5, 6), 7, 11, 19)),
        "Ly" : (( 18, 22, 24, 25, 28, 30, 31, 33, 37, 40, 42, 67 ),
                Integer((2, 8), (3, 7), (5, 6), 7, 11, 31, 37, 67)),
        "Th" : (( 19, 20, 21, 24, 27, 28, 30, 31, 36, 39 ),
                Integer((2, 15), (3, 10), (5, 3), (7, 2), 13, 19, 31)),
        "B" : (( 25, 27, 31, 32, 34, 36, 38, 39, 40, 42, 44, 46, 47, 48, 52, 55, 56, 60, 66, 70 ),
               Integer((2, 41), (3, 13), (5, 6), (7, 2), 11, 13, 17, 19, 23, 31, 47)),
        "M" : (( 32, 36, 38, 40, 41, 45, 48, 50, 51, 54, 56, 57, 59, 60, 62, 66, 68, 69, 70, 71, 78, 84,
                87, 88, 92, 93, 94, 95, 104, 105, 110, 119 ), Integer((2, 46), (3, 20), (5, 9), (7, 6),
            (11, 2), (13, 3), 17, 19, 23, 29, 31, 41, 47, 59, 71)),
        "2F4(2)'" : (( 10, 12, 13, 16 ), Integer((2, 11), (3, 3), (5, 2), 13))
    }

    def __init__(self, name):
        self._name = name

    @doc_inherit
    def apex(self):
        return SporadicGroup._groups.get(self._name)[0]

    @doc_inherit
    def order(self):
        return SporadicGroup._groups.get(self._name)[1]

    def __str__(self):
        return self._name

    @staticmethod
    def getAllGroups():
        """Returns all sporadic group names."""
        return SporadicGroup._groups.keys()

class AlternatingGroup(Group):
    """AlternatingGroup(n) represents alternating group of degree n
    """
    def __init__(self, degree):
        self._degree = degree
        self._apex = None
        self._order = None

    def degree(self):
        """Returns alternating group degree."""
        return self._degree

    @doc_inherit
    def apex(self):
        if self._apex is None:
            n = self._degree
            partitions = filter(lambda x: (len(x)+n) % 2 == 0, Partitions(n))
            self._apex = sortAndFilter([reduce(lcm, partition) for partition in partitions])
        return self._apex

    @doc_inherit
    def order(self):
        if self._order is None:
            # n!/2
            self._order = reduce(lambda x, y: x*y, xrange(3, self._degree+1))
        return self._order

    def __str__(self):
        return "Alt({})".format(self._degree)


#####################
# SPECTRA CALCULATION
#####################

def _symplectic_order(n, field):
    n //= 2
    q = field.order()
    o = (q**(n*n)) * reduce(lambda x, y: x*y, (q**(2*i)-1 for i in xrange(1, n+1)))
    return o

def _symplectic_odd_c(n, field):
    """Spectra of symplectic groups in odd characteristic
    """
    n //= 2
    q = field.order()
    p = field.char()
    # (1)
    a1 = SemisimpleElements(q, n)
    # (2)
    a2 = MixedElements(q, n, lambda k: (p**(k-1)+1)//2, lambda k: p**k)
    # (3)
    k = getExponent(2*n-1, p)
    a3 = [] if k is None else [2*p*(2*n-1)]
    return chain(a1, a2, a3)

def _symplectic_even_c(n, field):
    """Spectra of symplectic groups in characteristic 2
    """
    n //= 2
    q = field.order()
    # (1)
    a1 = SemisimpleElements(q, n)
    # (2)
    a2 = (2*elem for elem in SemisimpleElements(q, n-1))
    # (3)
    a3 = MixedElements(q, n, lambda k: 2**(k-1)+1, lambda k: 2**(k+1))
    # (4)
    k = getExponent(n-1, 2)
    a4 = [] if k is None else [(n-1)*4]
    return chain(a1, a2, a3, a4)


def _symplectic(n, field):
    """Spectra of symplectic groups
    """
    if field.char() == 2:
        return _symplectic_even_c(n, field)
    else:
        return _symplectic_odd_c(n, field)

def _p_symplectic_order(n, field):
    # equals to Sp(n, q) if q even
    d = 1 + (field.char() % 2) # 1 if char == 2, otherwise 2
    return _symplectic_order(n, field)//d

def _p_symplectic_odd_c(n, field):
    """Spectra of projective symplectic groups in characteristic 2
    """
    n //= 2
    q = field.order()
    p = field.char()
    # (1)
    t = (q**n-1)//2
    a1 = [t, t+1]
    # (2)
    a2 = SemisimpleElements(q, n, min_length=2)
    # (3)
    a3 = MixedElements(q, n, lambda k: (p**(k-1)+1)//2, lambda k: p**k)
    # (4)
    k = getExponent(2*n-1, p)
    a4 = [] if k is None else [p*(2*n-1)]
    return chain(a1, a2, a3, a4)


def _p_symplectic(n, field):
    """Spectra of projective symplectic group. Note that PSp(n, 2^k) = Sp(n, 2^k)
    """
    if field.char() == 2:
        return _symplectic_even_c(n, field)
    else:
        return _p_symplectic_odd_c(n, field)

def _omega_order(n, field):
    # TODO
    pass

def _omega_odd_c(n, field):
    n = (n-1)//2
    q = field.order()
    p = field.char()
    # (1)
    t = (q**n-1)//2
    a1 = [t, t+1]
    # (2)
    a2 = SemisimpleElements(q, n, min_length=2)
    # (3)
    k = 1
    a3 = []
    while True:
        n1 = n - (p**(k-1) + 1)//2
        if n1 < 1: break
        t = (q**n1-1)//2
        a3.extend([t*p**k, (t+1)*p**k])
        k += 1
    # (4)
    a4 = MixedElements(q, n, lambda k: (p**(k-1)+1)//2, lambda k: p**k, min_length=2)
    # (5)
    k = getExponent(2*n-1, p)
    a5 = [] if k is None else [p*(2*n-1)]
    return chain(a1, a2, a3, a4, a5)

def _omega(n, field):
    if field.char() == 2:
        return _symplectic_even_c(n-1, field)
    else:
        if n == 5:
            return _p_symplectic_odd_c(4, field)
        return _omega_odd_c(n, field)

class ClassicalGroup(Group):
    """Usage:
    ClassicalGroup("PSp", 14, Field(2, 5))
    ClassicalGroup("PSp", 14, 32)
    ClassicalGroup("PSp", 14, 2, 5)
    """
    _groups = {"Sp" : (_symplectic, _symplectic_order),
               "PSp" : (_p_symplectic, _p_symplectic_order),
               "Omega" : (_omega, _omega_order)}

    def __init__(self, name, dimension, *field):
        self._name = name
        self._dim = dimension
        self._field = field[0] if isinstance(field[0], Field) else Field(*field)
        self._apex = None
        self._order = None

    def __str__(self):
        return "{}({}, {})".format(self._name, self._dim, self._field.order())

    def field(self):
        """Returns field of this group
        """
        return self._field

    def apex(self):
        if self._apex is None:
            func = ClassicalGroup._groups.get(self._name)[0]
            self._apex = sortAndFilter(func(self._dim, self._field))
        return self._apex

    def order(self):
        if self._order is None:
            func = ClassicalGroup._groups.get(self._name)[1]
            self._order = func(self._dim, self._field)
        return self._order



