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
__author__ = 'Daniel Lytkin'


def ordered_pair(a, b):
    """Returns (a, b) if a < b and (b, a) otherwise
    """
    if a > b:
        return b, a
    return a, b


class Graph(object):
    """Class representing graph. Vertices are indexed by numbers 0, 1, ...
    Values are stored in 'vertices' array.
    """

    def __init__(self, vertices=None):
        if vertices is None:
            vertices = []
        self._vertices = []
        self._adjacency = []
        for vertex in set(vertices):
            self._add_no_check(vertex)

    def _add_no_check(self, vertex):
        self._adjacency.append([False] * len(self._adjacency))
        self._vertices.append(vertex)

    def index(self, vertex):
        """Returns the index of vertex with given value. If there is no such
        vertex, returns None
        """
        try:
            return self._vertices.index(vertex)
        except ValueError:
            return None

    def _set_adjacency(self, index1, index2, value):
        index1, index2 = ordered_pair(index1, index2)
        self._adjacency[index2][index1] = value

    @property
    def vertices(self):
        """Returns graph's vertices
        """
        return list(self._vertices)

    @property
    def edges(self):
        """Returns list o graph's edges.
        """
        edges = list()
        for i in xrange(len(self._adjacency)):
            for j in xrange(len(self._adjacency[i])):
                if self._adjacency[i][j]:
                    edges.append(
                        ordered_pair(self._vertices[i], self._vertices[j]))
        edges.sort()
        return edges

    def _add_vertex(self, vertex):
        """Add new vertex to graph and return its index
        """
        v_index = self.index(vertex)
        if v_index is None:
            self._add_no_check(vertex)
            return len(self._vertices) - 1
        else:
            return v_index

    def add_vertex(self, vertex):
        """Adds new vertex to graph
        """
        self._add_vertex(vertex)

    def add_vertices(self, vertices):
        """Adds sets of vertices
        """
        for vertex in vertices:
            self.add_vertex(vertex)

    def add_edge(self, v1, v2):
        """Add new edge to graph. Adds missing vertices if necessary
        """
        i1 = self.index(v1)
        i2 = self.index(v2)
        if i1 is None:
            self._add_no_check(v1)
            i1 = len(self._vertices) - 1
        if i2 is None:
            self._add_no_check(v2)
            i2 = len(self._vertices) - 1
        self._set_adjacency(i1, i2, True)

    def add_edges(self, edges):
        """Adds sets of edges
        """
        for edge in edges:
            self.add_edge(*edge)

    def neighbors(self, index):
        """Returns indices of neighbors of vertex with specified index.
        """
        neighbors = []
        for i in xrange(index):
            if self._adjacency[index][i]:
                neighbors.append(i)
        for j in xrange(index + 1, len(self._adjacency)):
            if self._adjacency[j][index]:
                neighbors.append(j)
        return neighbors

    def clone_vertex(self, index, value):
        """Add new vertex 'value' with same neighbors as given, and connect to
        given. Or connects given and all its neighbors to 'value' if is is
        already in the set of vertices. Returns index of clone.

        """
        # adjacency of new vertex with all other vertices:
        new_row = (list(self._adjacency[index]) +
                  [True] +
                  [self._adjacency[j][index]
                   for j in xrange(index + 1, len(self._adjacency))])
        v_index = self.index(value)
        if v_index is None:
            self._adjacency.append(new_row)
            self._vertices.append(value)
            return len(self._adjacency) - 1
        else:
            for i in xrange(len(self._adjacency)):
                if i != v_index and new_row[i]:
                    self._set_adjacency(v_index, i, True)

    def adjacent(self, index1, index2):
        """Returns true iff vertices with indices index1 and index2 are
        adjacent
        """
        index1, index2 = ordered_pair(index1, index2)
        return self._adjacency[index2][index1]

    def as_sparse_graph(self):
        """Returns pair <vertices>, <edges> for this graph
        """
        vertices = list(self._vertices)
        vertices.sort()
        return vertices, self.edges

    def _max_cocliques_between_indices(self, indices):
        """Searches for largest cocliques among vertices with specified indices
        """
        if len(indices) == 1:
            return [list(indices)]

        limit = 0
        cocliques = [[]]

        for j in xrange(len(indices) - limit - 1):
            i = indices[j]
            # candidates for the next vertex in coclique:
            t = filter(lambda x: (x > i and not self._adjacency[x][i]), indices)
            if len(t) < limit:
                continue
            next_cocliques = self._max_cocliques_between_indices(t)
            for coclique in next_cocliques:
                if len(coclique) < limit:
                    continue
                if len(coclique) > limit:
                    # found larger coclique, delete old ones
                    cocliques = []
                    limit = len(coclique)
                coclique.insert(0, i)
                cocliques.append(coclique)

        return cocliques

    def max_cocliques(self):
        """Returns set of cocliques of maximal size (slow)
        """
        cocliquesIndices = self._max_cocliques_between_indices(
            range(len(self._adjacency)))
        return [map(lambda i: self._vertices[i], coclique)
                for coclique in cocliquesIndices]


def full_graph(n):
    """Creates full graph on n vertices
    """
    g = Graph()
    for i in xrange(n):
        g._vertices.append(i)
        g._adjacency.append([True] * len(g._adjacency))
    return g
