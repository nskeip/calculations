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
from tkinter import Canvas

from shapes import EdgeShape
from spectrum.graph import graph
from spectrum.graph.geometry import Point
from spectrum.gui.graph import shapes
from spectrum.tools.observers import Observable

__author__ = 'Daniel Lytkin'

PICKING = 0
TRANSLATING = 1

# params of selection rectangle
SELECTION_KW = {"outline": "#aaaaff"}


GROUP_COLORS = [
    '#d88686',
    '#8789d3',
    '#86cebd',
    '#ceb086',
    '#c2cc86',
    '#6794ff',
    '#1efa64',
    '#006666'
]


class PickedState(Observable):
    """'picked'/'not picked' state of graph vertices
    """

    def __init__(self):
        super(PickedState, self).__init__()
        self._picked = set()

    def clear(self):
        """Sets all elements unpicked
        """
        for item in self.get_picked().copy():
            self.pick(item, False)

    def pick(self, item, pick=True):
        """Sets picked state of 'item'
        """
        if pick:
            self._picked.add(item)
        else:
            self._picked.remove(item)

        # fire state changed event:
        self.notify(item)

    def is_picked(self, item):
        """Returns true if 'item' is in picked state
        """
        return item in self._picked

    def get_picked(self):
        """Returns set of all picked items
        """
        return self._picked  # .copy()


class MousePlugin(object):
    """Class responsible for all mouse manipulations with graph on canvas.
    """

    def apply(self, canvas):
        """Initializes the plugin for given canvas
        """
        self._canvas = canvas

        self._selection = None
        self._selection_rect = None
        self._click = None
        self._click_id = None
        self._picked_state = canvas.picked_vertex_state

        canvas.bind("<Button-1>", self._on_press)
        canvas.bind("<ButtonRelease-1>", self._on_release)
        canvas.bind("<Motion>", self._on_drag)

    def _on_drag(self, event):
        if self._click is not None:
            if self._click_id is not None:
                picked = self._picked_state.get_picked()
                if picked:
                    for vertex in picked:
                        self._canvas.move_vertex(vertex,
                                                 Point(event.x, event.y) - self._click)
                    self._click = Point(event.x, event.y)
            else:
                x0, x1 = graph.ordered_pair(self._selection.x, event.x)
                y0, y1 = graph.ordered_pair(self._selection.y, event.y)
                self._canvas.coords(self._selection_rect, x0, y0, x1, y1)

    def _on_press(self, event):
        self._click = Point(event.x, event.y)
        self._click_id = None
        id = self._canvas.get_object_id_by_location(self._click)
        if self._canvas.is_vertex(id):
            self._click_id = id
            vertex = self._canvas._get_vertex_by_shape_id(id)
            if (not self._picked_state.is_picked(vertex) and
                    not event.state & 1):
                self._picked_state.clear()
            self._picked_state.pick(vertex)
        else:
            if not event.state & 1:
                self._picked_state.clear()
            self._selection = Point(event.x, event.y)
            self._selection_rect = self._canvas.create_rectangle(
                event.x, event.y, event.x, event.y, **SELECTION_KW)

    def _on_release(self, event):
        self._click = None
        if self._selection is not None:
            selection = self._canvas.coords(self._selection_rect)
            for id in self._canvas.find_overlapping(*selection):
                if self._canvas.is_vertex(id):
                    vertex = self._canvas._get_vertex_by_shape_id(id)
                    self._picked_state.pick(vertex)
            self._canvas.delete(self._selection_rect)
            self._selection = None


class IterationsPlugin(object):
    """This plugin enables animation for iterable graph layouts
    """

    def apply(self, canvas, time_step=50):
        """Applies plugin for given canvas. Default FPS is 30
        """
        self._canvas = canvas
        self._event_id = None
        self.time_step = time_step

    def _step(self):
        self._canvas.layout.step()
        self._canvas.reset()  # TODO: temp
        self._event_id = self._canvas.after(self.time_step, self._step)

    def iterate(self, times):
        for i in range(times):
            self._canvas.layout.step()
        self._canvas.reset()

    def start(self):
        self._step()

    def stop(self):
        self._canvas.after_cancel(self._event_id)


class Vertex(object):
    """This class connects graph vertex with its shape on the canvas.
    """

    def __init__(self, value, shape, label):
        self._value = value
        self._shape = shape
        self._label = label
        self._shape.add_tag("vertex")
        self._incident = set()

    @property
    def shape(self):
        """Returns the shape that corresponds to this vertex
        """
        return self._shape

    @property
    def label_id(self):
        """Returns 'text' canvas element, that displays vertex value
        """
        return self._label

    @property
    def value(self):
        """Returns vertex value
        """
        return self._value

    @property
    def incident(self):
        """Returns the set of incident vertices
        """
        return self._incident


class Edge(object):
    """This class connects graph edge with its shape on the canvas
    """

    def __init__(self, start, end, shape):
        self._start = start
        self._end = end
        self._shape = shape
        self._shape.add_tag("edge")

    @property
    def shape(self):
        return self._shape

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end


