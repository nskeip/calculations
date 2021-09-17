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
from functools import reduce

from spectrum.calculations import orders, spectra, numeric
from spectrum.calculations.numeric import Constraints, Integer
from spectrum.tools.tools import doc_inherit, ObjectCache
from .partition import Partitions

__author__ = 'Daniel Lytkin'

_CACHE = True  # whether group caching is enabled

# whether to surround group name with \operatorname{} in str_latex()
#LATEX_OPERATORNAME = True


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
            self._base = numeric.first_divisor(arg[0])
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
    def order(self):
        return self._order

    @property
    def char(self):
        return self._base

    @property
    def pow(self):
        return self._pow

    def __str__(self):
        if self._pow == 1:
            return "F({})".format(self._base)
        return "F({}^{})".format(self._base, self._pow)


class Group:
    """Abstract class for finite groups.
    """

    def apex(self):
        """Returns apex of the group, which is the set of its element orders
        with all divisors filtered out.

        """
        raise NotImplementedError()

    def order(self):
        """Returns group order."""
        raise NotImplementedError()

    def _hs_str(self):
        """Returns haskell representation
        """
        raise NotImplementedError()


class SporadicGroup(Group):
    _groups = ('M11', 'M12', 'J1', 'M22', 'J2', 'M23', "2F4(2)'", 'HS', 'J3',
               'M24', 'McL', 'He', 'Ru', 'Suz', "O'N", 'Co3', 'Co2', 'Fi22',
               'HN', 'Ly', 'Th', 'Fi23', 'Co1', 'J4', "Fi24'", 'B', 'M')

    _latex = {'Co1': 'Co_1', 'Co3': 'Co_3', 'Co2': 'Co_2', "Fi24'": "Fi_{24}'",
              'M24': 'M_{24}', 'J1': 'J_1', 'M22': 'M_{22}', 'M23': 'M_{23}',
              'M11': 'M_{11}', 'J4': 'J_4', 'M12': 'M_{12}', 'J2': 'J_{2}',
              "2F4(2)'": "{}^2F_4(2)'", 'J3': 'J_3', 'Fi23': 'Fi_{23}',
              'Fi22': 'Fi_{22}'}

    _hs = {"2F4(2)'": "TwoF42'", "O'N": "ON"}

    def __init__(self, name):
        super(SporadicGroup, self).__init__()
        self._name = name

    @doc_inherit
    def apex(self):
        return spectra.sporadic_spectra.get(self._name, [])

    @doc_inherit
    def order(self):
        return orders.sporadic_orders.get(self._name)

    def __str__(self):
        return self._name

    def str_latex(self):
        return SporadicGroup._latex.get(self._name, self._name)

    def _hs_str(self):
        return "Sporadic " + SporadicGroup._hs.get(self._name, self._name)

    @staticmethod
    def all_groups():
        """Returns all sporadic_spectra group names."""
        return SporadicGroup._groups


class AlternatingGroup(Group):
    """AlternatingGroup(n) represents alternating group of degree n
    """
    if _CACHE:
        __metaclass__ = ObjectCache

    def __init__(self, degree):
        super(AlternatingGroup, self).__init__()
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
            partitions = [x for x in Partitions(n) if (len(x) + n) % 2 == 0]
            self._apex = numeric.sort_and_filter(
                [reduce(numeric.lcm, partition) for partition in partitions])
        return self._apex

    @doc_inherit
    def order(self):
        if self._order is None:
            # n!/2
            self._order = numeric.prod(range(3, self._degree + 1))
        return Integer(self._order)

    def __str__(self):
        return "Alt({})".format(self._degree)

    def str_latex(self):
        return str(self)

    def _hs_str(self):
        return "Alternating {{degree={}}}".format(self._degree)


