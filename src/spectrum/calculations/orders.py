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
from spectrum.calculations.numeric import Integer, gcd, prod

__author__ = 'Daniel Lytkin'

sporadic_orders = {
    "M11": (Integer((2, 4), (3, 2), 5, 11)),
    "M12": (Integer((2, 6), (3, 3), 5, 11)),
    "M22": (Integer((2, 7), (3, 2), 5, 7, 11)),
    "M23": (Integer((2, 7), (3, 2), 5, 7, 11, 23)),
    "M24": (Integer((2, 10), (3, 3), 5, 7, 11, 23)),
    "J1": (Integer((2, 3), 3, 5, 7, 11, 19)),
    "J2": (Integer((2, 7), (3, 3), (5, 2), 7)),
    "J3": (Integer((2, 7), (3, 5), 5, 17, 19)),
    "J4": (Integer((2, 21), (3, 3), 5, 7, (11, 3), 23, 29, 31, 37, 43)),
    "Co1": (Integer((2, 21), (3, 9), (5, 4), (7, 2), 11, 13, 23)),
    "Co2": (Integer((2, 18), (3, 6), (5, 3), 7, 11, 23)),
    "Co3": (Integer((2, 10), (3, 7), (5, 3), 7, 11, 23)),
    "Fi22": (Integer((2, 17), (3, 9), (5, 2), 7, 11, 13)),
    "Fi23": (Integer((2, 18), (3, 13), (5, 2), 7, 11, 13, 17, 23)),
    "Fi24'": (Integer((2, 21), (3, 16), (5, 2), (7, 3), 11, 13, 17, 23, 29)),
    "HS": (Integer((2, 9), (3, 2), (5, 3), 7, 11)),
    "McL": (Integer((2, 7), (3, 6), (5, 3), 7, 11)),
    "He": (Integer((2, 10), (3, 3), (5, 2), (7, 3), 17)),
    "Ru": (Integer((2, 14), (3, 3), (5, 3), 7, 13, 29)),
    "Suz": (Integer((2, 13), (3, 7), (5, 2), 7, 11, 13)),
    "O'N": (Integer((2, 9), (3, 4), 5, (7, 3), 11, 19, 31)),
    "HN": (Integer((2, 14), (3, 6), (5, 6), 7, 11, 19)),
    "Ly": (Integer((2, 8), (3, 7), (5, 6), 7, 11, 31, 37, 67)),
    "Th": (Integer((2, 15), (3, 10), (5, 3), (7, 2), 13, 19, 31)),
    "B": (
        Integer((2, 41), (3, 13), (5, 6), (7, 2), 11, 13, 17, 19, 23, 31, 47)),
    "M": (
        Integer((2, 46), (3, 20), (5, 9), (7, 6), (11, 2), (13, 3), 17, 19, 23,
            29,
            31, 41, 47, 59, 71)),
    "2F4(2)'": (Integer((2, 11), (3, 3), (5, 2), 13))
}


def _symplectic_order(n, field):
    n //= 2
    q = field.order
    return (Integer({field.char: field.pow * n * n}) *
            prod((Integer(q ** i - 1) *
                  Integer(q ** i + 1) for i in range(1, n + 1))))


def _projective_symplectic_order(n, field):
    # equals to Sp(n, q) if q even
    #d = 1 if field.char == 2 else 2
    o = _symplectic_order(n, field)
    if field.char != 2:
        o.div_by_prime(2)
    return o


def _omega_pm_order(sign):
    e = sign

    def order(n, field):
        q = field.order
        n //= 2
        o = (Integer({field.char: field.pow * n * (n - 1)}) *
             Integer(q ** n - e) *
             prod((Integer(q ** i - 1) *
                   Integer(q ** i + 1) for i in range(1, n))))
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
        part = prod((Integer(q ** k - 1) *
                     Integer(q ** k + 1) for k in range(1, n)))
        if not e:
            return (part * Integer({field.char: field.pow * n * n}) *
                    Integer(q ** n - 1) * Integer(q ** n + 1))
        if field.char == 2:
            part *= 2
        return (part * Integer({field.char: field.pow * n * (n - 1)}) *
                Integer(q ** n - e))

    return order


def _projective_general_linear_order(n, field):
    q = field.order
    return (Integer({field.char: field.pow * (n * (n - 1) / 2)}) *
            prod((Integer(q ** i - 1) for i in range(2, n + 1))))


def _projective_general_unitary_order(n, field):
    q = field.order
    return (Integer({field.char: field.pow * (n * (n - 1) / 2)}) *
            prod((Integer(q ** i - 1) *
                  Integer(q ** i + 1) for i in range(1, n // 2 + 1))) *
            prod((Integer(q ** (2 * i + 1) + 1)) for i in range(1,
                (n + 1) // 2)))


def _projective_special_linear_order(n, field):
    q = field.order
    return (Integer({field.char: field.pow * (n * (n - 1) / 2)}) *
            prod((Integer(q ** i - 1) for i in range(3, n + 1))) *
            Integer(q + 1) * Integer((q - 1) // gcd(n, q - 1)))


def _projective_special_unitary_order(n, field):
    q = field.order
    return (Integer({field.char: field.pow * (n * (n - 1) / 2)}) *
            prod((Integer(q ** i - 1) *
                  Integer(q ** i + 1) for i in range(2, n // 2 + 1))) *
            prod((Integer(q ** (2 * i + 1) + 1)) for i in range(1,
                (n + 1) // 2)) *
            Integer(q - 1) * Integer((q + 1) // gcd(n, q + 1)))


classical_orders = {
    "Sp": _symplectic_order,
    "PSp": _projective_symplectic_order,
    "Omega": _projective_symplectic_order,
    "Omega+": _omega_pm_order(1),
    "Omega-": _omega_pm_order(-1),
    "POmega+": _projective_omega_pm_order(1),
    "POmega-": _projective_omega_pm_order(-1),
    "SO": _special_orthogonal_order(0),
    "SO+": _special_orthogonal_order(1),
    "SO-": _special_orthogonal_order(-1),
    "PGL": _projective_general_linear_order,
    "PGU": _projective_general_unitary_order,
    "SL": _projective_general_linear_order,
    "SU": _projective_general_unitary_order,
    "PSL": _projective_special_linear_order,
    "PSU": _projective_special_unitary_order,
    }


def _order_product(field, pow, pluses, minuses):
    q = field.order
    return (Integer({field.char: field.pow * pow}) *
            prod((Integer(q ** i + 1) for i in pluses)) *
            prod((Integer(q ** i - 1) for i in minuses)))


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


exceptional_orders = {
    "E6": _e6_order,
    "2E6": _2e6_order,
    "E7": _e7_order,
    "E8": _e8_order,
    "F4": _f4_order,
    "2F4": _2f4_order,
    "G2": _g2_order,
    "2G2": _2g2_order,
    "2B2": _2b2_order,
    "3D4": _3d4_order,
    }