from spectrum.graph.drawing import GraphViewer
from spectrum.graph.graph import  FullGraph
from spectrum.graph.layout import CircleLayout

__author__ = 'Daniel Lytkin'

from Tkinter import *

root = Tk()
frame = Frame(master=root)
frame.pack()

graph = FullGraph(5)
graph.add_vertices(range(6, 10))
graph.add_edge(5, 7)
graph.add_edge(5, 8)
#graph.add_edge(0, 1)


canvas = GraphViewer(CircleLayout(graph, 0.5, 0.5, 0.25))
canvas.pack()
frame.mainloop()

