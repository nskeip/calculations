from random import random

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
            self._graph.vertices())
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


class IterativeLayout(Layout):
    def __init__(self, graph):
        super(IterativeLayout, self).__init__(graph)

    def step(self):
        raise NotImplementedError()

    def done(self):
        return True



