"""
Bibliography:
[1] Buturlakin A. A., “Spectra of finite symplectic and orthogonal groups”, Siberian Adv. in Math., 21, No. 3, 176–210
    (2011).
[2] Buturlakin A. A., “Spectra of finite linear and unitary groups”, Algebra and Logic, Vol. 47, No. 2, (2008).


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
import typing
from typing import Iterable

if typing.TYPE_CHECKING:
    from spectrum.calculations.groups import Field

from spectrum.calculations import numeric
from spectrum.calculations.numeric import gcd, lcm
from spectrum.calculations.semisimple import MixedElements, SemisimpleElements, SpectraElement
from spectrum.calculations.set import FullBoundedSets


__author__ = 'Daniel Lytkin'


def _symplectic_spectrum_odd_c(n: int, field: 'Field') -> Iterable[int]:
    """Spectra of symplectic groups in odd characteristic.
    [1, Corollary 1]
    """
    n //= 2
    q = field.order
    p = field.char

    # (1)
    a1 = SemisimpleElements(q, n)

    # (2)
    a2 = MixedElements(q, n,
                       lambda k: (p ** (k - 1) + 1) // 2,
                       lambda k: p ** k)

    # (3)
    k = numeric.get_exponent(2 * n - 1, p)
    a3 = [] if k is None else [2 * p * (2 * n - 1)]
    return itertools.chain(a1, a2, a3)


def _symplectic_spectrum_even_c(n: int, field: 'Field') -> Iterable[int]:
    """Spectra of symplectic groups in characteristic 2.
    [2, Corollary 3]
    """
    n //= 2
    q = field.order

    # (1)
    a1 = SemisimpleElements(q, n)

    # (2)
    a2 = (2 * elem for elem in SemisimpleElements(q, n - 1))

    # (3)
    a3 = MixedElements(q, n,
                       lambda k: 2 ** (k - 1) + 1,
                       lambda k: 2 ** (k + 1))

    # (4)
    k = numeric.get_exponent(n - 1, 2)
    a4 = [] if k is None else [(n - 1) * 4]
    return itertools.chain(a1, a2, a3, a4)


def _symplectic_spectrum(n: int, field: 'Field') -> Iterable[int]:
    """Spectra of symplectic groups
    """
    if field.char == 2:
        return _symplectic_spectrum_even_c(n, field)
    else:
        return _symplectic_spectrum_odd_c(n, field)


def _projective_symplectic_spectrum_odd_c(n: int, field: 'Field') -> Iterable[int]:
    """Spectra of projective symplectic groups in characteristic 2.
    [1, Corollary 2]
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


def _projective_symplectic_spectrum(n: int, field: 'Field') -> Iterable[int]:
    """Spectra of projective symplectic group. Note that
    PSp(n, 2^k) = Sp(n, 2^k)
    """
    if field.char == 2:
        return _symplectic_spectrum_even_c(n, field)
    else:
        return _projective_symplectic_spectrum_odd_c(n, field)


def _omega_spectrum_odd_c(n: int, field: 'Field') -> Iterable[int]:
    """Spectra of groups \Omega_{2n+1}(q) for odd q.
    [1, Corollary 6]
    """
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
        if n1 < 1:
            break
        t = (q ** n1 - 1) // 2
        a3.extend([t * p ** k, (t + 1) * p ** k])
        k += 1

    # (4)
    a4 = MixedElements(q, n,
                       lambda k: (p ** (k - 1) + 1) // 2,
                       lambda k: p ** k, min_length=2)

    # (5)
    k = numeric.get_exponent(2 * n - 1, p)
    a5 = [] if k is None else [p * (2 * n - 1)]
    return itertools.chain(a1, a2, a3, a4, a5)


def _omega_spectrum(n: int, field: 'Field') -> Iterable[int]:
    """Spectra of Omega_{2n+1}(q)
    """
    if field.char == 2:
        return _symplectic_spectrum_even_c(n - 1, field)
    else:
        if n == 5:
            return _projective_symplectic_spectrum_odd_c(4, field)
        return _omega_spectrum_odd_c(n, field)


