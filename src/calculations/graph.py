from itertools import combinations
from calculations.numeric import Integer, gcd, primePart

__author__ = 'Daniel Lytkin'

def _pair(a, b):
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
        self._adjacency.append([False]*len(self._adjacency))
        self._vertices.append(vertex)

    def _index(self, vertex):
        try:
            return self._vertices.index(vertex)
        except ValueError:
            return None

    def _set_adjacency(self, index1, index2, value):
        index1, index2 = _pair(index1, index2)
        self._adjacency[index2][index1] = value

    def vertices(self):
        """Returns graph's vertices
        """
        return iter(self._vertices)

    def edges(self):
        edges = list()
        for i in xrange(len(self._adjacency)):
            for j in xrange(len(self._adjacency[i])):
                if self._adjacency[i][j]:
                    edges.append(_pair(self._vertices[i], self._vertices[j]))
        edges.sort()
        return edges

    def _addVertex(self, vertex):
        """Add new vertex to graph and return its index
        """
        vIndex = self._index(vertex)
        if vIndex is None:
            self._add_no_check(vertex)
            return len(self._vertices) - 1
        else:
            return vIndex

    def addVertex(self, vertex):
        """Adds new vertex to graph
        """
        self._addVertex(vertex)

    def addVertices(self, vertices):
        for vertex in vertices:
            self.addVertex(vertex)

    def addEdge(self, v1, v2):
        """Add new edge to graph. Adds missing vertices if necessary
        """
        i1 = self._index(v1)
        i2 = self._index(v2)
        if i1 is None:
            self._add_no_check(v1)
            i1 = len(self._vertices) - 1
        if i2 is None:
            self._add_no_check(v2)
            i2 = len(self._vertices) - 1
        self._set_adjacency(i1, i2, True)

    def addEdges(self, edges):
        for edge in edges:
            self.addEdge(*edge)

    def _cloneVertex(self, index, value):
        # adjacency of new vertex with all other vertices:
        newRow = list(self._adjacency[index]) + [True] +\
                 [self._adjacency[j][index] for j in xrange(index+1, len(self._adjacency))]
        vIndex = self._index(value)
        if vIndex is None:
            self._adjacency.append(newRow)
            self._vertices.append(value)
            return len(self._adjacency) - 1
        else:
            for i in xrange(len(self._adjacency)):
                if i != vIndex and newRow[i]:
                    self._set_adjacency(vIndex, i, True)

    def cloneVertex(self, vertex, value):
        """Add new vertex 'value' with same neighbors as given, and connect to given.
        Or connects given and all its neighbors to 'value' if is is already in the set of vertices.
        Returns index of clone
        """
        return self._cloneVertex(self._vertices.index(vertex), value)

    def asSparseGraph(self):
        """Returns pair <vertices>, <edges> for this graph
        """
        vertices = list(self._vertices)
        vertices.sort()
        return vertices, self.edges()

    def _maxCocliquesInIndices(self, indices):
        """Searches for largest cocliques among vertices with specified indices
        """
        if len(indices) == 1: return [list(indices)]

        max = 0
        cocliques = []

        for j in xrange(len(indices)-max-1):
            i = indices[j]
            # candidates for the next vertex in coclique:
            t = filter(lambda x: (x > i and self._adjacency[x][i]==False), indices)
            if len(t) < max: continue
            nextCocliques = self._maxCocliquesInIndices(t)
            for coclique in nextCocliques:
                if len(coclique) < max: continue
                if len(coclique) > max:
                    # found larger coclique, delete old ones
                    cocliques = []
                    max = len(coclique)
                coclique.insert(0, i)
                cocliques.append(coclique)

        return cocliques


    def maxCocliques(self):
        cocliquesIndices = self._maxCocliquesInIndices(range(len(self._adjacency)))
        return [map(lambda i: self._vertices[i], coclique) for coclique in cocliquesIndices]


class PrimeGraph(Graph):
    def __init__(self, spectrum):
        Graph.__init__(self)
        for elem in spectrum:
            factors = Integer(elem).factors().keys()
            self.addVertices(factors)
            self.addEdges(combinations(factors, 2))

class FastGraph(Graph):
    def __init__(self, spectrum):
        Graph.__init__(self)
        for elem in spectrum:
            self._addElement(elem)

    def _addElement(self, a):
        """Add new spectrum element
        """
        neighbors = [] # these are the indices of future neighbors of a
        l = len(self._vertices) # memorize initial length so that we don't have to process newly added vertices
        for i in range(l):
            b = self._vertices[i]
            d = gcd(a, b)
            if d == 1: continue
            bd = primePart(b, d)
            if bd == 1:
                self._vertices[i] = d
                for neighbor in neighbors:
                    self._set_adjacency(i, neighbor, True)
                neighbors.append(i)
            else:
                self._vertices[i] = bd
                dIndex = self._cloneVertex(i, d)
                for neighbor in neighbors:
                    self._adjacency[dIndex][neighbor] = True
                neighbors.append(dIndex)

            a = primePart(a, d)
            if a == 1: break
        if a > 1:
            index = self._addVertex(a)
            for neighbor in neighbors:
                self._set_adjacency(index, neighbor, True)