class GraphCanvas(Canvas, object):
    """This is a canvas with an ability to draw graphs.
    """

    def __init__(self, master, layout, margin=20, caption=None, **kw):
        Canvas.__init__(self, master,
                        width=int(layout.size.x + 2 * margin),
                        height=int(layout.size.y + 2 * margin), **kw)

        self.__margin = margin

        self._vertex_label_mode = "auto"
        # map value -> Vertex object
        self._vertices = dict()
        self._layout = layout
        self._picked_vertex_state = PickedState()
        self._create_vertex_shape = (lambda vertex:
                                     shapes.create_default_shape(self, vertex))
        self.update()

        self._caption = self.create_caption(caption) if caption else None

        # self._translate = (0, 0)

        self._mouse_plugin = MousePlugin().apply(self)

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
        self.bind("<Configure>", lambda event: self._on_configure())

    def create_caption(self, caption_text):
        from tkinter.font import Font
        font = Font(family='Helvetica', size=28)
        label_id = self.create_text(0, 0, text=caption_text, fill='#888888', font=font, anchor='sw')
        self.tag_lower(label_id)
        return label_id

    @property
    def vertex_label_mode(self):
        return self._vertex_label_mode

    @vertex_label_mode.setter
    def vertex_label_mode(self, value):
        if value in ("auto", "center"):
            self._vertex_label_mode = value
            self.update_labels_locations()

    def _on_configure(self):
        """Updates layout space size so that it fits the canvas. Called on
        every change of canvas size.
        """
        self._layout.size = Point(self.winfo_width() - 2 * self.__margin,
                                  self.winfo_height() - 2 * self.__margin)
        if self._caption:
            self.coords(self._caption, 10, self.winfo_height() - 10)

    @property
    def vertices(self):
        """Returns set of vertices on the canvas.
        """
        return self._vertices.viewvalues()

    @property
    def picked_vertex_state(self):
        """Returns picked state of vertices on the canvas.
        """
        return self._picked_vertex_state

    def get_object_id_by_location(self, point):
        """Returns id of object in specified coordinates, or None if there is
        no object. If multiple objects match, returns highest one.
        """
        try:
            return self.find_overlapping(point.x, point.y, point.x, point.y)[-1]
        except IndexError:
            return None

    def clear(self):
        """Removes all shapes from canvas; they will be created again
        """
        for id in self.find_all():
            self.delete(id)

    def _add_vertex(self, value):
        label = self.create_text(0, 0, text=value)
        new_vertex = Vertex(value, self._create_vertex_shape(value), label)

        layout_location = self._layout[self.graph.index(value)]
        canvas_location = self._convert_layout_location(layout_location)
        self.set_vertex_location(new_vertex, canvas_location)

        self._vertices[value] = new_vertex

        # this is for variable vertex shape sizes
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
        """Reset vertex positions on canvas to layout coordinates"""
        for value in self.graph.vertices:
            layout_location = self.layout[self.graph.index(value)]
            canvas_location = self._convert_layout_location(layout_location)
            self.set_vertex_location(self._vertices[value], canvas_location)
            location = self.coords(self._vertices[value].shape.id)
            #self.coords(self._vertices[value].label_id, *location)

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
        self._update_vertex_label_location(vertex)
        # move edges ends
        for edge in vertex.incident:
            if vertex is edge.start:
                self._move_edge(edge, v, Point())
            else:
                self._move_edge(edge, Point(), v)

    def _update_vertex_label_location(self, vertex):
        #v_location = self._get_shape_center(vertex.shape.id)

        vertex_index = self.graph.index(vertex.value)
        vertex_location = self.get_vertex_location(vertex)
        if self._vertex_label_mode == 'auto':
            label_vector = self._layout.get_label_vector(vertex_index)
            label_radius = self._get_shape_radius(vertex.label_id)
            distance = label_radius + vertex.shape.radius
            label_location = vertex_location + distance * label_vector
        elif self._vertex_label_mode == 'center':
            label_location = vertex_location
        else:
            raise ValueError('Invalid vertex label mode: {}'.format(self._vertex_label_mode))

        #noinspection PyArgumentList
        self.coords(vertex.label_id, *label_location)
        self.tag_raise(vertex.label_id, vertex.shape.id)

    def update_labels_locations(self):
        """Updates locations of vertex labels.

        Used when labels position logic ('center', 'auto') changes from
        outside, e.g. from window menu.

        """
        for vertex in self._vertices.values():
            self._update_vertex_label_location(vertex)

    def _get_shape_radius(self, id):
        x, y, x1, y1 = self.bbox(id)
        return (Point(x1, y1) - Point(x, y)).square() ** 0.5 / 2

    def _get_shape_center(self, id):
        x, y, x1, y1 = self.coords(id)
        return (Point(x, y) + Point(x1, y1)) / 2

    def get_vertex_location(self, vertex):
        """Returns the center of vertex' shape
        """
        return self._get_shape_center(vertex.shape.id)

    def set_vertex_location(self, vertex, location):
        """Sets the location of the center of vertex' shape
        """
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
        return Point(margin + location.x, margin + location.y)

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

    def get_vertex(self, value):
        return self._vertices[value]

    @property
    def layout(self):
        """Returns layout instance
        """
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

    def color_vertex_groups(self, groups):
        colored = []
        if groups is not None:
            for index, group in enumerate(groups):
                color = GROUP_COLORS[index % len(GROUP_COLORS)]
                for value in group:
                    vertex = self._vertices[value]
                    vertex.shape.configure(fill=color)
                    colored.append(value)
        for value, vertex in self._vertices.iteritems():
            if value not in colored:
                vertex.shape.configure(fill='white')
