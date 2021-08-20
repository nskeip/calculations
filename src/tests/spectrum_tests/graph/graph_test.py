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
import unittest

from spectrum.graph.graph import Graph, full_graph

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

    def test_add_vertices(self):
        vertices = [1, 2, 3, 4, 5]
        g = Graph(vertices)
        h = Graph()
        h.add_vertices(vertices)
        self.assertSparseGraphEqual(g.as_sparse_graph(), h.as_sparse_graph())

    def test_vertices(self):
        g = Graph([1, 2, 3])
        self.assertSequenceEqual([1, 2, 3], list(g.vertices))


    def test_clone_vertex(self):
        vertices = [1, 2, 3, 4, 5]
        g = Graph(vertices)
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (4, 5)]
        g.add_edges(edges)
        g.clone_vertex(g.index(2), 6)
        self.assertSparseGraphEqual((vertices + [6], edges + [(1, 6), (2, 6),
            (4, 6), (5, 6)]), g.as_sparse_graph())

        g = Graph(vertices)
        g.add_edges(edges)
        g.clone_vertex(g.index(2), 3)
        self.assertSparseGraphEqual((vertices,
                                     edges + [(2, 3), (3, 4), (3, 5)]),
            g.as_sparse_graph())

    def test_max_cocliques(self):
        vertices = list(range(6))
        edges = [(0, 1), (0, 5), (1, 2), (1, 3),
            (1, 4), (1, 5), (2, 3), (2, 5)]
        g = Graph(vertices)
        g.add_edges(edges)

        cocliques = [list(cc) for cc in g.max_cocliques()]
        expected = [[0, 2, 4], [0, 3, 4], [3, 4, 5]]
        self.assertSequenceEqual(expected, cocliques)

    def test_full_graph(self):
        g = full_graph(4)

        expectedVertices = list(range(4))
        expectedEdges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        self.assertSparseGraphEqual((expectedVertices, expectedEdges),
            g.as_sparse_graph())

    def test_adjacent(self):
        g = Graph(list(range(3)))
        g.add_edge(0, 1)
        self.assertTrue(g.adjacent(0, 1))
        self.assertFalse(g.adjacent(1, 2))

    def test_neighbors(self):
        g = Graph(list(range(5)))
        edges = [(0, 1), (0, 3), (0, 4), (1, 2), (2, 3), (2, 4)]
        g.add_edges(edges)

        self.assertEqual([1, 3, 4], g.neighbors(0))
        self.assertEqual([1, 3, 4], g.neighbors(2))
