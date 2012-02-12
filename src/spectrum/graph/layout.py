from random import random
import math

__author__ = 'Daniel Lytkin'

class Layout(object):
    """Basic abstract implementation of layout.
    Layout provides map vertices -> coordinates, which is a tuple (x, y), each one in range 0.0 to 1.0.
    """

    def __init__(self, graph, defaultLocation=(0.0, 0.0)):
        self._locked = set()
        self._graph = graph
        self.__locations = dict()
        self._defaultLocation = defaultLocation

    @property
    def graph(self):
        return self._graph

    def set_unlocked_location(self, vertex, x, y):
        """Sets location of specified vertex if it is not locked."""
        if vertex not in self._locked:
            self.__locations[vertex] = (x, y)

    def set_location(self, vertex, x, y):
        """Sets location of specified vertex."""
        self.__locations[vertex] = (x, y)

    def get_location(self, vertex):
        if not self.__locations.has_key(vertex):
            self.__locations[vertex] = self._defaultLocation
        return self.__locations[vertex]

    def set_lock(self, vertex, locked):
        """Sets a lock on vertex, so that it won't be moved by layout."""
        if locked:
            self._locked.add(vertex)
        else:
            if vertex in self._locked:
                self._locked.remove(vertex)

    def is_locked(self, vertex):
        return vertex in self._locked

    def update(self):
        """Remove deleted vertices
        """
        deleted_vertices = self.__locations.viewkeys() - set(
            self._graph.vertices)
        for vertex in deleted_vertices:
            del self.__locations[vertex]

    def reset(self):
        self.__locations.clear()


class RandomLayout(Layout):
    def __init__(self, graph):
        super(RandomLayout, self).__init__(graph)
        self.reset()

    def get_location(self, vertex):
        if not self.__locations.has_key(vertex):
            self.set_unlocked_location(vertex, random(), random())
        return self.__locations[vertex]


class CircleLayout(Layout):
    def __init__(self, graph, x, y, r):
        super(CircleLayout, self).__init__(graph)
        self._center = (x, y)
        self._radius = r
        self.reset()

    def reset(self):
        self.__locations.clear()
        step = 2 * math.pi / len(self.graph.vertices)
        x, y = self._center
        r = self._radius
        for i, vertex in enumerate(self._graph.vertices):
            self.set_unlocked_location(vertex, x + r * math.sin(step * i),
                y + r * math.cos(step * i))


class SpringLayout(Layout):
    """Provides force-based layout. Edges are springs, vertices are charged
    particles.
    """

    def __init__(self, graph, spring_rate=10.0, spring_length=0.5,
                 electric_rate=0.01, damping=0.9):
        super(SpringLayout, self).__init__(graph)
        self._spring_rate = spring_rate
        self._spring_length = spring_length
        self._electric_rate = electric_rate
        self._damping = damping

        # set random initial positions
        for vertex in graph.vertices:
            self.set_unlocked_location(vertex, random(), random())
        self._velocities = dict.fromkeys(graph.vertices, (0.0, 0.0))

    def _distance_sq(self, v1, v2):
        x1, y1 = self.get_location(v1)
        x2, y2 = self.get_location(v2)
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def _repulsion_force(self, vertex, other):
        r = self._distance_sq(vertex, other)
        if r == 0.0: return random() * 0.00001, random() * 0.00001
        c = self._electric_rate / (r ** 1.5)
        x1, y1 = self.get_location(vertex)
        x2, y2 = self.get_location(other)
        return (x1 - x2) * c, (y1 - y2) * c

    def _attraction_force(self, vertex, other):
        r = self._distance_sq(vertex, other) ** 0.5
        if r == 0.0: return 0.0, 0.0
        c = self._spring_rate * (self._spring_length - r) / r
        x1, y1 = self.get_location(vertex)
        x2, y2 = self.get_location(other)
        return (x1 - x2) * c, (y1 - y2) * c

    def step(self, time_step):
        """Calculates position of vertices after a lapse of `time_step' after
        last position.
        """
        for vertex in xrange(len(self._graph.vertices)):
            force_x, force_y = 0, 0

            for other in xrange(len(self._graph.vertices)):
                if other == vertex: continue
                repulsion = self._repulsion_force(vertex, other)
                force_x += repulsion[0]
                force_y += repulsion[1]

            for other in self._graph.neighbors(vertex):
                attraction = self._attraction_force(vertex, other)
                force_x += attraction[0]
                force_y += attraction[1]

            vel_x, vel_y = self._velocities[vertex]
            vel_x = self._damping * (vel_x + time_step * force_x)
            vel_y = self._damping * (vel_y + time_step * force_y)
            self._velocities[vertex] = vel_x, vel_y

            # this is to prevent going behind borders:
            f = lambda a: min(max(0, a), 1)
            x, y = self.get_location(vertex)
            x += time_step * vel_x
            y += time_step * vel_y
            # todo: if vertex is on border, speed on axis=0
            self.set_unlocked_location(vertex, f(x), f(y))

    def total_kinetic_energy(self):
        return sum((x ** 2 + y ** 2 for x, y in self._velocities))



