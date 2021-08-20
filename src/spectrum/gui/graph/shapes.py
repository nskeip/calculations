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
from spectrum.graph.geometry import Point

__author__ = 'Daniel Lytkin'


class Shape:
    """Abstract class representing shapes on the canvas
    """

    def __init__(self, canvas):
        self._canvas = canvas
        self._id = None

    @property
    def id(self):
        """Returns object id of this shape."""
        return self._id

    def add_tag(self, tag):
        """Adds specified tag to current shape.
        """
        self._canvas.addtag_withtag(tag, self._id)

    def configure(self, **kw):
        """Calls canvas' method itemconfigure for this shape. E.g. to change
        fill color, call configure(fill="blue").
        """
        self._canvas.itemconfigure(self._id, **kw)


class EdgeShape(Shape):
    """Shape for edges (line)
    """

    def __init__(self, canvas, start, end):
        super(EdgeShape, self).__init__(canvas)
        self._id = canvas.create_line(start.x, start.y, end.x, end.y)


class VertexShape(Shape):
    """Abstract class representing shapes for vertices.
    """

    def __init__(self, canvas):
        super(VertexShape, self).__init__(canvas)
        self._id = None
        self._radius = None

    @property
    def radius(self):
        """Returns maximal distance from shape's center to its border."""
        if self._radius is None:
            x, y, x1, y1 = self._canvas.coords(self._id)
            self._radius = max((x1 - x) / 2, (y1 - y) / 2)
        return self._radius

    def set_selection(self, selected):
        """Sets whether this vertex is selected or not."""
        if selected:
            self.configure(outline="#444444", width=3)
        else:
            self.configure(outline="black", width=1)


class CircleShape(VertexShape):
    """Circle shape
    """

    def __init__(self, canvas, radius, location=Point(), **kw):
        super(CircleShape, self).__init__(canvas)
        r = radius
        self._radius = radius
        x, y = location.x, location.y
        self._id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="white", **kw)


def create_default_shape(canvas, vertex):
    """Creates default vertex shape, which is circle of radius 15"""
    return CircleShape(canvas, 15)