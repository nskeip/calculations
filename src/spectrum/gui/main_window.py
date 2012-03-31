from Tkinter import Frame, PanedWindow, Button
from spectrum.gui.group_select import GroupSelect
from spectrum.gui.gui_elements import GraphContainer, ApexListContainer, CheckBox

__author__ = 'Daniel Lytkin'

class MainWindow(Frame):
    def __init__(self, **kw):
        Frame.__init__(self, **kw)
        self.winfo_toplevel().minsize(width=600, height=400)
        self.grid(sticky="nesw")
        #self.grid_propagate(0)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.init_components()


    def init_components(self):
        self._panes = PanedWindow(self, orient='horizontal',
            sashrelief="raised")
        self._panes.grid(sticky="nesw")

        self._group_select_pane = Frame(self._panes)
        self._panes.add(self._group_select_pane)

        self._graph_container_pane = Frame(self._panes)
        self._panes.add(self._graph_container_pane)

        self._group_select_pane.columnconfigure(0, weight=1)
        self._group_select = GroupSelect(self._group_select_pane)
        self._group_select.grid(sticky="nwe")

        #self.show_apex()

        self._group_buttons_pane = Frame(self._group_select_pane)
        self._group_buttons_pane.grid(sticky="nesw")

        show_graph = CheckBox(self._group_buttons_pane, text="Show graph")
        show_graph.grid()

        button = Button(self._group_buttons_pane, text="GO",
            command=self.show_apex)
        button.grid()

        self._graph_container_pane.columnconfigure(0, weight=1)
        graph_container = GraphContainer(self._graph_container_pane)
        graph_container.grid(sticky="nesw")


    def show_apex(self):
        apex = self._group_select.selected_group.apex()
        self._apex_container_pane = Frame(self._panes)
        self._panes.add(self._apex_container_pane,
            after=self._group_select_pane,
            padx=5, pady=5)

        self._apex_container_pane.columnconfigure(0, weight=1)

        self._apex_container = ApexListContainer(self._apex_container_pane)
        self._apex_container.grid(sticky="nesw")
        self._apex_container.apex_list.set_apex(apex)




