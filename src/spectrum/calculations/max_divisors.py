from spectrum.calculations.groups import Field, ClassicalGroup
from spectrum.calculations.numeric import first_divisor, Integer

__author__ = 'Daniel Lytkin'


def first_primes(n):
    """Returns n first prime numbers.
    """
    ret = [2]
    n -= 1
    i = 3
    while n:
        while any(i % prime == 0 for prime in ret):
            i += 2
        ret.append(i)
        n -= 1
    return ret


def primes_less_than(n):
    """Returns list of primes less than n.
    """
    if n < 2: return []
    ret = [2]
    i = 3
    while True:
        while any(i % prime == 0 for prime in ret):
            i += 2
        if i >= n:
            break
        ret.append(i)
    return ret


def is_prime(n):
    return n == first_divisor(n)


def _prime_factors(integer):
    integer.factorize()
    return set(integer.factors.keys())

_integers = {}

def _get_factorized(base, pow):
    x = _integers.get((base, pow), None)
    if x is None:
        x = Integer(base ** pow - 1)
        x.factorize()
        _integers[(base, pow)] = x
    return x


def _min_power(p, n, primes):
    """Minimal power t such that \pi(p(p^t-1)(p^2t-1)...(p^nt-1)) contains given set
    of primes.
    """
    t = 0
    primes = set(primes)
    primes.remove(p)
    while primes:
        t += 1
        x = Integer()
        for i in range(1, n + 1):
            x *= _get_factorized(p, t * i)
            #x = prod(Integer(p ** (t * i) - 1) for i in range(1, n + 1))
        x.factorize()
        primes -= set(x.factors)
    return t

#def _clas_params(m):
#    """Returns list of candidates (n, Field), such that
#    \pi(q*(q-1)*(q^2-1)*...*(q^n-1)) can be contained in the set of first m
#    primes.
#    """
#    primes = first_primes(m)
#    for p in primes:  # characteristic
#        for n in range(1, m + 2):
#            for alpha in range(1, (m + 1) // n + 1):
#                yield (n, Field(p, alpha))

def classical_groups(m):
    """Returns list of classical groups, such that \pi(G) is contained in the
     set of first m primes.
    """
    ret = []
    primes = first_primes(m)
    set_primes = set(primes)
    for p in primes:
        for n in range(1, m + 2):
            t = _min_power(p, n, primes)
            for alpha in range(1, t + 1):
                field = Field(p, alpha)
                to_check = []
                if n >= 2 and (n, field.order) not in [(2, 2), (2, 3)]:
                    to_check.append(ClassicalGroup("PSL", n, field))
                if (n, field.order) != (1, 2):
                    if n > 1:
                        to_check.append(ClassicalGroup("PSU", 2 * n, field))
                    to_check.append(ClassicalGroup("PSU", 2 * n + 1, field))
                if n >= 2 and field.char % 2 == 1:
                    to_check.append(ClassicalGroup("Omega", 2 * n + 1, field))
                if n >= 3:
                    to_check.append(
                        ClassicalGroup("POmega+", 2 * (n + 1), field))
                    to_check.append(
                        ClassicalGroup("POmega-", 2 * (n + 1), field))
                if n >= 2:
                    to_check.append(ClassicalGroup("PSp", 2 * n, field))

                valid = lambda group: _prime_factors(
                    group.order()) <= set_primes
                ret.extend(filter(valid, to_check))
    ret.sort(
        key=lambda group: (max(group.order().factors.keys()), group.order()))
    return ret

