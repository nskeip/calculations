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
from Tkinter import Frame, PanedWindow, LabelFrame, Button, Menu, TclError
import codecs
import tkFileDialog
from spectrum.graph.layout import SpringLayout
from spectrum.gui.graph.graph_canvas import GraphCanvas, IterationsPlugin
from spectrum.gui.gui_elements import GroupNameLabel, IntegerContainer, ApexListContainer
from spectrum.tools import tools

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
        graph = self._group.prime_graph()
        self._graph_canvas = GraphCanvas(self._right_pane, SpringLayout(graph))
        self._graph_canvas.pack(expand=True, fill='both')

        self._graph_canvas.vertex_label_mode = self.getvar(
            name=self.winfo_name() + ".vertexlabelposition")

        self._iterations_plugin = IterationsPlugin()
        self._iterations_plugin.apply(self._graph_canvas)

        self.update_layout()

    def _init_components(self):
        self._panes = PanedWindow(self, orient='horizontal',
            sashrelief='raised')
        self._panes.pack(expand=True, fill='both')

        self._left_pane = Frame(self._panes, padx=2, pady=2)
        self._right_pane = Frame(self._panes)
        self._panes.add(self._left_pane, width=200)
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
        toplevel = self.winfo_toplevel()
        if toplevel['menu']:
            self._menu = self.nametowidget(name=toplevel['menu'])
        else:
            self._menu = Menu(toplevel)
            toplevel['menu'] = self._menu

        graph_options = Menu(self._menu, tearoff=0)
        self._menu.add_cascade(label="Graph", menu=graph_options)
        self._menu_index = self._menu.index("end")

        vertex_label_position = Menu(graph_options, tearoff=0)
        graph_options.add_cascade(label="Label position",
            menu=vertex_label_position)

        vertexlabelposition_var = self.winfo_name() + ".vertexlabelposition"
        vertex_label_position.add_radiobutton(label="Auto", value="auto",
            variable=vertexlabelposition_var)
        vertex_label_position.add_radiobutton(label="Center", value="center",
            variable=vertexlabelposition_var)

        graph_options.add_command(label="Save graph...",
            command=self.call_graph_save_dialog)

        self.bind("<Destroy>", self.__destroy_menu)

    #noinspection PyUnusedLocal
    def __destroy_menu(self, event):
        try:
            self._menu.delete(self._menu_index)
        except TclError:
            pass

    def call_graph_save_dialog(self):
        file_name = tkFileDialog.asksaveasfilename(defaultextension='.ps',
            filetypes=[('PostScript', '.ps')], parent=self.winfo_toplevel(),
            title="Save graph as image")
        if file_name:
            with codecs.open(file_name, 'w', encoding='utf-8') as file:
                file.write(self._graph_canvas.postscript())


    def update_layout(self):
        try:
            self._iterations_plugin.iterate(50)
        except AttributeError:
            pass





