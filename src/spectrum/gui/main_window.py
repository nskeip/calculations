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
from Tkinter import Frame, PanedWindow, Button, Menu, Toplevel, LabelFrame, Label
from collections import OrderedDict

from spectrum.calculations import graphs
from spectrum.gui.facade_frame import Facade
from spectrum.gui.group_select import GroupSelect
from spectrum.gui.gui_elements import FrameWithCloseButton, CheckBox, OptionList

__author__ = 'Daniel Lytkin'


class MainWindow(Frame):
    GRAPH_TYPES = OrderedDict([
        ("Prime Graph", graphs.PrimeGraph),
        ("Fast Graph", graphs.FastGraph)
    ])

    def __init__(self, **kw):
        Frame.__init__(self, **kw)
        self.winfo_toplevel().minsize(width=600, height=400)
        width = min(self.winfo_screenwidth(), 1280)
        height = min(self.winfo_screenheight(), 720)
        self.winfo_toplevel().geometry("{}x{}".format(width, height))
        self.pack(expand=True, fill='both')
        self._init_variables()
        self._init_components()
        self._init_menu()

    def _init_components(self):
        self._panes = PanedWindow(self, orient='horizontal', sashrelief="raised")
        self._panes.pack(expand=True, fill='both')

        self._left_pane = Frame(self._panes, padx=10, pady=5)
        self._right_pane = PanedWindow(self._panes)
        self._panes.add(self._left_pane, sticky='n')
        self._panes.add(self._right_pane)

        self._group_select = GroupSelect(self._left_pane)
        self._group_select.pack(expand=True, fill='x')

        # spacer
        Frame(self._left_pane, height=10).pack()

        graph_controls = LabelFrame(self._left_pane, text="Graph options", padx=10, pady=5)
        graph_controls.columnconfigure(1, weight=1)
        graph_controls.pack(expand=True, fill='x')

        self._show_graph_checkbutton = CheckBox(graph_controls, text='Show graph')
        self._show_graph_checkbutton.select()
        self._show_graph_checkbutton.grid(row=0, columnspan=2, sticky='w')

        Label(graph_controls, text='Algorithm').grid(row=1, sticky='w')
        self._graph_type = OptionList(graph_controls, values=MainWindow.GRAPH_TYPES.keys())
        self._graph_type.config(width=15)
        self._graph_type.grid(row=1, column=1, sticky='we')

        # spacer
        Frame(self._left_pane, height=10).pack()

        self._go_button = Button(self._left_pane, text='Go', command=self._go)
        self._go_button.pack()

    def _init_variables(self):
        # init default properties
        self.setvar("graphframeview", "onlyone")
        self.setvar("vertexlabelposition", "auto")

    def _init_menu(self):
        toplevel = self.winfo_toplevel()
        self._menu = Menu(toplevel)
        toplevel['menu'] = self._menu

        view = Menu(self._menu, tearoff=0)
        self._menu.add_cascade(label="View", menu=view)

        graph_view = Menu(view, tearoff=0)
        view.add_cascade(label="View graphs", menu=graph_view)

        graph_view.add_radiobutton(variable="graphframeview", label="Only one", value="onlyone")
        #        graph_view.add_radiobutton(label="In a row", value="row",
        #            variable=graph_view_var)
        graph_view.add_radiobutton(variable="graphframeview", label="In separate window", value="window")

    def _go(self):
        view = self.getvar("graphframeview")

        if view == "onlyone":
            for child in self._right_pane.winfo_children():
                child.destroy()
                #if view in ("onlyone", "row"):
            container = FrameWithCloseButton(self._right_pane)
            self._right_pane.add(container, minsize=600)
        else:
            container = Toplevel()

        graph_class = MainWindow.GRAPH_TYPES[self._graph_type.variable.get()]

        facade = Facade(container, self._group_select.selected_group,
                        show_graph=self._show_graph_checkbutton.is_selected(),
                        graph_class=graph_class)

        facade.pack(expand=True, fill='both')