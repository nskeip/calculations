from Tkinter import Canvas
from shapes import create_default_shape, EdgeShape
from spectrum.graph.geometry import Point
from spectrum.graph.graph import ordered_pair
from spectrum.tools.observers import Observable

__author__ = 'Daniel Lytkin'

PICKING = 0
TRANSLATING = 1

# params of selection rectangle
SELECTION_KW = {"outline": "#aaaaff"}


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
    def __init__(self, container):
        self._container = container

        self._selection = None
        self._selection_rect = None
        self._click = None
        self._click_id = None
        self._picked_state = container.picked_vertex_state

        container.bind("<Button-1>", self._on_press)
        container.bind("<ButtonRelease-1>", self._on_release)
        container.bind("<Motion>", self._on_drag)

    def _on_drag(self, event):
        if self._click is not None:
            if self._click_id is not None:
                picked = self._picked_state.get_picked()
                if picked:
                    for vertex in picked:
                        self._container.move_vertex(vertex,
                            Point(event.x, event.y) - self._click)
                    self._click = Point(event.x, event.y)
            else:
                x0, x1 = ordered_pair(self._selection.x, event.x)
                y0, y1 = ordered_pair(self._selection.y, event.y)
                self._container.coords(self._selection_rect, x0, y0, x1, y1)

    def _on_press(self, event):
        self._click = Point(event.x, event.y)
        self._click_id = None
        id = self._container.get_object_id_by_location(self._click)
        if self._container.is_vertex(id):
            self._click_id = id
            vertex = self._container._get_vertex_by_shape_id(id)
            if (not self._picked_state.is_picked(vertex) and
                not event.state & 1):
                self._picked_state.clear()
            self._picked_state.pick(vertex)
        else:
            if not event.state & 1:
                self._picked_state.clear()
            self._selection = Point(event.x, event.y)
            self._selection_rect = self._container.create_rectangle(
                event.x, event.y, event.x, event.y, **SELECTION_KW)

    def _on_release(self, event):
        self._click = None
        if self._selection is not None:
            selection = self._container.coords(self._selection_rect)
            for id in self._container.find_overlapping(*selection):
                if self._container.is_vertex(id):
                    vertex = self._container._get_vertex_by_shape_id(id)
                    self._picked_state.pick(vertex)
            self._container.delete(self._selection_rect)
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
    def __init__(self, layout, master=None, margin=20, **kw):
        Canvas.__init__(self, master, width=layout.size.x + 2 * margin,
            height=layout.size.y + 2 * margin, **kw)

        self.__margin = margin

        # map value -> Vertex object
        self._vertices = dict()

        self._layout = layout

        self._picked_vertex_state = PickedState()

        self._create_vertex_shape = (lambda vertex:
                                     create_default_shape(self, vertex))
        self.update()


        # self._translate = (0, 0)

        self._mouse_plugin = MousePlugin(self)

        # makes vertex shape change appearing if it was picked
        # also sets layout lock for picked vertices
        def createListener():
            state = self._picked_vertex_state
            layout = self.layout

            def listener(vertex):
                picked = state.is_picked(vertex)
                vertex.shape.set_selection(picked)
                layout.set_lock(layout.graph.index(vertex.value), picked)


            return listener

        self._picked_vertex_state.add_listener(createListener())

        # handle resize
        self.bind("<Configure>", lambda event: self.update_layout_size())


    def update_layout_size(self):
        self._layout.size = Point(self.winfo_width() - 2 * self.__margin,
            self.winfo_height() - 2 * self.__margin)

    @property
    def vertices(self):
        return self._vertices.viewvalues()

    @property
    def picked_vertex_state(self):
        return self._picked_vertex_state

    def get_object_id_by_location(self, point):
        """Returns id of object in specified coordinates, or None if there is
        no object. If multiple objects match, returns highest one.
        """
        try:
            return self.find_overlapping(point.x, point.y, point.x, point.y)[
                   -1]
        except IndexError:
            return None

    def clear(self):
        """Removes all shapes from canvas; they will be created again
        """
        for id in self.find_all():
            self.delete(id)

    def _add_vertex(self, value):
        new_vertex = Vertex(value, self._create_vertex_shape(value))

        layout_location = self._layout[self.graph.index(value)]
        canvas_location = self._convert_layout_location(layout_location)
        self.set_vertex_location(new_vertex, canvas_location)
        self._vertices[value] = new_vertex

        self.__margin = max(self.__margin, new_vertex.shape.radius)

    def _add_edge(self, start_index, end_index):
        start = self._vertices[start_index]
        end = self._vertices[end_index]
        edge = Edge(start, end, EdgeShape(self,
            self.get_vertex_location(start),
            self.get_vertex_location(end)))
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
        for value in self.graph.vertices:
            layout_location = self.layout[self.graph.index(value)]
            canvas_location = self._convert_layout_location(layout_location)
            self.set_vertex_location(self._vertices[value], canvas_location)

    def is_vertex(self, id):
        """Checks whether given shape id represents a vertex."""
        return id is not None and "vertex" in self.gettags(id)

    def move_vertex(self, vertex, v):
        """Move `vertex' by vector `v'
        """
        id = vertex.shape.id
        self.move(id, v.x, v.y)
        canvas_location = self._get_shape_center(id)
        layout_location = self._convert_canvas_location(canvas_location)
        self._layout[self.graph.index(vertex.value)] = layout_location
        # move edges ends
        for edge in vertex.incident:
            if vertex is edge.start:
                self._move_edge(edge, v, Point())
            else:
                self._move_edge(edge, Point(), v)

    def _get_shape_center(self, id):
        x, y, x1, y1 = self.coords(id)
        return (Point(x, y) + Point(x1, y1)) / 2

    def get_vertex_location(self, vertex):
        return self._get_shape_center(vertex.shape.id)

    def set_vertex_location(self, vertex, location):
        current = self.get_vertex_location(vertex)
        self.move_vertex(vertex, location - current)

    def _move_edge(self, edge, start, end):
        new = start.x, start.y, end.x, end.y
        current = self.coords(edge.shape.id)
        self.coords(edge.shape.id, *map(lambda x, y: x + y, current, new))

    def _convert_layout_location(self, location):
        """Converts layout coordinates to canvas coordinates
        """
        margin = self.__margin
        return margin + location.x, margin + location.y

    def _convert_canvas_location(self, location):
        """Converts canvas coordinates to layout coordinates
        """
        x, y = location
        margin = self.__margin
        return Point(x - margin, y - margin)

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