def _omega_pm_spectrum_odd_c(n: int, field: 'Field', sign: int) -> Iterable[int]:
    """Spectra of Omega^e_{2n}(q) for odd q.
    [1, Corollary 8]
    """
    n //= 2
    q = field.order
    p = field.char

    def nk(k):
        return (p ** (k - 1) + 3) // 2

    # (1)
    a1 = [(q ** n - sign) // 2]

    # (2)
    a2 = SemisimpleElements(q, n, min_length=2, parity=sign)

    # (3)
    a3 = []
    k = 1
    while True:
        n_k = nk(k)
        if n_k >= n:
            break
        for delta in [1, -1]:
            dk = gcd(4, q ** n_k - sign * delta) // 2
            a3.append(
                p ** k *
                lcm(
                    dk,
                    (q**(n - n_k) - delta) // dk
                )
            )
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


def _omega_pm_spectrum_even_c(n: int, field: 'Field', sign: int) -> Iterable[int]:
    """Spectra for groups \Omega^{\pm}(2^k).
    [1, Corollary 4]
    """
    n //= 2
    q = field.order

    # (1)
    a1 = SemisimpleElements(q, n, parity=sign)

    # (2)
    a2 = MixedElements(q, n,
                       lambda k: 2 ** (k - 1) + 2,
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
        if len(ni) % 2 != signMod:
            continue
        a5.append(4 * SpectraElement(q=q, partition=[1] + ni,
                                     signs=[-1] + [1] * len(ni)))

    # (6)
    a6 = (elem.lcm(SpectraElement(4, q, [1], [1])) for elem in SemisimpleElements(q, n - 3, parity=-sign))

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


def _projective_omega_pm_spectrum(sign: int):
    """Spectra of Omega^e_{2n}(q) for odd q.
    [1, Corollary 9]
    """
    e = sign

    def spectrum(n: int, field: 'Field') -> Iterable[int]:
        n //= 2
        q = field.order
        p = field.char
        # if gcd(4, q^n-e) != 4, then POmega = Omega
        b = (q % 4 == 3 and n % 2 == 1) if e == -1 else (q % 4 == 1)  # true iff gcd(4, q^n-e)=4
        if not b:
            return _omega_pm_spectrum(e)(n * 2, field)

        nk = lambda k: (p ** (k - 1) + 3) // 2

        # (1)
        a1 = [(q ** n - sign) // 4]

        # (2)
        a2 = []
        for n1 in range(1, n):
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
            if n_k >= n:
                break
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


def _omega_pm_spectrum(sign: int):
    e = sign

    def spectrum(n: int, field: 'Field') -> Iterable[int]:
        if field.char == 2:
            return _omega_pm_spectrum_even_c(n, field, e)
        else:
            return _omega_pm_spectrum_odd_c(n, field, e)

    return spectrum


def _special_orthogonal_odd_c_spectrum(n: int, field: 'Field') -> Iterable[int]:
    """Spectra of groups SO_{2n+1}(q) for odd q.
    [1, Corollary 5]
    """
    n = (n - 1) // 2
    q = field.order
    p = field.char

    # (1)
    a1 = SemisimpleElements(q, n)

    # (2)
    a2 = MixedElements(q, n,
                       lambda k: (p ** (k - 1) + 1) // 2,
                       lambda k: p ** k)

    # (3)
    k = numeric.get_exponent(2 * n - 1, p)
    a3 = [] if k is None else [p * (2 * n - 1)]
    return itertools.chain(a1, a2, a3)


def _special_orthogonal_pm_spectrum(sign: int):
    """Spectra SO^e_{2n}(q) for odd q.
    [1, Corollary 7]
    """
    e = sign

    def spectrum(n: int, field: 'Field') -> Iterable[int]:
        n //= 2
        q = field.order
        p = field.char

        # (1)
        a1 = SemisimpleElements(q, n, parity=e)

        # (2)
        a2 = MixedElements(q, n,
                           lambda k: (p ** (k - 1) + 3) // 2,
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
def _projective_general_linear_spectrum(sign: int):
    """Spectra of PGL and PGU groups.
    [2, Corollary 2]
    """
    e = sign

    def spectrum(n: int, field: 'Field') -> Iterable[int]:
        q = field.order
        p = field.char

        # (1)
        eps = 1 if n % 2 == 0 else e
        a1 = [(q ** n - eps) // (q - e)]

        # (2)
        a2 = SemisimpleElements(q, n, min_length=2, sign=e)

        # (3)
        a3 = MixedElements(q, n,
                           lambda k: p ** (k - 1) + 1,
                           lambda k: p ** k, sign=e)

        # (4)
        k = numeric.get_exponent(n - 1, p)
        a4 = [] if k is None else [p * (n - 1)]
        return itertools.chain(a1, a2, a3, a4)

    return spectrum


def _special_linear_spectrum(sign: int):
    """Spectra of SL and SU groups.
        [2, Corollary 1]
    """
    e = sign

    def spectrum(n: int, field: 'Field') -> Iterable[int]:
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
            if n1 < 1:
                break
            eps = 1 if n1 % 2 == 0 else e
            a3.append(p ** k * (q ** n1 - eps) / gcd(d, n1))
            k += 1

        # (4)
        a4 = MixedElements(q, n,
                           lambda k: p ** (k - 1) + 1,
                           lambda k: p ** k, min_length=2, sign=e)

        # (5)
        k = numeric.get_exponent(n - 1, p)
        a5 = [] if k is None else [p * (n - 1) * d]

        # (6)
        a6 = [p * gcd(2, q - 1) * (q + e)] if n == 4 else []
        return itertools.chain(a1, a2, a3, a4, a5, a6)

    return spectrum


def _projective_special_linear_spectrum(sign: int):
    """Spectra of PSL and PSU groups.
        [2, Corollary 3]
    """
    e = sign

    def spectrum(n: int, field: 'Field') -> Iterable[int]:
        q = field.order
        p = field.char
        d = gcd(n, q - e)

        # (1)
        eps = 1 if n % 2 == 0 else e
        a1 = [(q ** n - eps) // ((q - e) * d)]

        # (2)
        a2 = []
        eps = lambda s: 1 if s % 2 == 0 else e
        for n1 in range(1, (n + 2) // 2):
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
            if n1 < 1:
                break
            eps = 1 if n1 % 2 == 0 else e
            a4.append(p ** k * (q ** n1 - eps) / d)
            k += 1

        # (5)
        a5 = MixedElements(q, n,
                           lambda k: p ** (k - 1) + 1,
                           lambda k: p ** k, min_length=2, sign=e)

        # (6)
        k = numeric.get_exponent(n - 1, p)
        a6 = [] if k is None else [p * (n - 1)]
        return itertools.chain(a1, a2, a3, a4, a5, a6)

    return spectrum


classical_spectra = {
    'Sp': _symplectic_spectrum,
    'PSp': _projective_symplectic_spectrum,
    'Omega': _omega_spectrum,
    'Omega+': _omega_pm_spectrum(1),
    'Omega-': _omega_pm_spectrum(-1),
    'POmega+': _projective_omega_pm_spectrum(1),
    'POmega-': _projective_omega_pm_spectrum(-1),
    'SO': _special_orthogonal_odd_c_spectrum,
    'SO+': _special_orthogonal_pm_spectrum(1),
    'SO-': _special_orthogonal_pm_spectrum(-1),
    'PGL': _projective_general_linear_spectrum(1),
    'PGU': _projective_general_linear_spectrum(-1),
    'SL': _special_linear_spectrum(1),
    'SU': _special_linear_spectrum(-1),
    'PSL': _projective_special_linear_spectrum(1),
    'PSU': _projective_special_linear_spectrum(-1),
}
