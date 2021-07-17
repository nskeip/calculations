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
import codecs
import tkFileDialog
from Tkinter import Frame, PanedWindow, LabelFrame, Button, Menu, TclError, Listbox

from spectrum.graph.layout import SpringLayout
from spectrum.gui.graph.graph_canvas import GraphCanvas, IterationsPlugin
from spectrum.gui.gui_elements import GroupNameLabel, IntegerContainer, ApexListContainer, ListContainer
from spectrum.tools import tools

__author__ = 'Daniel Lytkin'


class Facade(Frame):
    """This is a Frame that contains group info, group order, apex and prime
    graph.
    """
    def __init__(self, parent, group, show_graph=True, graph_class=None, **kw):
        """
        Parameters:
            show_graph: whether to create and show graph instantly or provide a button to do that lately
            graph_factory: callable accepting one argument - the Group instance and returning Graph instance. Note that
                __str__ method of the callable is used in the UI.
        """
        Frame.__init__(self, parent, **kw)
        self._group = group
        #        self._show_apex = True
        self._show_graph = show_graph
        self._graph_class = graph_class
        self._init_variables()
        self._init_menu()
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
        graph_class = self._graph_class
        self.graph = graph_class(self._group)
        self._graph_canvas = GraphCanvas(self._right_pane, SpringLayout(self.graph), caption=str(graph_class))
        self._graph_canvas.pack(expand=True, fill='both')

        self._graph_canvas.vertex_label_mode = self.getvar(
            name=self.winfo_name() + ".vertexlabelposition")

        self._iterations_plugin = IterationsPlugin()
        self._iterations_plugin.apply(self._graph_canvas)

        self.update_layout()

    def _init_components(self):
        self._panes = PanedWindow(self, orient='horizontal', sashrelief='raised')
        self._panes.pack(expand=True, fill='both')

        self._left_pane = Frame(self._panes, padx=2, pady=2)
        self._right_pane = Frame(self._panes)
        self._panes.add(self._left_pane, width=250)
        self._panes.add(self._right_pane)

        # group name
        group_name_pane = LabelFrame(self._left_pane, text="Group", padx=10, pady=5)
        group_name_pane.pack(fill='x')

        self._group_name = GroupNameLabel(group_name_pane, self._group)
        self._group_name.pack(expand=True, fill='both')

        # group order
        group_order_pane = LabelFrame(self._left_pane, text="Order", padx=10, pady=5)
        group_order_pane.pack(fill='x')

        self._group_order = IntegerContainer(group_order_pane, integer=self._group.order())
        self._group_order.pack(expand=True, fill='both')

        # apex
        self._apex_pane = LabelFrame(self._left_pane, text="Apex", padx=10, pady=5)
        self._apex_pane.pack(expand=True, fill='both')

        self._apex_container = ApexListContainer(self._apex_pane, apex=self._group.apex())
        self._apex_container.pack(expand=True, fill='both')

        # graph controls
        cocliques_frame = LabelFrame(self._left_pane, text="Cocliques", padx=10, pady=5)
        cocliques_frame.pack(fill='x')

        self._cocliques_button = Button(cocliques_frame, text="Calculate", command=self._show_cocliques)
        self._cocliques_button.pack(anchor='nw')

        self._cocliques_container = ListContainer(cocliques_frame)
        self._cocliques_list = Listbox(self._cocliques_container)
        self._cocliques_container.set_listbox(self._cocliques_list)

        # Button(graph_controls, text='Group equivalent vertices').pack(anchor='nw')

        # this is a button that show up instead of graph canvas if we uncheck 'Show graph' checkbox.
        self._show_graph_button = Button(self._right_pane, text='Show graph',
                                         command=self._show_graph_canvas)
        self._graph_canvas = None
        if self._show_graph:
            self._show_graph_canvas()
        else:
            self._show_graph_button.pack()

    def _init_variables(self):
        def set_default_var(self, name):
            """Sets widget-specific var with same value as root.
            """
            default_var = self.getvar(name)
            local_var_name = self.winfo_name() + "." + name
            self.setvar(local_var_name, default_var)
            return local_var_name

        local_name = set_default_var(self, "vertexlabelposition")
        tools.trace_variable(self, local_name, "w",
                             self._change_vertex_label_position)

    def _change_vertex_label_position(self, name, *arg):
        # override default value
        self.setvar("vertexlabelposition", self.getvar(name))
        if self._graph_canvas is not None:
            self._graph_canvas.vertex_label_mode = self.getvar(name)

    def _init_menu(self):
        """Init menu bar content.
        """
        toplevel = self.winfo_toplevel()
        if toplevel['menu']:
            self._menu = self.nametowidget(name=toplevel['menu'])
        else:
            self._menu = Menu(toplevel)
            toplevel['menu'] = self._menu

        graph_options = Menu(self._menu, tearoff=0)
        self._menu.add_cascade(label="Graph", menu=graph_options)
        self._menu_index = self._menu.index("end")

        vertex_label_position_menu = Menu(graph_options, tearoff=0)
        graph_options.add_cascade(label="Label position", menu=vertex_label_position_menu)

        menu_var = self.winfo_name() + ".vertexlabelposition"
        vertex_label_position_menu.add_radiobutton(variable=menu_var, label="Auto", value="auto")
        vertex_label_position_menu.add_radiobutton(variable=menu_var, label="Center", value="center")

        graph_options.add_command(label="Save graph...", command=self.call_graph_save_dialog)

        self.bind("<Destroy>", self.__destroy_menu)

    #noinspection PyUnusedLocal
    def __destroy_menu(self, event):
        try:
            self._menu.delete(self._menu_index)
        except TclError:
            pass

    def _show_cocliques(self):
        cocliques = self.graph.max_cocliques()

        def select_coclique(*_):
            index = next(iter(self._cocliques_list.curselection()), None)
            if index is not None:
                selected = cocliques[int(index)]
                pick_state = self._graph_canvas.picked_vertex_state
                pick_state.clear()
                for value in selected:
                    pick_state.pick(self._graph_canvas.get_vertex(value))

        self._cocliques_list.insert(0, *[', '.join(map(str, coclique)) for coclique in cocliques])
        self._cocliques_list.bind("<Double-Button-1>", select_coclique)

        self._cocliques_button.forget()
        self._cocliques_container.pack(expand=True, fill='both')

    def call_graph_save_dialog(self):
        file_name = tkFileDialog.asksaveasfilename(defaultextension='.ps',
                                                   filetypes=[('PostScript', '.ps')], parent=self.winfo_toplevel(),
                                                   title="Save graph as image")
        if file_name:
            with codecs.open(file_name, 'w', encoding='utf-8') as f:
                f.write(self._graph_canvas.postscript())

    def update_layout(self):
        try:
            self._iterations_plugin.iterate(50)
        except AttributeError:
            pass





