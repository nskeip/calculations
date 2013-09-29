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
        """If multiplied by integer, returns vector multiplied by scalar;
        if multiplied by other vector, returns scalar product.
        """
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
        """Returns scalar square of the vector
        """
        return self * self

    def identity(self):
        """Returns the vector divided by its length
        """
        square = self.square()
        return self / (square ** 0.5) if square else Point()

