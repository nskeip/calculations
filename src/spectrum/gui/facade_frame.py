from Tkinter import Frame, PanedWindow, LabelFrame, Button
from spectrum.graph.layout import SpringLayout
from spectrum.gui.graph.graph_canvas import GraphCanvas, IterationsPlugin
from spectrum.gui.gui_elements import GroupNameLabel, IntegerContainer, ApexListContainer

__author__ = 'Daniel Lytkin'


class Facade(Frame):
    """This is a Frame that contains group info, group order, apex and prime
    graph.
    """

    def __init__(self, parent, group, show_graph=True, **kw):
        Frame.__init__(self, parent, **kw)
        self._group = group
        #        self._show_apex = True
        self._show_graph = show_graph
        self._init_components()


    @property
    def group(self):
        return self._group

    @property
    def apex_list_container(self):
        return self._apex_container

    @property
    def graph_canvas(self):
        return self._graph_canvas

    def _show_graph_canvas(self):
        self._show_graph_button.forget()
        # TODO: add different layouts and other options
        graph = self._group.prime_graph()
        self._graph_canvas = GraphCanvas(self._right_pane, SpringLayout(graph))
        self._graph_canvas.pack(expand=True, fill='both')

        self._iterations_plugin = IterationsPlugin()
        self._iterations_plugin.apply(self._graph_canvas)

        self.update_layout()

    def _init_components(self):
        self._panes = PanedWindow(self, orient='horizontal',
            sashrelief='raised')
        self._panes.pack(expand=True, fill='both')

        self._left_pane = Frame(self._panes, padx=2, pady=2)
        self._right_pane = Frame(self._panes)
        self._panes.add(self._left_pane)
        self._panes.add(self._right_pane)

        # group name
        group_name_pane = LabelFrame(self._left_pane, text="Group")
        group_name_pane.pack(fill='x')

        self._group_name = GroupNameLabel(group_name_pane, self._group)
        self._group_name.pack(expand=True, fill='both')

        # group order
        group_order_pane = LabelFrame(self._left_pane, text="Order")
        group_order_pane.pack(fill='x')

        self._group_order = IntegerContainer(group_order_pane,
            integer=self._group.order())
        self._group_order.pack(expand=True, fill='both')

        # apex
        self._apex_pane = LabelFrame(self._left_pane, text="Apex")
        self._apex_pane.pack(expand=True, fill='both')

        self._apex_container = ApexListContainer(self._apex_pane,
            apex=self._group.apex())
        self._apex_container.pack(expand=True, fill='both')

        self._show_graph_button = Button(self._right_pane, text='Show graph',
            command=self._show_graph_canvas)
        self._graph_canvas = None
        if self._show_graph:
            self._show_graph_canvas()
        else:
            self._show_graph_button.pack()


    def update_layout(self):
        try:
            self._iterations_plugin.iterate(50)
        except AttributeError:
            pass





