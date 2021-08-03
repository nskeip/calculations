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
from spectrum.calculations.numeric import Integer
from spectrum.calculations.set import MaximalBoundedSets, FullBoundedSets, BoundedSets
from spectrum.tools.tools import ObjectCache

__author__ = 'Daniel Lytkin'

_CACHE = True


class SpectraElement(long):
    """Special long extension for spectra elements. It contains information on
    how it was calculated. If 'verbose' is False, creates long, without any
    additional info
    """

    def __new__(cls, quotient=1, q=0, partition=None, signs=None,
                verbose=True):
        if partition is None:
            partition = []
        if signs is None:
            signs = []
        class_ = SpectraElement if verbose else long
        return long.__new__(class_, quotient * reduce(numeric.lcm,
                                                      (q ** ni + ei for (ni, ei) in zip(partition, signs)), 1))

    def __init__(self, quotient=1, q=0, partition=None, signs=None,
                 verbose=True):
        """Creates element = quotient * [q ^ n_1 + e_1, ...] for n_i in
        'partition', e_i in 'signs'
        """
        if partition is None:
            partition = []
        if signs is None:
            signs = []
        self._quotient = Integer(quotient)
        self._q = q
        self._partition = partition
        self._signs = signs
        super(SpectraElement, self).__init__(self)

    @property
    def quotient(self):
        return self._quotient

    @property
    def partition(self):
        return self._partition

    @property
    def signs(self):
        return self._signs

    def str_verbose(self):
        quotient = self._quotient.str_factorized() if (
            self._quotient != 1) else ""
        sign = lambda e: "+" if e > 0 else "-"
        power = lambda k: "^" + str(k) if k > 1 else ""
        element = lambda ni, ei: "{}{} {} 1".format(self._q, power(ni),
                                                    sign(ei))
        elements = ", ".join(
            element(ni, ei) for (ni, ei) in sorted(
                zip(self._partition, self._signs)))
        if len(self._partition) == 1:
            brackets = "({})" if self._quotient != 1 else "{}"
        else:
            brackets = "[{}]"
        lcm_str = brackets.format(elements) if elements else ""
        return " * ".join(filter(bool, (quotient, lcm_str)))

    def str_latex(self):
        quotient = self._quotient.str_factorized() if (
            self._quotient != 1) else ""
        sign = lambda e: "+" if e > 0 else "-"

        def power(k):
            if k == 1:
                return ""
            template = "^{}" if k < 10 else "^{{{}}}"
            return template.format(k)

        element = lambda ni, ei: "{}{} {} 1".format(self._q, power(ni),
                                                    sign(ei))
        elements = ", ".join(
            element(ni, ei) for (ni, ei) in sorted(
                zip(self._partition, self._signs), reverse=True))
        if len(self._partition) == 1:
            brackets = "({})" if self._quotient != 1 else "{}"
        else:
            brackets = "[{}]"
        lcm_str = brackets.format(elements) if elements else ""
        return " ".join(filter(bool, (quotient, lcm_str)))

    def lcm(self, other):
        """Returns lcm of this and other. 'q' must be the same. Quotients are
        multiplied.
        """
        elem = long.__new__(SpectraElement, numeric.lcm(self, other))
        quotient = self._quotient * other._quotient
        elem.__init__(quotient=quotient, q=self._q,
                      partition=list(self._partition) + list(other._partition),
                      signs=list(self._signs) + list(other._signs))
        return elem

    def __mul__(self, other):
        """Multiplies quotient by integer
        """
        elem = long.__new__(SpectraElement, long(self) * other)
        elem.__init__(quotient=self._quotient * other, q=self._q,
                      partition=self._partition, signs=self._signs)
        return elem

    def __rmul__(self, other):
        return self * other


