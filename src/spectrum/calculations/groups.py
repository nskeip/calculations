from itertools import chain
from numeric import *
from partition import Partitions
from semisimple import SemisimpleElements, MixedElements, evaluate
from set import FullBoundedSets
from spectrum.calculations.orders import sporadic_orders
from spectrum.calculations.spectra import sporadic_spectra
from spectrum.tools.tools import doc_inherit


__author__ = 'Daniel Lytkin'

_prod = lambda seq: reduce(lambda x, y: x * y, seq, 1)

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
    _groups = ('M11', 'M12', 'J1', 'M22', 'J2', 'M23', "2F4(2)'", 'HS', 'J3',
               'M24', 'McL', 'He', 'Ru', 'Suz', "O'N", 'Co3', 'Co2', 'Fi22',
               'HN', 'Ly', 'Th', 'Fi23', 'Co1', 'J4', "Fi24'", 'B', 'M')

    def __init__(self, name):
        self._name = name

    @doc_inherit
    def apex(self):
        return sporadic_spectra.get(self._name, [])

    @doc_inherit
    def order(self):
        return sporadic_orders.get(self._name)

    def __str__(self):
        return self._name

    @staticmethod
    def all_groups():
        """Returns all sporadic_spectra group names."""
        return SporadicGroup._groups


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
            self._order = _prod(xrange(3, self._degree + 1))
        return self._order

    def __str__(self):
        return "Alt({})".format(self._degree)


#############################
# SPECTRA OF CLASSICAL GROUPS
#############################

def _symplectic_order(n, field):
    n //= 2
    q = field.order
    return (Integer({field.char: field.pow * n * n}) *
            _prod((Integer(q ** i - 1) *
                   Integer(q ** i + 1) for i in xrange(1, n + 1))))


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
    #d = 1 if field.char == 2 else 2
    o = _symplectic_order(n, field)
    if field.char != 2:
        o.div_by_prime(2)
    return o


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
        o = (Integer({field.char: field.pow * n * (n - 1)}) *
             Integer(q ** n - e) *
             _prod((Integer(q ** i - 1) *
                    Integer(q ** i + 1) for i in xrange(1, n))))
        if field.char != 2:
            o.div_by_prime(2)
        return o

    return order


def _projective_omega_pm_order(sign):
    e = sign

    def order(n, field):
        omega_order = _omega_pm_order(e)(n, field)
        q = field.order
        n //= 2
        # gcd(4, q^n-e)
        omega_order.div_by_prime(2)
        if e == 1:
            divisor = 1 if (n % 2 == 1 and q % 4 == 3) else 2
        else:
            divisor = 2 if (n % 2 == 1 and q % 4 == 3) else 1
        if divisor > 1:
            omega_order.div_by_prime(2)
        return omega_order * gcd(q - e, 2)

    return order


def _special_orthogonal_order(sign):
    e = sign

    def order(n, field):
        q = field.order
        n //= 2
        part = _prod((Integer(q ** k - 1) *
                      Integer(q ** k + 1) for k in xrange(1, n)))
        if not e:
            return (part * Integer({field.char: field.pow * n * n}) *
                    Integer(q ** n - 1) * Integer(q ** n + 1))
        if field.char == 2:
            part *= 2
        return (part * Integer({field.char: field.pow * n * (n - 1)}) *
                Integer(q ** n - e))

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
    return (Integer({field.char: field.pow * (n * (n - 1) / 2)}) *
            _prod((Integer(q ** i - 1) for i in xrange(2, n + 1))))


