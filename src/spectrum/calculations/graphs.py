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
import itertools
from spectrum.calculations import numeric
from spectrum.calculations.numeric import Integer
from spectrum.graph.graph import Graph
from spectrum.tools.tools import MultiModeStringFormatter

__author__ = 'Daniel Lytkin'


class PrimeGraph(Graph):
    class __metaclass__(type):
        """Provide a metaclass in order to override class-level str method"""
        def __str__(self):
            return 'Prime Graph'

    def __init__(self, group):
        Graph.__init__(self)
        apex = group.apex()
        for elem in apex:
            factors = Integer(elem).factorize().keys()
            self.add_vertices(factors)
            self.add_edges(itertools.combinations(factors, 2))


class FastGraph(Graph):
    class __metaclass__(type):
        """Provide a metaclass in order to override class-level str method"""
        def __str__(self):
            return 'Fast Graph'

    def __init__(self, group):
        Graph.__init__(self)
        apex = group.apex()
        for elem in apex:
            self._add_element(elem)

        # TODO: should be moved from model to a view
        # for i, vertex in enumerate(self._vertices):
        #     instance = MultiModeStringFormatter.mixin_to(Integer(vertex))
        #     instance.str_mode = 'verbose'
        #     self._vertices[i] = instance

    def _add_element(self, a):
        """Add new spectrum element
        """
        # these are the indices of future neighbors of a
        neighbors = []
        # memorize initial length so that we don't have to process newly added
        # vertices
        l = len(self._vertices)
        for i in range(l):
            b = self._vertices[i]
            d = numeric.gcd(a, b)
            if d == 1:
                continue
            bd = numeric.prime_part(b, d)
            if bd == 1:
                self._vertices[i] = d
                for neighbor in neighbors:
                    self._set_adjacency(i, neighbor, True)
                neighbors.append(i)
            else:
                self._vertices[i] = bd
                dIndex = self.clone_vertex(i, d)
                for neighbor in neighbors:
                    self._adjacency[dIndex][neighbor] = True
                neighbors.append(dIndex)

            a = numeric.prime_part(a, d)
            if a == 1:
                break
        if a > 1:
            index = self._add_vertex(a)
            for neighbor in neighbors:
                self._set_adjacency(index, neighbor, True)