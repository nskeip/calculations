from random import random
import math

__author__ = 'Daniel Lytkin'

class Layout(object):
    """Basic abstract implementation of layout.
    Layout provides map vertices -> coordinates, which is a tuple (x, y), each one in range 0.0 to 1.0.
    """

    def __init__(self, graph, defaultLocation=(0.0, 0.0)):
        self._graph = graph
        self._coordMap = dict()
        self._defaultLocation = defaultLocation

    @property
    def graph(self):
        return self._graph

    def set_location(self, vertex, x, y):
        self._coordMap[vertex] = (x, y)

    def get_location(self, vertex):
        if not self._coordMap.has_key(vertex):
            self._coordMap[vertex] = self._defaultLocation
        return self._coordMap[vertex]

    def update(self):
        """Remove deleted vertices
        """
        deleted_vertices = self._coordMap.viewkeys() - set(
            self._graph.vertices)
        for vertex in deleted_vertices:
            del self._coordMap[vertex]

    def reset(self):
        self._coordMap.clear()


class RandomLayout(Layout):
    def __init__(self, graph):
        super(RandomLayout, self).__init__(graph)
        self.reset()

    def get_location(self, vertex):
        if not self._coordMap.has_key(vertex):
            self._coordMap[vertex] = (random(), random())
        return self._coordMap[vertex]


class CircleLayout(Layout):
    def __init__(self, graph, x, y, r):
        super(CircleLayout, self).__init__(graph)
        self._center = (x, y)
        self._radius = r
        self.reset()

    def reset(self):
        self._coordMap.clear()
        step = 2 * math.pi / len(self.graph.vertices)
        x, y = self._center
        r = self._radius
        for i, vertex in enumerate(self._graph.vertices):
            self._coordMap[vertex] = (x + r * math.sin(step * i),
                                      y + r * math.cos(step * i))


class SpringLayout(Layout):
    """Provides force-based layout. Edges are springs, vertices are charged
    particles.
    `rate' is repulsion divided by attraction; default 1.0.
    `damping' how fast vertices slow down; default 0.5
    `mass' function vertex -> mass. Default mass is 1.0.
    """

    def __init__(self, graph, spring_rate=1.0, spring_length=0.2,
                 electric_rate=1.0, damping=0.5, mass=lambda: 1.0):
        super(SpringLayout, self).__init__(graph)
        self._spring_rate = spring_rate
        self._spring_length = spring_length
        self._electric_rate = electric_rate
        self._damping = damping
        self._mass = mass

        # set random initial positions
        for vertex in graph.vertices:
            self._coordMap[vertex] = (random(), random())
        self._velocities = dict.fromkeys(graph.vertices, (0.0, 0.0))

    def _distance_sq(self, v1, v2):
        x1, y1 = self._coordMap[v1]
        x2, y2 = self._coordMap[v2]
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def _repulsion(self, vertex, other):
        return self._electric_rate / self._distance_sq(vertex, other)

    def _attraction(self, vertex, other):
        r = self._distance_sq(vertex, other) ** 0.5
        return self._spring_rate * (self._spring_length - r)

    def step(self, time_step):
        for vertex in self._graph.vertices:
            pass



