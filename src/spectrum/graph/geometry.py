__author__ = 'Daniel Lytkin'

class Point(tuple):
    """Represents 2D point.
    """

    def __new__(cls, x=0, y=0):
        return super(Point, cls).__new__(cls, (float(x), float(y)))

    def __init__(self, x=0, y=0):
        super(Point, self).__init__()

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def __add__(self, other):
        return Point(self[0] + other[0], self[1] + other[1])

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return Point(self[0] - other[0], self[1] - other[1])

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        if isinstance(other, tuple):
            # scalar product
            return self[0] * other[0] + self[1] * other[1]
            # multiplication by scalar
        return Point(other * self[0], other * self[1])

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        return Point(self[0] / other, self[1] / other)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def apply(self, function):
        """Returns new Point(f(x), f(y))
        """
        return Point(function(self.x), function(self.y))

    def square(self):
        return self * self

