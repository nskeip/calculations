from spectrum.graph.drawing import GraphViewer
from spectrum.graph.graph import  FullGraph
from spectrum.graph.layout import  SpringLayout

__author__ = 'Daniel Lytkin'

from Tkinter import *

root = Tk()
frame = Frame(master=root)
frame.pack()

graph = FullGraph(16)
#graph.add_edge(0, 1)
#graph.add_edge(1, 2)


canvas = GraphViewer(SpringLayout(graph))

def e(event):
    canvas.layout.step(0.1)
    canvas.reset()

canvas.bind_all("<space>", e)

canvas.pack()
frame.mainloop()

