from itertools import chain
from numeric import *
from partition import Partitions
from semisimple import SemisimpleElements, MixedElements, evaluate
from set import FullBoundedSets
from spectrum.tools.tools import doc_inherit


__author__ = 'Daniel Lytkin'

class Field:
    """Finite field.
    Can be created as Field(order) or Field(base, pow) where base**pow is the
    order of the field. `order' must be a prime power, otherwise the wrong
    field will be created.

    """

    def __init__(self, *arg):
        if len(arg) == 1:
            if arg[0] <= 1:
                raise ValueError("Field order must be at least 2")
            self._base = first_divisor(arg[0])
            self._pow = 1
            self._order = self._base
            while self._order < arg[0]:
                self._pow += 1
                self._order *= self._base
        elif len(arg) == 2:
            self._base, self._pow = arg[0], arg[1]
            if self._pow < 1 or self._base < 2:
                raise ValueError("Field order must be at least 2")
            self._order = self._base ** self._pow

    @property
    def order(self): return self._order

    @property
    def char(self): return self._base

    @property
    def pow(self): return self._pow


class Group(object):
    """Interface for finite groups with method to calculate their spectra
    """

    def apex(self):
        """Returns apex of the group, which is the set of its element orders
        with all divisors filtered out.

        """
        raise NotImplementedError()

    def order(self):
        """Returns group order."""
        raise NotImplementedError()


