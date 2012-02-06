import unittest
from spectrum.graph.graph import Graph
from spectrum.graph.layout import Layout

__author__ = 'Daniel Lytkin'

class LayoutTest(unittest.TestCase):
    def setUp(self):
        self.graph = Graph(range(5))
        self.graph.add_edges({(0, 1), (1, 2), (1, 3), (2, 3), (3, 4), (2, 4)})
        self.layout = Layout(self.graph, defaultLocation=(0.42, 0.42))

    def test_setLocation(self):
        self.assertEquals((0.42, 0.42), self.layout.get_location(0))
        self.layout.set_location(1, 1, 1)
        self.assertEquals((1, 1), self.layout.get_location(1))

        self.layout.reset()
        self.assertEquals((0.42, 0.42), self.layout.get_location(1))