def _projective_general_unitary_order(n, field):
    q = field.order
    return (Integer({field.char: field.pow * (n * (n - 1) / 2)}) *
            _prod((Integer(q ** i - 1) *
                   Integer(q ** i + 1) for i in xrange(1, n // 2 + 1))) *
            _prod((Integer(q ** (2 * i + 1) + 1)) for i in xrange(1,
                (n + 1) // 2)))


def _projective_special_linear_order(n, field):
    q = field.order
    return (Integer({field.char: field.pow * (n * (n - 1) / 2)}) *
            _prod((Integer(q ** i - 1) for i in xrange(3, n + 1))) *
            Integer(q + 1) * Integer((q - 1) // gcd(n, q - 1)))


def _projective_special_unitary_order(n, field):
    q = field.order
    return (Integer({field.char: field.pow * (n * (n - 1) / 2)}) *
            _prod((Integer(q ** i - 1) *
                   Integer(q ** i + 1) for i in xrange(2, n // 2 + 1))) *
            _prod((Integer(q ** (2 * i + 1) + 1)) for i in xrange(1,
                (n + 1) // 2)) *
            Integer(q - 1) * Integer((q + 1) // gcd(n, q + 1)))


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
            _projective_omega_pm_spectrum(1),
            _projective_omega_pm_order(1)),
        "POmega-": (
            _projective_omega_pm_spectrum(-1),
            _projective_omega_pm_order(-1)),
        "SO": (_special_orthogonal_odd_c, _special_orthogonal_order(0)),
        "SO+": (
            _special_orthogonal_pm_spectrum(1),
            _special_orthogonal_order(1)),
        "SO-": (
            _special_orthogonal_pm_spectrum(-1),
            _special_orthogonal_order(-1)),
        "PGL": (
            _projective_general_linear_spectrum(1),
            _projective_general_linear_order),
        "PGU": (
            _projective_general_linear_spectrum(-1),
            _projective_general_unitary_order),
        "SL": (_special_linear_spectrum(1), _projective_general_linear_order),
        "SU": (
            _special_linear_spectrum(-1),
            _projective_general_unitary_order),
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


def _g2_spectrum(field):
    q = field.order
    p = field.char
    if p == 2:
        return [8, 12, 2 * (q - 1), 2 * (q + 1), q ** 2 - 1, q ** 2 - q + 1,
                q ** 2 + q + 1]
    if p == 3 or p == 5:
        return [p ** 2, p * (q - 1), p * (q + 1), q ** 2 - 1, q ** 2 - q + 1,
                q ** 2 + q + 1]
    return [p * (q - 1), p * (q + 1), q ** 2 - 1, q ** 2 - q + 1,
            q ** 2 + q + 1]


def _2f4_spectrum(field):
    q = field.order
    sq = 2 ** ((field.pow + 1) // 2)
    ssq = 2 ** ((3 * field.pow + 1) // 2)
    return [12, 16, 4 * (q - 1), 2 * (q + 1), 4 * (q - sq + 1),
            4 * (q + sq + 1), q ** 2 - 1, q ** 2 + 1, q ** 2 - q + 1,
            (q - 1) * (q - sq + 1),
            (q - 1) * (q + sq + 1),
            q ** 2 - ssq + q - sq + 1,
            q ** 2 + ssq + q + sq + 1]


def _2b2_spectrum(field):
    q = field.order
    sq = 2 ** ((field.pow + 1) // 2)
    return [4, q - sq + 1, q + sq + 1, q - 1]


def _2g2_spectrum(field):
    q = field.order
    sq = 3 ** ((field.pow + 1) // 2)
    return [9, 6, (q + 1) // 2, q - 1, q - sq + 1, q + sq + 1]


def _order_product(field, pow, pluses, minuses):
    q = field.order
    return (Integer({field.char: field.pow * pow}) *
            _prod((Integer(q ** i + 1) for i in pluses)) *
            _prod((Integer(q ** i - 1) for i in minuses)))


def _e6_order(field):
    q = field.order
    return (_order_product(field, 36, [6, 4, 3, 3, 2, 1, 1], [9, 5, 3, 3, 1]) *
            Integer((q - 1) // gcd(3, q - 1)))


def _e7_order(field):
    q = field.order
    return (_order_product(field, 63, [9, 7, 6, 5, 4, 3, 3, 2, 1, 1],
        [9, 7, 5, 3, 3, 1]) * Integer((q - 1) // gcd(2, q - 1)))


def _e8_order(field):
    return (_order_product(field, 120,
        [15, 12, 10, 9, 7, 6, 6, 5, 4, 3, 3, 2, 1, 1],
        [15, 9, 7, 5, 3, 3, 1, 1]))


def _f4_order(field):
    return _order_product(field, 24, [6, 4, 3, 3, 2, 1, 1], [3, 3, 1, 1])


def _g2_order(field):
    return _order_product(field, 6, [3, 1], [3, 1])


def _2e6_order(field):
    q = field.order
    return (_order_product(field, 36, [9, 6, 5, 4, 3, 3, 2, 1], [3, 3, 1, 1]) *
            Integer((q + 1) // gcd(3, q + 1)))


def _3d4_order(field):
    q = field.order
    return _order_product(field, 12, [3, 1], [3, 1]) * (q ** 8 + q ** 4 + 1)


def _2b2_order(field):
    q = field.order
    return Integer({2: field.pow * 2}) * (q ** 2 + 1) * (q - 1)


def _2f4_order(field):
    return _order_product(field, 12, [6, 3, 2, 1], [1, 1])


def _2g2_order(field):
    q = field.order
    return Integer({3: field.pow * 3}) * (q ** 3 + 1) * (q - 1)


class ExceptionalGroup(Group):
    _groups = {
        "E6": (None, _e6_order),
        "2E6": (None, _2e6_order),
        "E7": (None, _e7_order),
        "E8": (None, _e8_order),
        "F4": (None, _f4_order),
        "2F4": (_2f4_spectrum, _2f4_order),
        "G2": (_g2_spectrum, _g2_order),
        "2G2": (_2g2_spectrum, _2g2_order),
        "2B2": (_2b2_spectrum, _2b2_order),
        "3D4": (None, _3d4_order)
    }

    def __init__(self, name, *field):
        self._name = name
        self._field = field[0] if isinstance(field[0], Field) else Field(
            *field)
        self._apex = None
        self._order = None


    def __str__(self):
        return "{}({})".format(self._name, self._field.order)

    @staticmethod
    def types():
        return sorted(ExceptionalGroup._groups.keys(),
            key=lambda key: key.strip("2"))

    @property
    def field(self):
        """Returns field of this group
        """
        return self._field

    def apex(self):
        if self._apex is None:
            func = ExceptionalGroup._groups.get(self._name)[0]
            self._apex = sort_and_filter(func(self._field))
        return self._apex

    def order(self):
        if self._order is None:
            func = ExceptionalGroup._groups.get(self._name)[1]
            self._order = func(self._field)
        return self._order