class SemisimpleElements(object):
    """Generates elements of form LCM(q^{n_1} \pm 1, ..., q^{n_k} \pm 1) for
    all partitions n_1 + ... + n_k = n.
    If `min_length' is set to t, then k >= t. Only min_length=1, 2 or 3 are supported.
    If `parity' is set to 1 or -1, generates elements with even or odd number
    of pluses respectively.
    If `sign' is set to 1 or -1, generates elements of form
    LCM(q^{n_1}-sign^{n_1}, ..., q^{n_k}-sign^{n_k})
    `sign' or `parity' arguments must be only used separately.
    """

    if _CACHE:
        __metaclass__ = ObjectCache

    def __init__(self, q, n, min_length=1, parity=0, sign=0, verbose=True):
        self._q = q
        self._n = n
        self._min_length = min_length
        self._parity = parity
        self._sign = sign
        self._verbose = verbose
        self._stored = None

    def _with_sign_generator(self):
        """Generates semisimple element with specified sign
        (for Linear and Unitary groups)
        """
        q = self._q
        n = self._n
        # [q^n_1 - 1, ..., q^n_k - 1] if sign = 1, else
        # [q^n_1 - sign^n_1, ..., q^n_k - sign^n_k]
        f = lambda nk: (-1 if (self._sign == 1 or nk % 2 == 0) else 1)
        #        f = ((lambda ni: -1) if self._sign == 1 else
        #             lambda ni: (-1 if nk % 2 == 0 else 1 for nk in ni))
        for ni in BoundedSets(n):
            if len(ni) + n - sum(ni) < self._min_length:
                continue
            yield SpectraElement(q=q, partition=ni, signs=map(f, ni),
                                 verbose=self._verbose)

    def _with_parity_generator(self):
        """Generates semisimple elements with even or odd number of pluses"""
        q = self._q
        n = self._n
        plusesMod = 0 if self._parity == 1 else 1
        for pluses in range(plusesMod, n + 1):
            plusPartitions = FullBoundedSets(pluses)
            if pluses > 0:
                plusPartitions = itertools.chain(plusPartitions,
                                                 (partition + [1] for partition in FullBoundedSets(pluses - 1)))
            for plusPartition in plusPartitions:
                minuses = n - pluses
                if not len(plusPartition) % 2 == plusesMod:
                    continue
                plusPart = plusPartition if pluses else []
                for minusPartition in MaximalBoundedSets(minuses):
                    rest = n - sum(plusPartition) - sum(minusPartition)
                    if len(plusPartition) + len(
                            minusPartition) + rest < self._min_length:
                        continue
                    minusPart = minusPartition if minuses else []
                    yield SpectraElement(q=q,
                                         partition=plusPart + minusPart,
                                         signs=[1] * len(plusPart) + [-1] * len(minusPart),
                                         verbose=self._verbose)

    def _general_generator(self):
        """Generates all semisimple elements"""
        q = self._q
        n = self._n
        for left in range((n + 2) // 2):
            right = n - left
            leftPartitions = MaximalBoundedSets(left)
            for lPartition in leftPartitions:
                lPart = lPartition if left else []
                rightPartitions = MaximalBoundedSets(right)
                for rPartition in rightPartitions:
                    rest = n - sum(lPartition) - sum(rPartition)
                    length = len(lPartition) + len(rPartition)
                    if length + rest < self._min_length:
                        continue
                    rPart = rPartition if right else []
                    yield self._store_and_return(
                        SpectraElement(q=q, partition=lPart + rPart, signs=[-1] * len(lPart) + [1] * len(rPart),
                                       verbose=self._verbose))
                    yield self._store_and_return(
                        SpectraElement(q=q, partition=lPart + rPart,
                                       signs=[1] * len(lPart) +
                                             [-1] * len(rPart),
                                       verbose=self._verbose))

    def __iter__(self):
        if self._stored is not None:
            return iter(self._stored)
        if self._sign:
            return self._with_sign_generator()
        if self._parity:
            return self._with_parity_generator()
        return self._general_generator()

    def _store_and_return(self, element):
        if self._stored is None:
            self._stored = []
        self._stored.append(element)
        return element


class MixedElements(object):
    """Generates elements of form g(k) * LCM(q^{n_1} \pm 1, ..., q^{n_s} \pm 1)
    for all k and partitions f(k) + n_1 + ... + n_s = n, where k, s > 0.
    """

    def __init__(self, q, n, f, g, min_length=1, parity=0, sign=0):
        self._q = q
        self._n = n
        self._f = f
        self._g = g
        self._min_length = min_length
        self._parity = parity
        self._sign = sign


    def __iter__(self):
        k = 1
        while True:
            toPart = self._n - self._f(k)
            if toPart <= 0: break
            for elem in SemisimpleElements(self._q, toPart,
                                           min_length=self._min_length, parity=self._parity,
                                           sign=self._sign):
                yield elem * self._g(k)
            k += 1

