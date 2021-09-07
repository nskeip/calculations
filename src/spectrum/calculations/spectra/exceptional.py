"""
Bibliography:
[1] Buturlakin A. A., “Spectra of Groups E_8(Q)”, Algebra and Logic, Vol. 57, No. 1, (2018).

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

import enum
import itertools
import typing
from math import gcd, log, ceil
from typing import Iterable

if typing.TYPE_CHECKING:
    from spectrum.calculations.groups import Field


def _g2_spectrum(field: 'Field') -> Iterable[int]:
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


def _2f4_spectrum(field: 'Field') -> Iterable[int]:
    q = field.order
    sq = 2 ** ((field.pow + 1) // 2)
    ssq = 2 ** ((3 * field.pow + 1) // 2)
    return [12, 16, 4 * (q - 1), 2 * (q + 1), 4 * (q - sq + 1),
            4 * (q + sq + 1), q ** 2 - 1, q ** 2 + 1, q ** 2 - q + 1,
            (q - 1) * (q - sq + 1),
            (q - 1) * (q + sq + 1),
            q ** 2 - ssq + q - sq + 1,
            q ** 2 + ssq + q + sq + 1]


def _2b2_spectrum(field: 'Field') -> Iterable[int]:
    q = field.order
    sq = 2 ** ((field.pow + 1) // 2)
    return [4, q - sq + 1, q + sq + 1, q - 1]


def _2g2_spectrum(field: 'Field') -> Iterable[int]:
    q = field.order
    sq = 3 ** ((field.pow + 1) // 2)
    return [9, 6, (q + 1) // 2, q - 1, q - sq + 1, q + sq + 1]


def _e6_spectrum(sign: int):
    e = sign

    def spectrum(field: 'Field') -> Iterable[int]:
        q = field.order
        p = field.char
        d = gcd(3, q - e)
        # (1)
        a1 = [(q ** 6 - 1) // d, (q ** 6 + e * q ** 3 + 1) // d, (q * q + e * q + 1) * (q ** 4 - q * q + 1) // d,
              (q - e) * (q * q + 1) * (q ** 3 + e) // d, (q * q - 1) * (q ** 4 + 1) // d, (q + e) * (q ** 5 - e) // d,
              q ** 5 - e]
        # (2)
        a2 = [
            p * x for x in
            [(q ** 6 - 1) // (d * (q - e)), (q ** 5 - e) // d, q ** 4 - 1, (q ** 3 - e) * (q + e),
             (q - e) * (q ** 3 + e) // d]
        ]
        # (3)
        pA2 = 4 if p == 2 else p
        a3 = [
            pA2 * x for x in
            [(q ** 3 - e) * (q + e) // d, (q ** 4 + q * q + 1) // d, (q ** 4 - 1) // d]
        ]
        # (4)
        pA3 = p * p if p in (2, 3) else p
        a4 = [
            pA3 * x for x in
            [(q * q + 1) * (q - e) // d, q ** q - 1]
        ]
        # (5)
        pD4 = 8 if p == 2 else p * p if p in (3, 5) else p
        a5 = [
            pD4 * x for x in
            [q - e, (q * q - 1) // d, (q * q + e * q + 1) // d]
        ]
        # (6)
        pD5 = 8 if p == 2 else p * p if p in (3, 5, 7) else p
        a6 = [pD5 * (q - e) // d]
        # (7)
        pE6 = 16 if p == 2 else 27 if p == 3 else p * p if p in (5, 7, 11) else p
        a7 = [pE6]
        return itertools.chain(a1, a2, a3, a4, a5, a6, a7)

    return spectrum


class RootSystemType(enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'


class RootSystem:
    root_system_type: RootSystemType

    def __init__(self, root_system_type: typing.Union[str, RootSystemType], n: int):
        self.root_system_type = RootSystemType(root_system_type)
        self.n = n

    def mh(self):
        """
        Maximal height of the root.
        [3, table 1]
        """
        if self.root_system_type == RootSystemType.A:
            return self.n
        elif self.root_system_type in (RootSystemType.B, RootSystemType.C):
            return 2 * self.n - 1
        elif self.root_system_type == RootSystemType.D:
            return 2 * self.n - 3
        elif (self.root_system_type == RootSystemType.E and self.n == 6) or \
                (self.root_system_type == RootSystemType.F and self.n == 4):
            return 11
        elif self.root_system_type == RootSystemType.E and self.n == 7:
            return 17
        elif self.root_system_type == RootSystemType.E and self.n == 8:
            return 29
        elif self.root_system_type == RootSystemType.G and self.n == 2:
            return 5
        else:
            raise ValueError(f'Max height is not defined for {self.root_system_type.value}_{self.n}')

    def p(self, p: int):
        """
        Least p power that is greater than n.
        """
        return p ** ceil(log(self.mh() + 1, p))


def _e8_spectrum(field: 'Field') -> Iterable[int]:
    """
    [1, main theorem]
    """
    q = field.order
    p = field.char

    return [  # (1)
        (q + 1) * (q**2 + q + 1) * (q**5 - 1),
        (q - 1) * (q**2 - q + 1) * (q**5 + 1),

        (q + 1) * (q ** 2 + 1) * (q ** 5 - 1),
        (q - 1) * (q ** 2 + 1) * (q ** 5 + 1),

        (q + 1) * (q ** 7 - 1),
        (q - 1) * (q ** 7 + 1),

        q ** 8 - 1,

        (q + 1) * (q ** 3 - 1) * (q ** 4 + 1),
        (q - 1) * (q ** 3 + 1) * (q ** 4 + 1),

        (q ** 2 + 1) * (q ** 6 - 1),
        (q ** 2 - 1) * (q ** 6 + 1),

        (q ** 2 - 1) * (q ** 2 + q + 1) * (q ** 4 - q ** 2 + 1),
        (q ** 2 - 1) * (q ** 2 - q + 1) * (q ** 4 - q ** 2 + 1),

        (q ** 2 - 1) * (q ** 6 - q ** 3 + 1),
        (q ** 2 - 1) * (q ** 6 + q ** 3 + 1),

        (q ** 2 + q + 1) * (q ** 6 + q ** 3 + 1) // gcd(3, q - 1),
        (q ** 2 - q + 1) * (q ** 6 - q ** 3 + 1) // gcd(3, q + 1),

        q**8 + q**7 - q**5 - q**4 - q**3 + q + 1,
        q**8 - q**7 + q**5 - q**4 + q**3 - q + 1,

        q**8 - q**4 + 1,
        q**8 - q**6 + q**4 - q**2 + 1,
    ] + [  # (2)
        p * x for x in [
            (q ** 2 - q + 1) * (q ** 5 + 1),
            (q ** 2 + q + 1) * (q ** 5 - 1),

            (q + 1) * (q ** 6 - q ** 3 + 1),
            (q - 1) * (q ** 6 + q ** 3 + 1),

            q ** 7 + 1,
            q ** 7 - 1,

            (q ** 3 - 1) * (q ** 4 - q ** 2 - 1),
            (q ** 3 + 1) * (q ** 4 - q ** 2 + 1),

            (q ** 8 - 1) // ((q - 1) * gcd(2, q - 1)),
            (q ** 8 - 1) // ((q + 1) * gcd(2, q - 1)),

            q ** 6 + 1,
        ]
    ] + [  # (3)
        RootSystem('A', 2).p(p) * x for x in [
            q ** 6 - 1,

            q ** 6 + q ** 3 + 1,
            q ** 6 - q ** 3 + 1,

            (q ** 2 + q + 1) * (q ** 4 - q ** 2 + 1),
            (q ** 2 - q + 1) * (q ** 4 - q ** 2 + 1),

            (q ** 2 - q + 1) * (q ** 4 - 1),
            (q ** 2 + q + 1) * (q ** 4 - 1),

            (q ** 2 - 1) * (q ** 4 + 1),

            (q + 1) * (q ** 5 - 1),
            (q - 1) * (q ** 5 + 1),
        ]
    ] + [  # (4)
        RootSystem('A', 3).p(p) * x for x in [
            (q ** 5) - 1,
            (q ** 5) + 1,

            (q ** 4 + 1) * (q - 1),
            (q ** 4 + 1) * (q + 1),

            (q ** 3 - 1) * (q ** 2 + 1),
            (q ** 3 + 1) * (q ** 2 + 1),
        ]
    ] + [  # (5)
        RootSystem('A', 4).p(p) * x for x in [
            (q ** 5 - 1) // (q - 1),
            (q ** 5 + 1) // (q + 1),

            q ** 4 - 1,
        ]
    ] + [  # (6)
        RootSystem('A', 5).p(p) * x for x in [
            (q ** 3 - 1) * (q + 1),
            (q ** 3 + 1) * (q - 1),

            q ** 4 + 1,

            (q ** 4 - 1) // gcd(2, q - 1),

            q ** 4 - q ** 2 + 1,
        ]
    ] + [  # (7)
        RootSystem('D', 5).p(p) * x for x in [
            (q ** 2 + 1) * (q - 1),
            (q ** 2 + 1) * (q + 1),

            q ** 3 - 1,
            q ** 3 + 1,
        ]
    ] + [  # (8)
        RootSystem('D', 6).p(p) * (q ** 2 + 1)
    ] + [  # (9)
        RootSystem('E', 6).p(p) * x for x in [
            (q ** 2 - q + 1),
            (q ** 2 + q + 1),

            q ** 2 - 1,
        ]
    ] + [  # (10)
        RootSystem('E', 7).p(p) * x for x in [
            q - 1,
            q + 1,
        ]
    ] + [  # (11)
        RootSystem('E', 8).p(p)
    ]


exceptional_spectra = {
    '2F4': _2f4_spectrum,
    'G2': _g2_spectrum,
    '2G2': _2g2_spectrum,
    '2B2': _2b2_spectrum,
    'E6': _e6_spectrum(1),
    '2E6': _e6_spectrum(-1),
    'E8': _e8_spectrum,
}
