from Tkinter import Frame, PanedWindow, Button
from spectrum.gui.facade_frame import Facade
from spectrum.gui.group_select import GroupSelect
from spectrum.gui.gui_elements import FrameWithCloseButton

__author__ = 'Daniel Lytkin'

class MainWindow(Frame):
    def __init__(self, **kw):
        Frame.__init__(self, **kw)
        self.winfo_toplevel().minsize(width=600, height=400)
        self.pack(expand=True, fill='both')
        self.init_components()


    def init_components(self):
        self._panes = PanedWindow(self, orient='horizontal',
            sashrelief="raised")
        self._panes.pack(expand=True, fill='both')

        self._left_pane = Frame(self._panes)
        self._right_pane = Frame(self._panes)
        self._panes.add(self._left_pane, sticky='n')
        self._panes.add(self._right_pane)

        self._group_select = GroupSelect(self._left_pane)
        self._group_select.pack(expand=True, fill='x')

        self._go_button = Button(self._left_pane, text='Go', command=self._go)
        self._go_button.pack()


    def _go(self):
        facade_pane = FrameWithCloseButton(self._right_pane)
        facade_pane.pack(expand=True, fill='both')

        facade = Facade(facade_pane, self._group_select.selected_group)
        facade.pack(expand=True, fill='both')






