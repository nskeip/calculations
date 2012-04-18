from collections import Counter
from math import sqrt

__author__ = 'Daniel Lytkin'

# Module providing methods to calculate GCD and LCM etc.

def gcd(a, b):
    """Returns GCD of two numbers
    """
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Returns LCM of two numbers
    """
    return a / gcd(a, b) * b


def prime_part(n, b):
    """Returns b'-part of number n, which is the greatest divisor of n coprime
    to d
    """
    while True:
        d = gcd(n, b)
        if d <= 1: break
        n //= d
    return n


def filter_divisors(iterable, reverse=False):
    """
    removes all elements that divide any other.
    input argument must be in decreasing order
    If 'reverse' is True, returns list in increasing order
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
    """Converts raw sequence of numbers to sorted sequence without divisors
    """
    ret = list(sequence)
    ret.sort(reverse=True)
    return filter_divisors(ret, reverse=reverse)


def first_divisor(number):
    """Returns smallest divisor of 'number' greater than 1
    """
    if number % 2 == 0: return 2
    #primes = []
    for j in xrange(1, int(sqrt(number)) // 2 + 1):
        i = 2 * j + 1
        if number % i == 0:
            return i
            #if any(i % p == 0 for p in primes):
            #    continue
            #primes.append(i)
    return number


def is_prime(n):
    """Checks whether n is prime."""
    return n == first_divisor(n)


def is_prime_power(n):
    """Checks whether n is a power of prime number."""
    base = first_divisor(n)
    return get_exponent(n, base) is not None


def closest_prime(n):
    """Returns closest prime number to n. If there are two such primes, returns
    smaller one."""
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
    """Returns closest prime power to n. If there are two such prime powers,
    returns smaller one."""
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
    """
    k = 2 ** (n.bit_length() - 1)
    if 2 * k - n > n - k:
        return k
    return k * 2


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
    for j in xrange(previous // 2 + 1, int(sqrt(number)) // 2 + 1):
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


prod = lambda seq: reduce(lambda x, y: x * y, seq, 1)


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
        self._factorization_str = False
        if not args:
            self._int = 1
            self._factors = Counter()
        elif len(args) == 1:
            if isinstance(args[0], int) or isinstance(args[0], long):
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
                if type(arg) in (int, long):
                    self._factors[arg] += 1
                else:
                    if arg[1]: self._factors[arg[0]] += arg[1]
            self._multiply()

    def _multiply(self):
        self._int = reduce(lambda x, y: x * y, self._factors.elements(), 1)

    def __int__(self):
        return self._int

    def __cmp__(self, other):
        if isinstance(other, Integer):
            return cmp(self._int, other._int)
        return cmp(self._int, other)

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

    def enable_factorization_str(self, enable=True):
        """Sets __str__ to show factorized number instead of a product
        """
        self._factorization_str = enable
        if enable:
            self.factorize()

    def __str__(self):
        if not self._factorization_str:
            return str(self._int)
        factors = self._factors.items()
        factors.sort(key=lambda x: x[0])
        factor_power_str = (lambda f, p: "{}^{}".format(f, p)
        if p > 1 else str(f))
        return " * ".join(factor_power_str(f, p) for f, p in factors)

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
        for key, value in _factorize_number(divisor).iteritems():
            self._factors[key] += value * p

    def factorize(self):
        """Factorize all not factorized divisors
        """
        for x in self._factors.keys():
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