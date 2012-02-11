from random import random
import math

__author__ = 'Daniel Lytkin'

class Layout(object):
    """Basic abstract implementation of layout.
    Layout provides map vertices -> coordinates, which is a tuple (x, y), each one in range 0.0 to 1.0.
    """

    def __init__(self, graph, defaultLocation=(0.0, 0.0)):
        self._graph = graph
        self._locations = dict()
        self._defaultLocation = defaultLocation

    @property
    def graph(self):
        return self._graph

    def set_location(self, vertex, x, y):
        self._locations[vertex] = (x, y)

    def get_location(self, vertex):
        if not self._locations.has_key(vertex):
            self._locations[vertex] = self._defaultLocation
        return self._locations[vertex]

    # TODO: def setLock(vertex, locked)

    def update(self):
        """Remove deleted vertices
        """
        deleted_vertices = self._locations.viewkeys() - set(
            self._graph.vertices)
        for vertex in deleted_vertices:
            del self._locations[vertex]

    def reset(self):
        self._locations.clear()


class RandomLayout(Layout):
    def __init__(self, graph):
        super(RandomLayout, self).__init__(graph)
        self.reset()

    def get_location(self, vertex):
        if not self._locations.has_key(vertex):
            self._locations[vertex] = (random(), random())
        return self._locations[vertex]


class CircleLayout(Layout):
    def __init__(self, graph, x, y, r):
        super(CircleLayout, self).__init__(graph)
        self._center = (x, y)
        self._radius = r
        self.reset()

    def reset(self):
        self._locations.clear()
        step = 2 * math.pi / len(self.graph.vertices)
        x, y = self._center
        r = self._radius
        for i, vertex in enumerate(self._graph.vertices):
            self._locations[vertex] = (x + r * math.sin(step * i),
                                       y + r * math.cos(step * i))


class SpringLayout(Layout):
    """Provides force-based layout. Edges are springs, vertices are charged
    particles.
    `rate' is repulsion divided by attraction; default 1.0.
    `damping' how fast vertices slow down; default 0.5
    `mass' function vertex -> mass. Default mass is 1.0.
    """

    def __init__(self, graph, spring_rate=10.0, spring_length=0.5,
                 electric_rate=0.01, damping=0.5, mass=lambda: 1.0):
        super(SpringLayout, self).__init__(graph)
        self._spring_rate = spring_rate
        self._spring_length = spring_length
        self._electric_rate = electric_rate
        self._damping = damping
        self._mass = mass

        # set random initial positions
        for vertex in graph.vertices:
            self._locations[vertex] = (random(), random())
        self._velocities = dict.fromkeys(graph.vertices, (0.0, 0.0))

    def _distance_sq(self, v1, v2):
        x1, y1 = self._locations[v1]
        x2, y2 = self._locations[v2]
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def _repulsion_force(self, vertex, other):
        r = self._distance_sq(vertex, other)
        if r == 0.0: return random(), random()
        c = self._electric_rate / (r ** 1.5)
        x1, y1 = self._locations[vertex]
        x2, y2 = self._locations[other]
        return (x1 - x2) * c, (y1 - y2) * c

    def _attraction_force(self, vertex, other):
        r = self._distance_sq(vertex, other) ** 0.5
        if r == 0.0: return random(), random()
        c = self._spring_rate * (self._spring_length - r) / r
        x1, y1 = self._locations[vertex]
        x2, y2 = self._locations[other]
        return (x1 - x2) * c, (y1 - y2) * c

    def step(self, time_step):
        for vertex in xrange(len(self._graph.vertices)):
            force_x, force_y = 0, 0

            for other in xrange(len(self._graph.vertices)):
                if other == vertex: continue
                repulsion = self._repulsion_force(vertex, other)
                force_x += repulsion[0]
                force_y += repulsion[1]

                if self._graph.adjacent(vertex, other):
                    attraction = self._attraction_force(vertex, other)
                    force_x += attraction[0]
                    force_y += attraction[1]

            vel_x, vel_y = self._velocities[vertex]
            vel_x = self._damping * (vel_x + time_step * force_x)
            vel_y = self._damping * (vel_y + time_step * force_y)
            self._velocities[vertex] = vel_x, vel_y

            # this is to prevent going behind borders:
            f = lambda a: min(max(0, a), 1)
            x, y = self._locations[vertex]
            x += time_step * vel_x
            y += time_step * vel_y
            self._locations[vertex] = f(x), f(y)




