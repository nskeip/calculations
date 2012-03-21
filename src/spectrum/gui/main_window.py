from Tkinter import Frame, PanedWindow
from spectrum.gui.group_select import GroupSelect

__author__ = 'Daniel Lytkin'

class MainWindow(Frame):
    def __init__(self, parent=None, **kw):
        #parent = parent or Tk()
        Frame.__init__(self, parent, **kw)
        self.grid(sticky="nesw")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.init_components()


    def init_components(self):
        panes = PanedWindow(self, orient='horizontal', sashrelief="ridge")
        panes.grid(sticky="nesw")

        left_pane = Frame(panes)
        panes.add(left_pane)

        right_pane = Frame(panes)
        panes.add(right_pane, width=400)

        left_pane.columnconfigure(0, weight=1)
        self._group_select = GroupSelect(left_pane)
        self._group_select.grid(sticky="nwe")






