from numeric import *
from partition import Partitions
from spectrum.calculations.orders import sporadic_orders, classical_orders, exceptional_orders
from spectrum.calculations.spectra import sporadic_spectra, classical_spectra, exceptional_spectra
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
            self._order = prod(xrange(3, self._degree + 1))
        return self._order

    def __str__(self):
        return "Alt({})".format(self._degree)


class ClassicalGroup(Group):
    """Usage:
    ClassicalGroup("PSp", 14, Field(2, 5))
    ClassicalGroup("PSp", 14, 32)
    ClassicalGroup("PSp", 14, 2, 5)
    """
    _groups = (
        'PGL', 'PGU', 'Omega', 'Omega+', 'POmega+', 'Omega-', 'POmega-', 'SL',
        'PSL', 'SO', 'SO+', 'SO-', 'SU', 'PSU', 'Sp', 'PSp')

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
        return ClassicalGroup._groups

    @property
    def field(self):
        """Returns field of this group
        """
        return self._field

    def apex(self):
        if self._apex is None:
            func = classical_spectra.get(self._name, lambda *arg: [])
            self._apex = sort_and_filter(func(self._dim, self._field))
        return self._apex

    def order(self):
        if self._order is None:
            func = classical_orders.get(self._name, lambda *arg: Integer())
            self._order = func(self._dim, self._field)
        return self._order


class ExceptionalGroup(Group):
    _groups = (
        "E6", "2E6", "E7", "E8", "F4", "2F4", "G2", "2G2", "2B2", "3D4",)

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
        return ExceptionalGroup._groups

    @property
    def field(self):
        """Returns field of this group
        """
        return self._field

    def apex(self):
        if self._apex is None:
            func = exceptional_spectra.get(self._name, lambda *arg: [])
            self._apex = sort_and_filter(func(self._field))
        return self._apex

    def order(self):
        if self._order is None:
            func = exceptional_orders.get(self._name, lambda *arg: Integer())
            self._order = func(self._field)
        return self._order

