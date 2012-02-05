from spectrum.graph.drawing import GraphViewer
from spectrum.graph.graph import Graph, FullGraph
from spectrum.graph.layout import RandomLayout

__author__ = 'Daniel Lytkin'

from Tkinter import *

root = Tk()
frame = Frame(master=root)
frame.pack()

graph = FullGraph(5)
#graph.add_vertices(range(10))
#graph.add_edge(0, 1)

canvas = GraphViewer(RandomLayout(graph))
canvas.pack()
frame.mainloop()

