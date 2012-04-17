from Tkinter import Frame, PanedWindow, Button, Menu, StringVar, Toplevel
from spectrum.gui.facade_frame import Facade
from spectrum.gui.group_select import GroupSelect
from spectrum.gui.gui_elements import FrameWithCloseButton
from spectrum.tools.tools import Properties

__author__ = 'Daniel Lytkin'

class MainWindow(Frame):
    def __init__(self, **kw):
        Frame.__init__(self, **kw)
        self.winfo_toplevel().minsize(width=600, height=400)
        self.pack(expand=True, fill='both')
        self._init_properties()
        self._init_components()

    @property
    def properties(self):
        """Returns Properties instance: a dict that can contain both regular
        entries and Tkinter Variables
        """
        return self._properties

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

        graph_view_var = self._properties.get_variable("graphframeview")
        graph_view.add_radiobutton(label="Only one", value="onlyone",
            variable=graph_view_var)
        graph_view.add_radiobutton(label="In a row", value="row",
            variable=graph_view_var)
        graph_view.add_radiobutton(label="In separate window", value="window",
            variable=graph_view_var)


    def _init_properties(self):
        self._properties = Properties()
        self._properties.add_variable("graphframeview", StringVar(),
            initial="onlyone")


    def _go(self):
        view = self._properties["graphframeview"]
        if view == "onlyone":
            for child in self._right_pane.winfo_children():
                child.destroy()
            container = FrameWithCloseButton(self._right_pane)
            self._right_pane.add(container, minsize=600)
        elif view == "row":
            container = FrameWithCloseButton(self._right_pane)
            self._right_pane.add(container, minsize=600)
        else: # view == "window":
            container = Toplevel()

        facade = Facade(container, self._group_select.selected_group)
        w = facade.winfo_reqwidth()
        h = facade.winfo_reqheight()

        if isinstance(container, Toplevel):
            pass
        else:
            self._right_pane.paneconfig(container, width=600, height=100)
            #container.config(width=600, height=100)
        facade.pack(expand=True, fill='both')
        facade.update_layout()












