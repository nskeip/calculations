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
import itertools
from spectrum.calculations import numeric
from spectrum.calculations.numeric import gcd, lcm
from spectrum.calculations.semisimple import MixedElements, SemisimpleElements, SpectraElement
from spectrum.calculations.set import FullBoundedSets

__author__ = 'Daniel Lytkin'

sporadic_spectra = {
    'Co1': (16, 22, 23, 24, 26, 28, 33, 35, 36, 39, 40, 42, 60),
    'Ru': (14, 15, 16, 20, 24, 26, 29),
    'Co3': (14, 18, 20, 21, 22, 23, 24, 30),
    'Co2': (11, 16, 18, 20, 23, 24, 28, 30),
    'HS': (7, 8, 11, 12, 15, 20),
    'McL': (8, 9, 11, 12, 14, 30),
    'HN': (9, 12, 14, 19, 21, 22, 25, 30, 35, 40),
    'Th': (19, 20, 21, 24, 27, 28, 30, 31, 36, 39),
    'Suz': (11, 13, 14, 15, 18, 20, 21, 24),
    'Ly': (18, 22, 24, 25, 28, 30, 31, 33, 37, 40, 42, 67),
    "2F4(2)'": (10, 12, 13, 16),
    'Fi23': (16, 17, 22, 23, 24, 26, 27, 28, 35, 36, 39, 42, 60),
    'He': (8, 10, 12, 15, 17, 21, 28),
    'B': (25, 27, 31, 32, 34, 36, 38, 39, 40, 42, 44, 46, 47, 48, 52, 55, 56,
          60, 66, 70),
    'M24': (8, 10, 11, 12, 14, 15, 21, 23),
    'M': (32, 36, 38, 40, 41, 45, 48, 50, 51, 54, 56, 57, 59, 60, 62, 66, 68,
          69, 70, 71, 78, 84, 87, 88, 92, 93, 94, 95, 104, 105, 110, 119),
    'M22': (5, 6, 7, 8, 11),
    'M23': (6, 8, 11, 14, 15, 23),
    "O'N": (11, 12, 15, 16, 19, 20, 28, 31),
    "Fi24'": (16, 17, 22, 23, 24, 26, 27, 28, 29, 33, 35, 36, 39, 42, 45, 60),
    'J4': (16, 23, 24, 28, 29, 30, 31, 35, 37, 40, 42, 43, 44, 66),
    'J1': (6, 7, 10, 11, 15, 19),
    'J2': (7, 8, 10, 12, 15),
    'J3': (8, 9, 10, 12, 15, 17, 19),
    'M11': (5, 6, 8, 11),
    'M12': (6, 8, 10, 11),
    'Fi22': (13, 14, 16, 18, 20, 21, 22, 24, 30)
}




#############################
# SPECTRA OF CLASSICAL GROUPS
#############################
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
    k = numeric.get_exponent(2 * n - 1, p)
    a3 = [] if k is None else [2 * p * (2 * n - 1)]
    return itertools.chain(a1, a2, a3)


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
    k = numeric.get_exponent(n - 1, 2)
    a4 = [] if k is None else [(n - 1) * 4]
    return itertools.chain(a1, a2, a3, a4)


