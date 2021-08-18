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
import math
import operator
from collections import Counter

__author__ = 'Daniel Lytkin'

# Module providing methods to calculate GCD and LCM etc.
from functools import reduce


def gcd(a, b):
    """Calculates greatest common divisor of two numbers.

    Args:
        a, b: Integers

    Returns:
        GCD(a, b)
    """
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Calculates least common multiple of two numbers.

    Args:
        a, b: Integers

    Returns:
        LCM(a, b)
    """
    return a / gcd(a, b) * b


def prime_part(n, b):
    """Calculates b'-part of number n, which is the greatest divisor of n
    coprime to d.

    Args:
        n: Integer that we'll divide by every prime divisor of b
        b: Integer whose prime divisors we remove from n's prime divisors

    Returns:
        Greatest divisor of n which is relatively prime to d.
    """
    while True:
        d = gcd(n, b)
        if d <= 1: break
        n //= d
    return n


def filter_divisors(iterable, reverse=False):
    """Removes all elements that divide any other.

    Returns list generated by given iterable consisting of elements that are
    maximal by divisibility.
    Input argument must be in decreasing order

    Args:
        iterable: Input iterable of integers in decreasing order.
        reverse: If true, returns list in increasing order. Default is false.

    Returns:
        List without divisors.

    """
    ret = []
    if not reverse:
        def append_left(element): ret.insert(0, element)

        add_element = append_left
    else:
        add_element = ret.append
    for element in iterable:
        if not any(x % element == 0 for x in ret):
            add_element(element)

    return ret


def sort_and_filter(sequence, reverse=False):
    """Converts raw sequence of numbers to sorted sequence without divisors.

    Args:
        sequence: Input iterable of sequence.
        reverse: If true, returns list in increasing order. Default is false.

    Returns:
        List without divisors.

    """
    ret = list(sequence)
    ret.sort(reverse=True)
    return filter_divisors(ret, reverse=reverse)


def first_divisor(number):
    """Returns smallest divisor of 'number' greater than 1.

    Args:
        number: Integer

    Returns:
        Smallest (prime) divisor of given number greater than 1.

    """
    if number % 2 == 0: return 2
    #primes = []
    for j in range(1, int(math.sqrt(number)) // 2 + 1):
        i = 2 * j + 1
        if number % i == 0:
            return i
            #if any(i % p == 0 for p in primes):
            #    continue
            #primes.append(i)
    return number


def is_prime(n):
    """Checks whether n is prime.

    Args:
        n: Integer

    Returns:
        Whether n is a prime number.

    """
    return n == first_divisor(n)


def is_prime_power(n):
    """Checks whether n is a power of prime number.

    Args:
        n: Integer

    Returns:
        Whether n is a power of a prime number.

    """
    if n % 2 == 0:
        return n & (n - 1) == 0
    base = first_divisor(n)
    return get_exponent(n, base) is not None


def closest_prime(n):
    """Returns closest prime number to n.

    If there are two such primes, returns smaller one.

    Args:
        n: Integer

    Returns:
        Closest prime number to n.

    """
    if n < 3:
        return 2
    if is_prime(n):
        return n
    offset = 1 if n % 2 == 0 else 2
    while True:
        if is_prime(n - offset):
            return n - offset
        if is_prime(n + offset):
            return n + offset
        offset += 2


def closest_prime_power(n):
    """Returns closest prime power to n.

    If there are two such prime powers, returns smaller one.

    Args:
        n: Integer

    Returns:
        Closest prime power to n.

    """
    if n < 3:
        return 2
    if is_prime_power(n):
        return n
    offset = 1
    while True:
        if is_prime_power(n - offset):
            return n - offset
        if is_prime_power(n + offset):
            return n + offset
        offset += 1


def closest_power_of_two(n):
    """Returns closest power of two to n.

    Args:
        n: Integer

    Returns:
        Closest power of two to n.

    """
    k = 2 ** (n.bit_length() - 1)
    if 2 * k - n > n - k:
        return k
    return k * 2


def is_power_of_two(n):
    """Returns whether n is a power of 2
    """
    return get_exponent(n, 2) is not None


def binary_expansion(n):
    """Returns binary expansion of n
    """
    ret = []
    while n > 0:
        power = 2 ** (n.bit_length() - 1)
        n -= power
        ret.append(power)
    return ret


def closest_odd_prime_power(n):
    """Returns closest odd prime power to n. If there are two such prime powers,
    returns smaller one."""
    if n <= 3:
        return 3
    if n % 2 == 1 and is_prime_power(n):
        return n
    offset = 1 if n % 2 == 0 else 2
    while True:
        if is_prime_power(n - offset):
            return n - offset
        if is_prime_power(n + offset):
            return n + offset
        offset += 2


def next_odd_divisor(number, previous):
    """Returns next divisor greater than 'previous'.
    Number must not be divisible by any number <= previous.
    """
    for j in range(previous // 2 + 1, int(math.sqrt(number)) // 2 + 1):
        i = 2 * j + 1
        if number % i == 0:
            return i
    return number


def get_exponent(number, base):
    """If number = base**k, returns k. Else returns None
    """
    if number <= 1: return 0
    k = 0
    if base > 1:
        while number % base == 0:
            number /= base
            k += 1
    return k if number == 1 else None


prod = lambda seq: reduce(operator.mul, seq, 1)


def _removeFactor(number, factor):
    """Returns maximal power of 'factor', dividing 'number' and number divided
        by factor in that power
    """
    power = 0
    while number % factor == 0:
        number /= factor
        power += 1
    return power, number


def _factorize_number(number):
    factors = Counter()
    # first handle the 2 for other primes are odd, so that we can then
    # increment divisor by two
    power, remainder = _removeFactor(number, 2)
    if power:
        factors[2] += power

    currentDivisor = 1
    while remainder > 1:
        # search for the next divisor
        currentDivisor = next_odd_divisor(remainder, currentDivisor)
        # and remove it
        power, remainder = _removeFactor(remainder,
            currentDivisor)
        if power:
            factors[currentDivisor] += power
    return factors


class Integer(object):
    """Represents integer with methods to factorize.
    Usage: Integer(12345) for number 12345 or Integer((2,5), (3,2), 5, 7) for number 2^5 * 3^3 * 5 * 7
    """

    def __init__(self, *args):
        if not args:
            self._int = 1
            self._factors = Counter()
        elif len(args) == 1:
            if isinstance(args[0], int):
                self._int = args[0]
                self._factors = Counter({args[0]: 1})
            elif isinstance(args[0], Integer):
                self._int = args[0]._int
                self._factors = args[0]._factors.copy()
            elif isinstance(args[0], dict):
                self._factors = Counter(args[0])
                self._multiply()
        else:
            self._factors = Counter()
            for arg in args:
                if type(arg) is int:
                    self._factors[arg] += 1
                else:
                    if arg[1]: self._factors[arg[0]] += arg[1]
            self._multiply()

    def _multiply(self):
        self._int = reduce(operator.mul, self._factors.elements(), 1)

    def __int__(self):
        return self._int

    @staticmethod
    def _cmp(a, b):
        return (a > b) - (a < b)

    def __cmp__(self, other):
        if isinstance(other, Integer):
            return self._cmp(self._int, other._int)
        return self._cmp(self._int, other)

    def copy(self):
        copy = Integer()
        copy._factors = self._factors.copy()
        copy._int = self._int
        return copy

    def __imul__(self, other):
        if isinstance(other, Integer):
            self._factors += other._factors
            self._int *= other._int
        elif isinstance(other, int) or isinstance(other, long):
            self._factors[other] += 1
            self._int *= other
        return self

    def __mul__(self, other):
        ret = None
        if isinstance(other, Integer):
            ret = Integer()
            ret._factors = other._factors + self._factors
            ret._int = other._int * self._int
        elif isinstance(other, int) or isinstance(other, long):
            ret = self.copy()
            ret._factors[other] += 1
            ret._int *= other
        return ret

    def __rmul__(self, other):
        return self.__mul__(other)

    #    def __div__(self, other):
    #        if other == 1:
    #            return self.copy()
    #        other = Integer(other)
    #        other.factorize()
    #        ret = Integer()
    #        to_factor = []
    #        for factor in self._factors.keys():
    #            for prime_factor in other._factors:
    #                if factor % prime_factor == 0:
    #                    to_factor.append(factor)
    #                    break
    #        for factor in to_factor:
    #            self._factorize_divisor(factor)
    #        for factor, value in self._factors.iteritems():
    #            p = value - other._factors[factor]
    #            if p > 0:
    #                ret._factors[factor] += p
    #        ret._multiply()
    #        return ret
    #
    #    def __floordiv__(self, other):
    #        return self.__div__(other)

    def __mod__(self, other):
        return self._int % int(other)

    def __str__(self):
        return str(self._int)

    def str_factorized(self):
        """Returns factorized string representation
        """
        self.factorize()
        factors_keys = sorted(self._factors.keys())
        power = lambda k: "^" + str(k) if k > 1 else ""
        factor_power_str = lambda f, p: "{}{}".format(f, power(p))
        return " * ".join(factor_power_str(f, self._factors[f]) for f in factors_keys)

    def str_verbose(self):
        """Same as str_factorised
        """
        return self.str_factorized()

    def str_latex(self):
        """Returns factorized latex representation
        """
        self.factorize()
        factors = self._factors.items()
        factors.sort(key=lambda x: x[0])

        def power(k):
            if k == 1:
                return ""
            template = "^{}" if k < 10 else "^{{{}}}"
            return template.format(k)

        factor_power_str = lambda f, p: "{}{}".format(f, power(p))
        return " \cdot ".join(factor_power_str(f, p) for f, p in factors)

    def div_by_prime(self, prime):
        for factor in self._factors.keys():
            if factor % prime == 0:
                p = self._factors[factor]
                del self._factors[factor]
                pow, rest = _removeFactor(factor, prime)
                self._factors[prime] += pow * p - 1
                if rest > 1:
                    self._factors[rest] += p
                self._int //= prime
                break


    def _factorize_divisor(self, divisor):
        """Factorizes one factor of this number
        """
        p = self._factors[divisor]
        del self._factors[divisor]
        if not p: return
        for key, value in _factorize_number(divisor).items():
            self._factors[int(key)] += value * p

    def factorize(self):
        """Factorize all not factorized divisors
        """
        for x in list(self._factors.keys()):  # list creates a copy
            self._factorize_divisor(x)
        return self._factors


    @property
    def factors(self):
        return self._factors


PRIME = 1
PRIME_POWER = 2

class Constraints(object):
    """Class representing numeric constraints, e.g. for dimension and
    characteristic of classical group. Minimal value must fit the constraints.
    """

    def __init__(self, min=None, parity=0, primality=None):
        self._min = min
        self._parity = parity
        self._primality = primality

    def closest_valid(self, value):
        """Returns closest number, that is valid under these constraints.
        """
        if self._min is not None:
            value = max(value, self._min)
        if self._primality == PRIME:
            if self._parity == 1:
                return 2 if 2 >= self._min else None
            elif self._parity == -1:
                value = closest_prime(value)
            else:
                value = closest_prime(value)
                if value < 3:
                    value = 3
        elif self._primality == PRIME_POWER:
            if self._parity == 1:
                value = closest_power_of_two(value)
            elif self._parity == -1:
                value = closest_odd_prime_power(value)
            else:
                value = closest_prime_power(value)
        else:
            if self._parity == 1:
                value -= value % 2
            if self._parity == -1:
                value -= 1 - (value % 2)

        return value

    def is_valid(self, value):
        """Returns true iff given value is valid under these constraints.
        """
        if self._min is not None and value < self._min:
            return False
        if self._parity == 1 and value % 2 == 1:
            return False
        if self._parity == -1 and value % 2 == 0:
            return False
        if self._primality == PRIME and not is_prime(value):
            return False
        if self._primality == PRIME_POWER and not is_prime_power(value):
            return False
        return True