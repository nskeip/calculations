__author__ = 'Daniel Lytkin'

def ordered_pair(a, b):
    """Returns (a, b) if a < b and (b, a) otherwise
    """
    if a > b:
        return b, a
    return a, b


class Graph:
    def __init__(self, vertices=list()):
        self._vertices = []
        self._adjacency = []
        for vertex in set(vertices):
            self._add_no_check(vertex)

    def _add_no_check(self, vertex):
        self._adjacency.append([False] * len(self._adjacency))
        self._vertices.append(vertex)

    def index(self, vertex):
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
        vIndex = self.index(vertex)
        if vIndex is None:
            self._add_no_check(vertex)
            return len(self._vertices) - 1
        else:
            return vIndex

    def add_vertex(self, vertex):
        """Adds new vertex to graph
        """
        self._add_vertex(vertex)

    def add_vertices(self, vertices):
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
        newRow = (list(self._adjacency[index]) +
                  [True] +
                  [self._adjacency[j][index]
                   for j in xrange(index + 1, len(self._adjacency))])
        vIndex = self.index(value)
        if vIndex is None:
            self._adjacency.append(newRow)
            self._vertices.append(value)
            return len(self._adjacency) - 1
        else:
            for i in xrange(len(self._adjacency)):
                if i != vIndex and newRow[i]:
                    self._set_adjacency(vIndex, i, True)


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
        if len(indices) == 1: return [list(indices)]

        max = 0
        cocliques = []

        for j in xrange(len(indices) - max - 1):
            i = indices[j]
            # candidates for the next vertex in coclique:
            t = filter(lambda x: (x > i and self._adjacency[x][i] == False),
                indices)
            if len(t) < max: continue
            nextCocliques = self._max_cocliques_between_indices(t)
            for coclique in nextCocliques:
                if len(coclique) < max: continue
                if len(coclique) > max:
                    # found larger coclique, delete old ones
                    cocliques = []
                    max = len(coclique)
                coclique.insert(0, i)
                cocliques.append(coclique)

        return cocliques


    def max_cocliques(self):
        cocliquesIndices = self._max_cocliques_between_indices(
            range(len(self._adjacency)))
        return [map(lambda i: self._vertices[i], coclique)
                for coclique in cocliquesIndices]


def full_graph(n):
    g = Graph()
    for i in xrange(n):
        g._vertices.append(i)
        g._adjacency.append([True] * len(g._adjacency))
    return g
