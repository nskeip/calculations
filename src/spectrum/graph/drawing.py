from Tkinter import Canvas
from shapes import create_default_shape, EdgeShape
from spectrum.graph.graph import ordered_pair
from spectrum.tools.observers import Observable

__author__ = 'Daniel Lytkin'

PICKING = 0
TRANSLATING = 1


def vsum(v1, v2):
    """2D vector sum"""
    return v1[0] + v2[0], v1[1] + v2[1]


def vdiff(v1, v2):
    """2D vector difference"""
    return v1[0] - v2[0], v1[1] - v2[1]


class PickedState(Observable):
    """Picked state of graph vertices. Used to manipulate vertices on canvas.
    """

    def __init__(self):
        super(PickedState, self).__init__()
        self._picked = set()

    def clear(self):
        for item in self.get_picked().copy():
            self.pick(item, False)

    def pick(self, item, pick=True):
        if pick:
            self._picked.add(item)
        else:
            self._picked.remove(item)
            # fire state changed event:
        self.notify(item)

    def is_picked(self, item):
        return item in self._picked

    def get_picked(self):
        return self._picked#.copy()


class MousePlugin(object):
    class Click(object):
        def __init__(self, x, y, id=None):
            self.x = x
            self.y = y
            self.id = id

    def __init__(self, container):
        self._container = container

        self._selection = None
        self._click = None
        self._picked_state = container.picked_vertex_state

        container.bind("<Button-1>", self._on_press)
        container.bind("<ButtonRelease-1>", self._on_release)
        container.bind("<Motion>", self._on_drag)

    def _on_drag(self, event):
        if self._click is not None:
            if self._click.id is not None:
                picked = self._picked_state.get_picked()
                if picked:
                    for vertex in picked:
                        self._container.move_vertex(vertex,
                            event.x-self._click.x, event.y-self._click.y)
                    self._click.x = event.x
                    self._click.y = event.y
            else:
                x0, x1 = ordered_pair(self._selection.x, event.x)
                y0, y1 = ordered_pair(self._selection.y, event.y)
                self._container.coords(self._selection.id, x0, y0, x1, y1)

    def _on_press(self, event):
        self._click = self.Click(event.x, event.y)
        id = self._container.get_object_id_by_location(event.x, event.y)
        if self._container.is_vertex(id):
            self._click.id = id
            vertex = self._container._get_vertex_by_shape_id(id)
            if (not self._picked_state.is_picked(vertex) and
                not event.state & 1):
                self._picked_state.clear()
            self._picked_state.pick(vertex)
        else:
            if not event.state & 1:
                self._picked_state.clear()
            self._selection = self.Click(event.x, event.y,
                self._container.create_rectangle(
                    event.x, event.y, event.x, event.y))

    def _on_release(self, event):
        self._click = None
        if self._selection is not None:
            selection = self._container.coords(self._selection.id)
            for id in self._container.find_overlapping(*selection):
                if self._container.is_vertex(id):
                    vertex = self._container._get_vertex_by_shape_id(id)
                    self._picked_state.pick(vertex)
            self._container.delete(self._selection.id)
            self._selection = None


class Vertex(object):
    def __init__(self, value, shape):
        self._value = value
        self._shape = shape
        self._shape.add_tag("vertex")
        self._incident = set()

    @property
    def shape(self): return self._shape

    @property
    def value(self): return self._value

    @property
    def incident(self): return self._incident


class Edge(object):
    def __init__(self, start, end, shape):
        self._start = start
        self._end = end
        self._shape = shape
        self._shape.add_tag("edge")

    @property
    def shape(self): return self._shape

    @property
    def start(self): return self._start

    @property
    def end(self): return self._end


