from Tkinter import Frame, PanedWindow, Button, Menu, StringVar, Toplevel
from spectrum.gui.facade_frame import Facade
from spectrum.gui.group_select import GroupSelect
from spectrum.gui.gui_elements import FrameWithCloseButton, CheckBox
from spectrum.tools.tools import properties

__author__ = 'Daniel Lytkin'

class MainWindow(Frame):
    def __init__(self, **kw):
        Frame.__init__(self, **kw)
        self.winfo_toplevel().minsize(width=800, height=480)
        self.pack(expand=True, fill='both')
        self._init_properties()
        self._init_components()


    def _init_components(self):
        self._panes = PanedWindow(self, orient='horizontal',
            sashrelief="raised")
        self._panes.pack(expand=True, fill='both')

        self._left_pane = Frame(self._panes)
        self._right_pane = PanedWindow(self._panes)
        self._panes.add(self._left_pane, sticky='n')
        self._panes.add(self._right_pane)

        self._group_select = GroupSelect(self._left_pane)
        self._group_select.pack(expand=True, fill='x')

        self._show_graph_checkbutton = CheckBox(self._left_pane,
            text='Show graph')
        self._show_graph_checkbutton.select()
        self._show_graph_checkbutton.pack()

        self._go_button = Button(self._left_pane, text='Go', command=self._go)
        self._go_button.pack()

        self._init_menu()


    def _init_menu(self):
        toplevel = self.winfo_toplevel()
        self._menu = Menu(toplevel)
        toplevel['menu'] = self._menu

        view = Menu(self._menu, tearoff=0)
        self._menu.add_cascade(label="View", menu=view)

        graph_view = Menu(view, tearoff=0)
        view.add_cascade(label="View graphs", menu=graph_view)

        graph_view_var = properties.get_variable("graphframeview")
        graph_view.add_radiobutton(label="Only one", value="onlyone",
            variable=graph_view_var)
        graph_view.add_radiobutton(label="In a row", value="row",
            variable=graph_view_var)
        graph_view.add_radiobutton(label="In separate window", value="window",
            variable=graph_view_var)


    def _init_properties(self):
        properties.add_variable("graphframeview", StringVar(),
            initial="onlyone")


    def _go(self):
        view = properties["graphframeview"]

        if view == "onlyone":
            for child in self._right_pane.winfo_children():
                child.destroy()
        if view in ("onlyone", "row"):
            container = FrameWithCloseButton(self._right_pane)
            self._right_pane.add(container, minsize=600)
        else:
            container = Toplevel()

        facade = Facade(container, self._group_select.selected_group,
            show_graph=self._show_graph_checkbutton.is_selected())

        facade.pack(expand=True, fill='both')












