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
    """Returns b'-part of number n, which is the greatest divisor of n coprime to d
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
    """Returns lowest divisor of 'number' greater than 1
    """
    if not number % 2: return 2
    for j in xrange(1, int(sqrt(number)) // 2 + 1):
        i = 2 * j + 1
        if number % i == 0:
            return i
    return number


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


class Integer:
    """Represents integer with methods to factorize.
    Usage: Integer(12345) for number 12345 or Integer((2,5), (3,2), 5, 7) for number 2^5 * 3^3 * 5 * 7
    """

    def __init__(self, *args):
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
        ret = Integer()
        if isinstance(other, Integer):
            ret._factors = other._factors + self._factors
            ret._int = other._int * self._int
        elif isinstance(other, int) or isinstance(other, long):
            ret._factors[other] += 1
            ret._int *= other
        return ret

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        other = Integer(other)
        other.factorize()
        ret = Integer()
        for factor in self._factors.keys():
            for prime_factor in other._factors:
                if factor % prime_factor == 0:
                    self._factorize_divisor(factor)
                    break
        for factor, value in self._factors.iteritems():
            p = value - other._factors[factor]
            if p > 0:
                ret._factors[factor] += p
        ret._multiply()
        return ret

    def __floordiv__(self, other):
        return self.__div__(other)

    def __repr__(self):
        return "{} = {}".format(self._int, self._factors)


    def _factorize_divisor(self, divisor):
        """Factorizes one factor of this number
        """
        p = self._factors[divisor]
        if not p: return
        for key, value in _factorize_number(divisor).iteritems():
            self._factors[key] += value * p
        del self._factors[divisor]

    def factorize(self):
        """Factorize all not factorized divisors
        """
        for x in self._factors.keys():
            self._factorize_divisor(x)
        return self._factors


    @property
    def factors(self):
        return self._factors