def _symplectic_spectrum(n, field):
    """Spectra of symplectic groups
    """
    if field.char == 2:
        return _symplectic_spectrum_even_c(n, field)
    else:
        return _symplectic_spectrum_odd_c(n, field)


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
    k = numeric.get_exponent(2 * n - 1, p)
    a4 = [] if k is None else [p * (2 * n - 1)]
    return itertools.chain(a1, a2, a3, a4)


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
    k = numeric.get_exponent(2 * n - 1, p)
    a5 = [] if k is None else [p * (2 * n - 1)]
    return itertools.chain(a1, a2, a3, a4, a5)


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
        a5.append(elem.lcm(SpectraElement(p, q, [1], [-1])))
        a5.append(elem.lcm(SpectraElement(p, q, [1], [1])))

    # (6)
    t = (q ** (n - 2) - sign) // 2
    a6 = [p * lcm(q - 1, t), p * lcm(q + 1, t)]
    # (7)
    k = numeric.get_exponent(2 * n - 3, p)
    a7 = [] if k is None else [p * (2 * n - 3) * gcd(4, q ** n - sign) // 2]
    # (8)
    a8 = [p * (q * q - 1), p * (q * q + 1)] if n == 4 and sign == 1 else []
    # (9)
    a9 = [9 * (q - 1), 9 * (q + 1)] if n == 4 and p == 3 and sign == 1 else []
    return itertools.chain(a1, a2, a3, a4, a5, a6, a7, a8, a9)


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
        a5.append(4 * SpectraElement(q=q, partition=[1] + ni,
            signs=[-1] + [1] * len(ni)))
        # (6)
    a6 = (elem.lcm(
        SpectraElement(4, q, [1], [1])) for elem in SemisimpleElements(q, n - 3
        , parity=sign))
    # (7)
    k = numeric.get_exponent(n - 2, 2)
    a7 = [] if k is None else [4 * (n - 2)]
    return itertools.chain(a1, a2, a3, a4, a5, a6, a7)


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
            a6.append(elem.lcm(SpectraElement(p, q, [1], [-1])))
            a6.append(elem.lcm(SpectraElement(p, q, [1], [1])))

        # (7)
        t = (q ** (n - 2) - sign) // 2
        a7 = [p * lcm(q - 1, t), p * lcm(q + 1, t)]
        # (8)
        k = numeric.get_exponent(2 * n - 3, p)
        a8 = [] if k is None else [p * (2 * n - 3)]
        return itertools.chain(a1, a2, a3, a4, a5, a6, a7, a8)

    return spectrum


def _omega_pm_spectrum(sign):
    e = sign

    def spectrum(n, field):
        if field.char == 2:
            return _omega_pm_spectrum_even_c(n, field, e)
        else:
            return _omega_pm_spectrum_odd_c(n, field, e)

    return spectrum


def _special_orthogonal_odd_c_spectrum(n, field):
    n = (n - 1) // 2
    q = field.order
    p = field.char
    # (1)
    a1 = SemisimpleElements(q, n)
    # (2)
    a2 = MixedElements(q, n, lambda k: (p ** (k - 1) + 1) // 2,
        lambda k: p ** k)
    # (3)
    k = numeric.get_exponent(2 * n - 1, p)
    a3 = [] if k is None else [p * (2 * n - 1)]
    return itertools.chain(a1, a2, a3)


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
            a3.append(elem.lcm(SpectraElement(p, q, [1], [-1])))
            a3.append(elem.lcm(SpectraElement(p, q, [1], [1])))
            # (4)
        k = numeric.get_exponent(2 * n - 3, p)
        a4 = [] if k is None else [2 * p * (2 * n - 3)]
        return itertools.chain(a1, a2, a3, a4)

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
        k = numeric.get_exponent(n - 1, p)
        a4 = [] if k is None else [p * (n - 1)]
        return itertools.chain(a1, a2, a3, a4)

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
        k = numeric.get_exponent(n - 1, p)
        a5 = [] if k is None else [p * (n - 1) * d]
        # (6)
        a6 = [p * gcd(2, q - 1) * (q + e)] if n == 4 else []
        return itertools.chain(a1, a2, a3, a4, a5, a6)

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
            a2.append(lcm(q ** pair[0] + signs[0], q ** pair[1] + signs[1]) //
                      gcd(n // gcd(n1, n - n1), q - e))
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
        k = numeric.get_exponent(n - 1, p)
        a6 = [] if k is None else [p * (n - 1)]
        return itertools.chain(a1, a2, a3, a4, a5, a6)

    return spectrum


classical_spectra = {
    "Sp": _symplectic_spectrum,
    "PSp": _projective_symplectic_spectrum,
    "Omega": _omega_spectrum,
    "Omega+": _omega_pm_spectrum(1),
    "Omega-": _omega_pm_spectrum(-1),
    "POmega+": _projective_omega_pm_spectrum(1),
    "POmega-": _projective_omega_pm_spectrum(-1),
    "SO": _special_orthogonal_odd_c_spectrum,
    "SO+": _special_orthogonal_pm_spectrum(1),
    "SO-": _special_orthogonal_pm_spectrum(-1),
    "PGL": _projective_general_linear_spectrum(1),
    "PGU": _projective_general_linear_spectrum(-1),
    "SL": _special_linear_spectrum(1),
    "SU": _special_linear_spectrum(-1),
    "PSL": _projective_special_linear_spectrum(1),
    "PSU": _projective_special_linear_spectrum(-1),
    }


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


exceptional_spectra = {
    "2F4": _2f4_spectrum,
    "G2": _g2_spectrum,
    "2G2": _2g2_spectrum,
    "2B2": _2b2_spectrum,
    }