class ClassicalGroup(Group):
    """Usage:
    ClassicalGroup("PSp", 14, Field(2, 5))
    ClassicalGroup("PSp", 14, 32)
    ClassicalGroup("PSp", 14, 2, 5)
    """
    if _CACHE:
        __metaclass__ = ObjectCache

    _groups = (
        'PGL', 'PGU', 'Omega', 'Omega+', 'POmega+', 'Omega-', 'POmega-', 'SL',
        'PSL', 'SO', 'SO+', 'SO-', 'SU', 'PSU', 'Sp', 'PSp')

    _latex = {'Omega+': 'Omega^+', 'Omega-': 'Omega^-',
              'POmega+': 'POmega^+', 'POmega-': 'POmega^-', 'SO+': 'SO^+',
              'SO-': 'SO^-'}

    # constraints for dimension
    _dim_constraints = {
        'Omega': Constraints(min=5, parity=-1),
        'Omega+': Constraints(min=8, parity=1),
        'Omega-': Constraints(min=8, parity=1),
        'POmega+': Constraints(min=8, parity=1),
        'POmega-': Constraints(min=8, parity=1),
        'SO': Constraints(min=5, parity=-1),
        'SO+': Constraints(min=8, parity=1),
        'SO-': Constraints(min=8, parity=1),
        'Sp': Constraints(min=4, parity=1),
        'PSp': Constraints(min=4, parity=1)
    }

    # constraints for field order
    _field_constraints = {'SO': Constraints(min=3,
                                            primality=numeric.PRIME_POWER, parity=-1)}

    def __init__(self, name, dimension, *field):
        super(ClassicalGroup, self).__init__()
        self._name = name
        self._dim = dimension
        self._field = field[0] if isinstance(field[0], Field) else Field(
            *field)
        self._apex = None
        self._order = None

    def __str__(self):
        return "{}({}, {})".format(self._name, self._dim, self._field.order)

    def str_latex(self):
        name = ClassicalGroup._latex.get(self._name, self._name)
        dim = str(self._dim)
        if len(dim) > 1:
            dim = "{" + dim + "}"
        return "{}_{}({})".format(name, dim, self._field.order)

    def _hs_str(self):
        return super(ClassicalGroup, self)._hs_str()

    @staticmethod
    def types():
        return ClassicalGroup._groups

    @property
    def field(self):
        """Returns field of this group
        """
        return self._field

    def apex(self):
        if self._apex is None:
            func = spectra.classical_spectra.get(self._name, lambda *arg: [])
            self._apex = numeric.sort_and_filter(func(self._dim, self._field))
        return self._apex

    def order(self):
        if self._order is None:
            func = orders.classical_orders.get(self._name,
                                               lambda *arg: Integer())
            self._order = func(self._dim, self._field)
        return self._order

    @staticmethod
    def field_constraints(name):
        """Returns constraints on field for specified kind of groups
        """
        return ClassicalGroup._field_constraints.get(name, Constraints(min=2,
                                                                       primality=numeric.PRIME_POWER))

    @staticmethod
    def dim_constraints(name):
        """Returns constraints on dimension for specified kind of groups
        """
        return ClassicalGroup._dim_constraints.get(name, Constraints(min=2))


class ExceptionalGroup(Group):
    if _CACHE:
        __metaclass__ = ObjectCache

    _groups = (
        "E6", "2E6", "E7", "E8", "F4", "2F4", "G2", "2G2", "2B2", "3D4",)

    _latex = {"E6": 'E_6', "2E6": '{}^2E_6', "E7": 'E_7', "E8": 'E_8',
              "F4": 'F_4', "2F4": '{}^2F_4', "G2": 'G_2', "2G2": '{}^2G_2',
              "2B2": '{}^2B_2', "3D4": '{}^3D_4'}

    def __init__(self, name, *field):
        super(ExceptionalGroup, self).__init__()
        self._name = name
        self._field = field[0] if isinstance(field[0], Field) else Field(
            *field)
        self._apex = None
        self._order = None


    def __str__(self):
        return "{}({})".format(self._name, self._field.order)

    def str_latex(self):
        name = ExceptionalGroup._latex.get(self._name, self._name)
        return "{}({})".format(name, self._field.order)

    @staticmethod
    def types():
        return ExceptionalGroup._groups

    @property
    def field(self):
        """Returns field of this group
        """
        return self._field

    def apex(self):
        if self._apex is None:
            func = spectra.exceptional_spectra.get(self._name, lambda *arg: [])
            self._apex = numeric.sort_and_filter(func(self._field))
        return self._apex

    def order(self):
        if self._order is None:
            func = orders.exceptional_orders.get(self._name,
                                                 lambda *arg: Integer())
            self._order = func(self._field)
        return self._order