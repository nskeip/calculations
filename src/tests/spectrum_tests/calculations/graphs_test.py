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

from spectrum.calculations.graphs import FastGraph, PrimeGraph
from spectrum.calculations.groups import Group

__author__ = 'Daniel Lytkin'

class GraphsTest(unittest.TestCase):
    def assertSparseGraphEqual(self, graph1, graph2):
        v1, e1 = graph1[0], graph1[1]
        v2, e2 = graph2[0], graph2[1]
        self.assertSequenceEqual(v1, v2)
        self.assertSetEqual(set(e1), set(e2))

    @staticmethod
    def _make_group_with_specified_apex(apex):
        class GroupWithSpecifiedApex(Group):
            def apex(self):
                return apex
        return GroupWithSpecifiedApex()

    def test_fast_graph(self):
        apex = [27, 59040, 65520, 531432, 1594320, 1771440, 1790880, 2391480,
                14348904, 16120104, 43046720, 43578080, 47829680, 48419360,
                53733680, 64570080, 193710244, 217625044, 217924025]

        g = FastGraph(self._make_group_with_specified_apex(apex))

        expectedVertices = [3, 4, 5, 41, 73, 91, 1181, 3281, 7381, 532171,
                            597871]
        expectedEdges = [(3, 4), (3, 5), (3, 41), (3, 73), (3, 91), (3, 3281),
            (3, 7381), (3, 597871), (4, 5), (4, 41), (4, 73), (4, 91),
            (4, 3281), (4, 7381), (4, 532171), (4, 597871), (5, 41), (5, 73),
            (5, 91), (5, 1181), (5, 3281), (5, 7381), (5, 597871), (41, 73),
            (41, 91), (41, 3281), (41, 7381), (73, 91), (91, 7381),
            (91, 532171), (91, 597871), (1181, 7381)]
        self.assertSparseGraphEqual((expectedVertices, expectedEdges),
            g.as_sparse_graph())

    def test_prime_graph(self):
        g = PrimeGraph(self._make_group_with_specified_apex([72, 90, 240, 246, 328, 410, 728, 730]))

        expectedVertices = [2, 3, 5, 7, 13, 41, 73]
        expectedEdges = [(2, 3), (2, 5), (2, 7), (2, 13), (2, 41),
            (2, 73), (3, 5), (3, 41), (5, 41), (5, 73), (7, 13)]
        self.assertSparseGraphEqual((expectedVertices, expectedEdges),
            g.as_sparse_graph())
