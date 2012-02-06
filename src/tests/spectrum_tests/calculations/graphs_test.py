import unittest
from spectrum.calculations.graphs import FastGraph, PrimeGraph

__author__ = 'Daniel Lytkin'

class GraphsTest(unittest.TestCase):
    def assertSparseGraphEqual(self, graph1, graph2):
        v1, e1 = graph1[0], graph1[1]
        v2, e2 = graph2[0], graph2[1]
        self.assertSequenceEqual(v1, v2)
        self.assertSetEqual(set(e1), set(e2))

    def test_fast_graph(self):
        apex = [8, 28, 36, 126, 130, 455, 511, 513, 585]

        g = FastGraph(apex)

        expectedVertices = [2, 7, 9, 19, 65, 73]
        expectedEdges = [(2, 7), (2, 9), (2, 65), (7, 9), (7, 65), (7, 73),
            (9, 19), (9, 65)]
        self.assertSparseGraphEqual((expectedVertices, expectedEdges),
            g.as_sparse_graph())

    def test_prime_graph(self):
        g = PrimeGraph([72, 90, 240, 246, 328, 410, 728, 730])

        expectedVertices = [2, 3, 5, 7, 13, 41, 73]
        expectedEdges = [(2, 3), (2, 5), (2, 7), (2, 13), (2, 41),
            (2, 73), (3, 5), (3, 41), (5, 41), (5, 73), (7, 13)]
        self.assertSparseGraphEqual((expectedVertices, expectedEdges),
            g.as_sparse_graph())
