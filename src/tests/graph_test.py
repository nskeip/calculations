import unittest
from calculations.graph import Graph, PrimeGraph, FastGraph

__author__ = 'Daniel Lytkin'

class GraphTest(unittest.TestCase):
    def assertSparseGraphEqual(self, graph1, graph2):
        v1, e1 = graph1[0], graph1[1]
        v2, e2 = graph2[0], graph2[1]
        self.assertSequenceEqual(v1, v2)
        self.assertSetEqual(set(e1), set(e2))

    def test_sparse(self):
        g = Graph([7, 5, 9, 4, 2])
        g.add_edges([(7, 5), (5, 2), (4, 9), (4, 7), (7, 9)])

        expectedVertices = [2, 4, 5, 7, 9]
        expectedEdges = [(5, 7), (2, 5), (4, 9), (4, 7), (7, 9)]
        self.assertSparseGraphEqual((expectedVertices, expectedEdges),
            g.as_sparse_graph())

    def test_prime_graph(self):
        g = PrimeGraph([72, 90, 240, 246, 328, 410, 728, 730])

        expectedVertices = [2, 3, 5, 7, 13, 41, 73]
        expectedEdges = [(2, 3), (2, 5), (2, 7), (2, 13), (2, 41),
            (2, 73), (3, 5), (3, 41), (5, 41), (5, 73), (7, 13)]
        self.assertSparseGraphEqual((expectedVertices, expectedEdges),
            g.as_sparse_graph())

    def test_add_vertices(self):
        vertices = [1, 2, 3, 4, 5]
        g = Graph(vertices)
        h = Graph()
        h.add_vertices(vertices)
        self.assertSparseGraphEqual(g.as_sparse_graph(), h.as_sparse_graph())

    def test_vertices(self):
        g = Graph([1, 2, 3])
        self.assertSequenceEqual([1, 2, 3], list(g.vertices))

    def test_fast_graph(self):
        apex = [8, 28, 36, 126, 130, 455, 511, 513, 585]

        g = FastGraph(apex)

        expectedVertices = [2, 7, 9, 19, 65, 73]
        expectedEdges = [(2, 7), (2, 9), (2, 65), (7, 9), (7, 65), (7, 73),
            (9, 19), (9, 65)]
        self.assertSparseGraphEqual((expectedVertices, expectedEdges),
            g.as_sparse_graph())

    def test_clone_vertex(self):
        vertices = [1, 2, 3, 4, 5]
        g = Graph(vertices)
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (4, 5)]
        g.add_edges(edges)
        g.clone_vertex(2, 6)
        self.assertSparseGraphEqual((vertices + [6], edges + [(1, 6), (2, 6),
            (4, 6), (5, 6)]), g.as_sparse_graph())

        g = Graph(vertices)
        g.add_edges(edges)
        g.clone_vertex(2, 3)
        self.assertSparseGraphEqual((vertices,
                                     edges + [(2, 3), (3, 4), (3, 5)]),
            g.as_sparse_graph())

    def test_max_cocliques(self):
        vertices = range(6)
        edges = [(0, 1), (0, 5), (1, 2), (1, 3),
            (1, 4), (1, 5), (2, 3), (2, 5)]
        g = Graph(vertices)
        g.add_edges(edges)

        cocliques = g.max_cocliques()
        expected = [[0, 2, 4], [0, 3, 4], [3, 4, 5]]
        self.assertSequenceEqual(expected, cocliques)