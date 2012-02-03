from calculations.graph import Graph
from graph.drawing import GraphViewer
from graph.layout import RandomLayout

__author__ = 'Daniel Lytkin'

from Tkinter import *

root = Tk()
frame = Frame(master=root)
frame.pack()

graph = Graph()
graph.addVertices(range(10))
graph.addEdge(0, 1)

canvas = GraphViewer(RandomLayout(graph))
canvas.pack()
frame.mainloop()