class GraphViewer(Canvas):
    def __init__(self, layout, width=400, height=400):
        Canvas.__init__(self, width=width, height=height)
        self.__w = width
        self.__h = height
        self.__margin = 20 # todo: temp

        # map value -> Vertex object
        self._vertices = dict()

        self._layout = layout

        self._picked_vertex_state = PickedState()

        self._create_vertex_shape = (lambda vertex:
                                     create_default_shape(self, vertex))
        self.update()

        # self._translate = (0, 0)

        self._mouse_plugin = MousePlugin(self)

        def createListener():
            state = self._picked_vertex_state

            def listener(vertex):
                picked = state.is_picked(vertex)
                vertex.shape.set_selection(picked)

            return listener

        self._picked_vertex_state.add_listener(createListener())

    @property
    def vertices(self):
        return self._vertices.viewvalues()

    @property
    def picked_vertex_state(self):
        return self._picked_vertex_state

    def get_object_id_by_location(self, x, y):
        """Returns id of object in specified coordinates, or None if there is
        no object. If multiple objects match, returns highest one.
        """
        try:
            return self.find_overlapping(x, y, x, y)[-1]
        except IndexError:
            return None

    def clear(self):
        """Removes all shapes from canvas; they will be created again
        """
        for id in self.find_all():
            self.delete(id)

    def _add_vertex(self, value):
        new_vertex = Vertex(value, self._create_vertex_shape(value))

        layout_location = self._layout.get_location(value)
        canvas_location = self._convert_layout_location(*layout_location)
        self.set_vertex_location(new_vertex, *canvas_location)
        self._vertices[value] = new_vertex

        self.__margin = max(self.__margin, new_vertex.shape.radius)

    def _add_edge(self, start_value, end_value):
        start = self._vertices[start_value]
        end = self._vertices[end_value]
        coords = (self.get_vertex_location(start) +
                  self.get_vertex_location(end))
        edge = Edge(start, end, EdgeShape(self, *coords))
        start.incident.add(edge)
        end.incident.add(edge)
        self.tag_raise("vertex", edge.shape.id)

    def update(self):
        """Updates layout, removes deleted vertices, adds missing ones.
        """
        self.layout.update()
        graph_vertices = set(self.graph.vertices)
        local_vertices = self._vertices.viewkeys()
        # deleted vertices:
        for value in local_vertices - graph_vertices:
            del self._vertices[value]
            # new vertices:
        for value in graph_vertices - local_vertices:
            self._add_vertex(value)

        self.delete("edge")
        for start_value, end_value in self.graph.edges:
            self._add_edge(start_value, end_value)

    def reset(self):
        # TODO: temporary
        """Reset vertex positions."""
        for vertex in self.graph.vertices:
            layout_location = self.layout.get_location(vertex.value)
            canvas_location = self._convert_layout_location(*layout_location)
            self.set_vertex_location(vertex, *canvas_location)

    def is_vertex(self, id):
        """Checks whether given shape id represents a vertex."""
        return id is not None and "vertex" in self.gettags(id)

    def move_vertex(self, vertex, x, y):
        id = vertex.shape.id
        self.move(id, x, y)
        canvas_location = self._get_shape_center(id)
        layout_location = self._convert_canvas_location(*canvas_location)
        self._layout.set_location(vertex, *layout_location)
        # move edges ends
        for edge in vertex.incident:
            if vertex is edge.start:
                self.move_edge(edge, x, y, 0, 0)
            else:
                self.move_edge(edge, 0, 0, x, y)

    def _get_shape_center(self, id):
        x, y, x1, y1 = self.coords(id)
        return (x + x1) / 2, (y + y1) / 2

    def get_vertex_location(self, vertex):
        return self._get_shape_center(vertex.shape.id)

    def set_vertex_location(self, vertex, x, y):
        px, py = self.get_vertex_location(vertex)
        self.move_vertex(vertex, x - px, y - py)

    def move_edge(self, edge, *dcoords):
        prev = self.coords(edge.shape.id)
        self.coords(edge.shape.id, *map(lambda x, y: x + y, prev, dcoords))

    def _convert_layout_location(self, x, y):
        """Converts layout coordinates to canvas coordinates
        """
        margin = self.__margin
        w = self.__w - 2 * margin
        h = self.__h - 2 * margin
        return margin + w * x, margin + h * y

    def _convert_canvas_location(self, x, y):
        """Converts canvas coordinates to layout coordinates
        """
        margin = self.__margin
        w = self.__w
        h = self.__h
        return (x - margin) / (w - 2 * margin), (y - margin) / (h - 2 * margin)

    def _get_vertex_by_shape_id(self, id):
        for vertex in self._vertices.itervalues():
            if vertex.shape.id == id:
                return vertex
        return None

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, layout):
        """Setter for graph layout"""
        self.clear()
        self._layout = layout

    @property
    def graph(self):
        """Returns current graph in container"""
        return self._layout.graph