class SporadicGroup(Group):
    _groups = {
        "M11": (( 5, 6, 8, 11 ), Integer((2, 4), (3, 2), 5, 11)),
        "M12": (( 6, 8, 10, 11 ), Integer((2, 6), (3, 3), 5, 11)),
        "M22": (( 5, 6, 7, 8, 11 ), Integer((2, 7), (3, 2), 5, 7, 11)),
        "M23": (( 6, 8, 11, 14, 15, 23 ),
                Integer((2, 7), (3, 2), 5, 7, 11, 23)),
        "M24": (( 8, 10, 11, 12, 14, 15, 21, 23 ),
                Integer((2, 10), (3, 3), 5, 7, 11, 23)),
        "J1": (( 6, 7, 10, 11, 15, 19 ), Integer((2, 3), 3, 5, 7, 11, 19)),
        "J2": (( 7, 8, 10, 12, 15 ), Integer((2, 7), (3, 3), (5, 2), 7)),
        "J3": (( 8, 9, 10, 12, 15, 17, 19 ),
               Integer((2, 7), (3, 5), 5, 17, 19)),
        "J4": (( 16, 23, 24, 28, 29, 30, 31, 35, 37, 40, 42, 43, 44, 66 ),
               Integer((2, 21), (3, 3), 5, 7, (11, 3), 23, 29, 31, 37, 43)),
        "Co1": (( 16, 22, 23, 24, 26, 28, 33, 35, 36, 39, 40, 42, 60 ),
                Integer((2, 21), (3, 9), (5, 4), (7, 2), 11, 13, 23)),
        "Co2": (( 11, 16, 18, 20, 23, 24, 28, 30 ),
                Integer((2, 18), (3, 6), (5, 3), 7, 11, 23)),
        "Co3": (( 14, 18, 20, 21, 22, 23, 24, 30 ),
                Integer((2, 10), (3, 7), (5, 3), 7, 11, 23)),
        "Fi22": (( 13, 14, 16, 18, 20, 21, 22, 24, 30 ),
                 Integer((2, 17), (3, 9), (5, 2), 7, 11, 13)),
        "Fi23": (( 16, 17, 22, 23, 24, 26, 27, 28, 35, 36, 39, 42, 60 ),
                 Integer((2, 18), (3, 13), (5, 2), 7, 11, 13, 17, 23)),
        "Fi24'": (
            ( 16, 17, 22, 23, 24, 26, 27, 28, 29, 33, 35, 36, 39, 42, 45, 60 ),
            Integer((2, 21), (3, 16), (5, 2), (7, 3), 11, 13, 17, 23, 29)),
        "HS": (( 7, 8, 11, 12, 15, 20 ),
               Integer((2, 9), (3, 2), (5, 3), 7, 11)),
        "McL": (( 8, 9, 11, 12, 14, 30 ),
                Integer((2, 7), (3, 6), (5, 3), 7, 11)),
        "He": (( 8, 10, 12, 15, 17, 21, 28 ),
               Integer((2, 10), (3, 3), (5, 2), (7, 3), 17)),
        "Ru": (( 14, 15, 16, 20, 24, 26, 29 ),
               Integer((2, 14), (3, 3), (5, 3), 7, 13, 29)),
        "Suz": (( 11, 13, 14, 15, 18, 20, 21, 24 ),
                Integer((2, 13), (3, 7), (5, 2), 7, 11, 13)),
        "O'N": (( 11, 12, 15, 16, 19, 20, 28, 31 ),
                Integer((2, 9), (3, 4), 5, (7, 3), 11, 19, 31)),
        "HN": (( 9, 12, 14, 19, 21, 22, 25, 30, 35, 40 ),
               Integer((2, 14), (3, 6), (5, 6), 7, 11, 19)),
        "Ly": (( 18, 22, 24, 25, 28, 30, 31, 33, 37, 40, 42, 67 ),
               Integer((2, 8), (3, 7), (5, 6), 7, 11, 31, 37, 67)),
        "Th": (( 19, 20, 21, 24, 27, 28, 30, 31, 36, 39 ),
               Integer((2, 15), (3, 10), (5, 3), (7, 2), 13, 19, 31)),
        "B": ((25, 27, 31, 32, 34, 36, 38, 39, 40, 42, 44, 46, 47, 48, 52, 55,
               56, 60, 66, 70 ),
              Integer((2, 41), (3, 13), (5, 6), (7, 2), 11, 13, 17, 19, 23, 31,
                  47)),
        "M": ((32, 36, 38, 40, 41, 45, 48, 50, 51, 54, 56, 57, 59, 60, 62, 66,
               68, 69, 70, 71, 78, 84,
               87, 88, 92, 93, 94, 95, 104, 105, 110, 119 ),
              Integer((2, 46), (3, 20), (5, 9), (7, 6),
                  (11, 2), (13, 3), 17, 19, 23, 29, 31, 41, 47, 59, 71)),
        "2F4(2)'": (( 10, 12, 13, 16 ), Integer((2, 11), (3, 3), (5, 2), 13))
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
    def all_groups():
        """Returns all sporadic group names."""
        return [k for (k, v) in sorted(SporadicGroup._groups.iteritems(),
            key=lambda x: int(x[1][1]))]


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
            partitions = filter(lambda x: (len(x) + n) % 2 == 0, Partitions(n))
            self._apex = sort_and_filter(
                [reduce(lcm, partition) for partition in partitions])
        return self._apex

    @doc_inherit
    def order(self):
        if self._order is None:
            # n!/2
            self._order = reduce(lambda x, y: x * y,
                xrange(3, self._degree + 1))
        return self._order

    def __str__(self):
        return "Alt({})".format(self._degree)


#############################
# SPECTRA OF CLASSICAL GROUPS
#############################

def _symplectic_order(n, field):
    n //= 2
    q = field.order
    o = (q ** (n * n)) * reduce(lambda x, y: x * y,
        (q ** (2 * i) - 1 for i in xrange(1, n + 1)))
    return o


def _symplectic_spectrum_odd_c(n, field):
    """Spectra of symplectic groups in odd characteristic
    """
    n //= 2
    q = field.order
    p = field.char
    # (1)
    a1 = SemisimpleElements(q, n)
    # (2)
    a2 = MixedElements(q, n, lambda k: (p ** (k - 1) + 1) // 2,
        lambda k: p ** k)
    # (3)
    k = get_exponent(2 * n - 1, p)
    a3 = [] if k is None else [2 * p * (2 * n - 1)]
    return chain(a1, a2, a3)


def _symplectic_spectrum_even_c(n, field):
    """Spectra of symplectic groups in characteristic 2
    """
    n //= 2
    q = field.order
    # (1)
    a1 = SemisimpleElements(q, n)
    # (2)
    a2 = (2 * elem for elem in SemisimpleElements(q, n - 1))
    # (3)
    a3 = MixedElements(q, n, lambda k: 2 ** (k - 1) + 1,
        lambda k: 2 ** (k + 1))
    # (4)
    k = get_exponent(n - 1, 2)
    a4 = [] if k is None else [(n - 1) * 4]
    return chain(a1, a2, a3, a4)


def _symplectic_spectrum(n, field):
    """Spectra of symplectic groups
    """
    if field.char == 2:
        return _symplectic_spectrum_even_c(n, field)
    else:
        return _symplectic_spectrum_odd_c(n, field)


def _projective_symplectic_order(n, field):
    # equals to Sp(n, q) if q even
    d = 1 + (field.char % 2) # 1 if char == 2, otherwise 2
    return _symplectic_order(n, field) // d


def _projective_symplectic_spectrum_odd_c(n, field):
    """Spectra of projective symplectic groups in characteristic 2
    """
    n //= 2
    q = field.order
    p = field.char
    # (1)
    t = (q ** n - 1) // 2
    a1 = [t, t + 1]
    # (2)
    a2 = SemisimpleElements(q, n, min_length=2)
    # (3)
    a3 = MixedElements(q, n, lambda k: (p ** (k - 1) + 1) // 2,
        lambda k: p ** k)
    # (4)
    k = get_exponent(2 * n - 1, p)
    a4 = [] if k is None else [p * (2 * n - 1)]
    return chain(a1, a2, a3, a4)


def _projective_symplectic_spectrum(n, field):
    """Spectra of projective symplectic group. Note that
    PSp(n, 2^k) = Sp(n, 2^k)
    """
    if field.char == 2:
        return _symplectic_spectrum_even_c(n, field)
    else:
        return _projective_symplectic_spectrum_odd_c(n, field)


def _omega_spectrum_odd_c(n, field):
    n = (n - 1) // 2
    q = field.order
    p = field.char
    # (1)
    t = (q ** n - 1) // 2
    a1 = [t, t + 1]
    # (2)
    a2 = SemisimpleElements(q, n, min_length=2)
    # (3)
    k = 1
    a3 = []
    while True:
        n1 = n - (p ** (k - 1) + 1) // 2
        if n1 < 1: break
        t = (q ** n1 - 1) // 2
        a3.extend([t * p ** k, (t + 1) * p ** k])
        k += 1
        # (4)
    a4 = MixedElements(q, n, lambda k: (p ** (k - 1) + 1) // 2,
        lambda k: p ** k, min_length=2)
    # (5)
    k = get_exponent(2 * n - 1, p)
    a5 = [] if k is None else [p * (2 * n - 1)]
    return chain(a1, a2, a3, a4, a5)


def _omega_spectrum(n, field):
    """Spectra of Omega_{2n+1}(q)
    """
    if field.char == 2:
        return _symplectic_spectrum_even_c(n - 1, field)
    else:
        if n == 5:
            return _projective_symplectic_spectrum_odd_c(4, field)
        return _omega_spectrum_odd_c(n, field)


def _omega_pm_spectrum_odd_c(n, field, sign):
    n //= 2
    q = field.order
    p = field.char
    nk = lambda k: (p ** (k - 1) + 3) // 2
    # (1)
    a1 = [(q ** n - sign) // 2]
    # (2)
    a2 = SemisimpleElements(q, n, min_length=2, parity=sign)
    # (3)
    a3 = []
    k = 1
    while True:
        n_k = nk(k)
        if n_k >= n: break
        dk = gcd(4, q ** n_k - sign) // 2
        a3.append(p ** k * lcm(dk, (q ** (n - n_k) + 1) // dk))
        a3.append(p ** k * lcm(dk, (q ** (n - n_k) - 1) // dk))
        k += 1
        # (4)
    a4 = MixedElements(q, n, nk, lambda k: p ** k, min_length=2)
    # (5)
    a5 = []
    for elem in SemisimpleElements(q, n - 2, min_length=2, parity=sign):
        a5.append(p * lcm(q - 1, elem))
        a5.append(p * lcm(q + 1, elem))
        # (6)
    t = (q ** (n - 2) - sign) // 2
    a6 = [p * lcm(q - 1, t), p * lcm(q + 1, t)]
    # (7)
    k = get_exponent(2 * n - 3, p)
    a7 = [] if k is None else [p * (2 * n - 3) * gcd(4, q ** n - sign) // 2]
    # (8)
    a8 = [p * (q * q - 1), p * (q * q + 1)] if n == 4 and sign == 1 else []
    # (9)
    a9 = [9 * (q - 1), 9 * (q + 1)] if n == 4 and p == 3 and sign == 1 else []
    return chain(a1, a2, a3, a4, a5, a6, a7, a8, a9)


def _omega_pm_spectrum_even_c(n, field, sign):
    n //= 2
    q = field.order
    # (1)
    a1 = SemisimpleElements(q, n, parity=sign)
    # (2)
    a2 = MixedElements(q, n, lambda k: 2 ** (k - 1) + 2,
        lambda k: 2 ** (k + 1))
    # (3)
    a3 = (2 * elem for elem in SemisimpleElements(q, n - 2))
    # (4)
    a4 = []
    for elem in SemisimpleElements(q, n - 2, parity=sign):
        a4.append(2 * lcm(q - 1, elem))
        a4.append(2 * lcm(q + 1, elem))
        # (5)
    a5 = []
    signMod = 0 if sign == 1 else 1
    for ni in FullBoundedSets(n - 3):
        if len(ni) % 2 != signMod: continue
        a5.append(4 * lcm(q - 1, evaluate(q, ni, 1)))
        # (6)
    a6 = (4 * lcm(q + 1, elem) for elem in SemisimpleElements(q, n - 3,
        parity=sign))
    # (7)
    k = get_exponent(n - 2, 2)
    a7 = [] if k is None else [4 * (n - 2)]
    return chain(a1, a2, a3, a4, a5, a6, a7)


def _equal_two_part(a, b):
    """Returns True iff a_{2} = b_{2}
    """
    while a % 2 == 0 and b % 2 == 0:
        a, b = a // 2, b // 2
    return a % 2 == 1 and b % 2 == 1


def _projective_omega_pm_spectrum(sign):
    e = sign

    def spectrum(n, field):
        n //= 2
        q = field.order
        p = field.char
        # if gcd(4, q^n-e) != 4, then POmega = Omega
        b = n % 2 == 1 and q % 4 == 3  # true iff gcd(4, q^n+1)=4
        if not ((b and e == -1) or q % 2 == 1):
            return _omega_pm_spectrum(e)(n * 2, field)

        nk = lambda k: (p ** (k - 1) + 3) // 2
        # (1)
        a1 = [(q ** n - sign) // 4]
        # (2)
        a2 = []
        for n1 in xrange(1, n):
            for e1 in [-1, 1]:
                a = q ** n1 - e1
                b = q ** (n - n1) - e * e1
                d = 2 if _equal_two_part(a, b) else 1
                a2.append(lcm(a, b) // d)
            # (3)
        a3 = SemisimpleElements(q, n, min_length=3, parity=sign)
        # (4)
        a4 = []
        k = 1
        while True:
            n_k = nk(k)
            if n_k >= n: break
            a4.append(p ** k * (q ** (n - n_k) + 1) // 2)
            a4.append(p ** k * (q ** (n - n_k) - 1) // 2)
            k += 1
            # (5)
        a5 = MixedElements(q, n, nk, lambda k: p ** k, min_length=2)
        # (6)
        a6 = []
        for elem in SemisimpleElements(q, n - 2, min_length=2, parity=sign):
            a6.append(p * lcm(q - 1, elem))
            a6.append(p * lcm(q + 1, elem))
            # (7)
        t = (q ** (n - 2) - sign) // 2
        a7 = [p * lcm(q - 1, t), p * lcm(q + 1, t)]
        # (8)
        k = get_exponent(2 * n - 3, p)
        a8 = [] if k is None else [p * (2 * n - 3)]
        return chain(a1, a2, a3, a4, a5, a6, a7, a8)

    return spectrum


def _omega_pm_spectrum(sign):
    e = sign

    def spectrum(n, field):
        if field.char == 2:
            return _omega_pm_spectrum_even_c(n, field, e)
        else:
            return _omega_pm_spectrum_odd_c(n, field, e)

    return spectrum


def _omega_pm_order(sign):
    e = sign

    def order(n, field):
        q = field.order
        n //= 2
        return q ** (n * (n - 1)) * (q ** n - e) * reduce(lambda x, y: x * y,
            ((q ** (2 * i) - 1) for i in xrange(1, n))) // gcd(q - e, 2)

    return order


def _projective_omega_pm_order(sign):
    e = sign

    def order(n, field):
        omega_order = _omega_pm_order(e)(n, field)
        q = field.order
        n //= 2
        # gcd(4, q^n-e)
        if e == 1:
            divisor = 2 if (n % 2 == 1 and q % 4 == 3) else 4
        else:
            divisor = 4 if (n % 2 == 1 and q % 4 == 3) else 2
        return omega_order * gcd(q - e, 2) // divisor

    return order


def _special_orthogonal_order(sign):
    e = sign

    def order(n, field):
        q = field.order
        n //= 2
        part = reduce(lambda x, y: x * y,
            (q ** (2 * k) - 1 for k in xrange(1, n)))
        if not e:
            return part * q ** (n * n) * (q ** (2 * n) - 1)
        if field.char == 2: part *= 2
        return part * q ** (n * (n - 1)) * (q ** n - e)

    return order


def _special_orthogonal_odd_c(n, field):
    n = (n - 1) // 2
    q = field.order
    p = field.char
    # (1)
    a1 = SemisimpleElements(q, n)
    # (2)
    a2 = MixedElements(q, n, lambda k: (p ** (k - 1) + 1) // 2,
        lambda k: p ** k)
    # (3)
    k = get_exponent(2 * n - 1, p)
    a3 = [] if k is None else [p * (2 * n - 1)]
    return chain(a1, a2, a3)


def _special_orthogonal_pm_spectrum(sign):
    e = sign

    def spectrum(n, field):
        n //= 2
        q = field.order
        p = field.char
        # (1)
        a1 = SemisimpleElements(q, n, parity=e)
        # (2)
        a2 = MixedElements(q, n, lambda k: (p ** (k - 1) + 3) // 2,
            lambda k: p ** k)
        # (3)
        a3 = []
        for elem in SemisimpleElements(q, n - 2, parity=e):
            a3.append(p * lcm(q - 1, elem))
            a3.append(p * lcm(q + 1, elem))
            # (4)
        k = get_exponent(2 * n - 3, p)
        a4 = [] if k is None else [2 * p * (2 * n - 3)]
        return chain(a1, a2, a3, a4)

    return spectrum


# PGL and PGU
def _projective_general_linear_spectrum(sign):
    e = sign

    def spectrum(n, field):
        q = field.order
        p = field.char
        # (1)
        eps = 1 if n % 2 == 0 else e
        a1 = [(q ** n - eps) // (q - e)]
        # (2)
        a2 = SemisimpleElements(q, n, min_length=2, sign=e)
        # (3)
        a3 = MixedElements(q, n, lambda k: p ** (k - 1) + 1,
            lambda k: p ** k, sign=e)
        # (4)
        k = get_exponent(n - 1, p)
        a4 = [] if k is None else [p * (n - 1)]
        return chain(a1, a2, a3, a4)

    return spectrum


def _special_linear_spectrum(sign):
    e = sign

    def spectrum(n, field):
        q = field.order
        p = field.char
        # (1)
        eps = 1 if n % 2 == 0 else e
        a1 = [(q ** n - eps) // (q - e)]
        # (2)
        a2 = SemisimpleElements(q, n, min_length=2, sign=e)
        # (3)
        a3 = []
        k = 1
        d = gcd(n, q - e)
        while True:
            n1 = n - p ** (k - 1) - 1
            if n1 < 1: break
            eps = 1 if n1 % 2 == 0 else e
            a3.append(p ** k * (q ** n1 - eps) / gcd(d, n1))
            k += 1
            # (4)
        a4 = MixedElements(q, n, lambda k: p ** (k - 1) + 1,
            lambda k: p ** k, min_length=2, sign=e)
        # (5)
        k = get_exponent(n - 1, p)
        a5 = [] if k is None else [p * (n - 1) * d]
        # (6)
        a6 = [p * gcd(2, q - 1) * (q + e)] if n == 4 else []
        return chain(a1, a2, a3, a4, a5, a6)

    return spectrum


def _projective_special_linear_spectrum(sign):
    e = sign

    def spectrum(n, field):
        q = field.order
        p = field.char
        d = gcd(n, q - e)
        # (1)
        eps = 1 if n % 2 == 0 else e
        a1 = [(q ** n - eps) // ((q - e) * d)]
        # (2)
        a2 = []
        eps = lambda s: 1 if s % 2 == 0 else e
        for n1 in xrange(1, (n + 2) // 2):
            pair = (n1, n - n1)
            signs = (-eps(n1), -eps(n - n1))
            a2.append(evaluate(q, pair, ei=signs) // gcd(n // gcd(n1, n - n1),
                q - e))
            # (3)
        a3 = SemisimpleElements(q, n, min_length=3, sign=e)
        # (4)
        a4 = []
        k = 1
        while True:
            n1 = n - p ** (k - 1) - 1
            if n1 < 1: break
            eps = 1 if n1 % 2 == 0 else e
            a4.append(p ** k * (q ** n1 - eps) / d)
            k += 1
            # (5)
        a5 = MixedElements(q, n, lambda k: p ** (k - 1) + 1,
            lambda k: p ** k, min_length=2, sign=e)
        # (6)
        k = get_exponent(n - 1, p)
        a6 = [] if k is None else [p * (n - 1)]
        return chain(a1, a2, a3, a4, a5, a6)

    return spectrum


def _projective_general_linear_order(n, field):
    q = field.order
    return q ** (n * (n - 1) / 2) * reduce(lambda x, y: x * y,
        (q ** i - 1 for i in xrange(2, n + 1)))


def _projective_general_unitary_order(n, field):
    q = field.order
    return q ** (n * (n - 1) / 2) * reduce(lambda x, y: x * y,
        ((q ** i - 1 if i % 2 == 0 else q ** i + 1) for i in xrange(2, n + 1)))


def _projective_special_linear_order(n, field):
    q = field.order
    return _projective_general_linear_order(n, field) / gcd(n, q - 1)


def _projective_special_unitary_order(n, field):
    q = field.order
    return _projective_general_unitary_order(n, field) / gcd(n, q + 1)


class ClassicalGroup(Group):
    """Usage:
    ClassicalGroup("PSp", 14, Field(2, 5))
    ClassicalGroup("PSp", 14, 32)
    ClassicalGroup("PSp", 14, 2, 5)
    """
    _groups = {
        "Sp": (_symplectic_spectrum, _symplectic_order),
        "PSp": (_projective_symplectic_spectrum, _projective_symplectic_order),
        "Omega": (_omega_spectrum, _projective_symplectic_order),
        "Omega+": (_omega_pm_spectrum(1), _omega_pm_order(1)),
        "Omega-": (_omega_pm_spectrum(-1), _omega_pm_order(-1)),
        "POmega+": (
        _projective_omega_pm_spectrum(1), _projective_omega_pm_order(1)),
        "POmega-": (
        _projective_omega_pm_spectrum(-1), _projective_omega_pm_order(-1)),
        "SO": (_special_orthogonal_odd_c, _special_orthogonal_order(0)),
        "SO+": (
        _special_orthogonal_pm_spectrum(1), _special_orthogonal_order(1)),
        "SO-": (
        _special_orthogonal_pm_spectrum(-1), _special_orthogonal_order(-1)),
        "PGL": (
            _projective_general_linear_spectrum(1),
            _projective_general_linear_order),
        "PGU": (
            _projective_general_linear_spectrum(-1),
            _projective_general_unitary_order),
        "SL": (_special_linear_spectrum(1), _projective_general_linear_order),
        "SU": (_special_linear_spectrum(-1), _projective_general_unitary_order)
        ,
        "PSL": (
            _projective_special_linear_spectrum(1),
            _projective_special_linear_order),
        "PSU": (
            _projective_special_linear_spectrum(-1),
            _projective_special_unitary_order)
    }

    def __init__(self, name, dimension, *field):
        self._name = name
        self._dim = dimension
        self._field = field[0] if isinstance(field[0], Field) else Field(
            *field)
        self._apex = None
        self._order = None

    def __str__(self):
        return "{}({}, {})".format(self._name, self._dim, self._field.order)

    @staticmethod
    def types():
        return sorted(ClassicalGroup._groups.keys(),
            key=lambda key: key.strip("P"))

    @property
    def field(self):
        """Returns field of this group
        """
        return self._field

    def apex(self):
        if self._apex is None:
            func = ClassicalGroup._groups.get(self._name)[0]
            self._apex = sort_and_filter(func(self._dim, self._field))
        return self._apex

    def order(self):
        if self._order is None:
            func = ClassicalGroup._groups.get(self._name)[1]
            self._order = func(self._dim, self._field)
        return self._order



