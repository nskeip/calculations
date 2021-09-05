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

import itertools
import typing
from math import gcd
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


def _e8_spectrum(field: 'Field') -> Iterable[int]:
    """
    [3, main theorem]
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

        (q ** 2 + q + 1) * (q ** 6 + q ** 3 + 1) / gcd(3, q - 1),
        (q ** 2 - q + 1) * (q ** 6 - q ** 3 + 1) / gcd(3, q + 1),

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

            (q ** 8 - 1) / ((q - 1) * gcd(2, q - 1)),
            (q ** 8 - 1) / ((q + 1) * gcd(2, q - 1)),

            q ** 6 + 1,
        ]
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
