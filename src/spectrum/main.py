from spectrum.graph.drawing import GraphViewer
from spectrum.graph.graph import full_graph
from spectrum.graph.layout import CircleLayout

__author__ = 'Daniel Lytkin'

from Tkinter import *

root = Tk()
frame = Frame(master=root)
frame.pack()

graph = full_graph(15)
#graph.add_edge(0, 1)
#graph.add_edge(1, 2)
graph.add_vertex(20)

canvas = GraphViewer(CircleLayout(graph, 0.3))

id = None

def e():
    global id
    canvas.layout.step(0.1)
    canvas.reset()
    id = frame.after(50, e)

# e()

def stop(event):
    frame.after_cancel(id)

canvas.bind_all("<space>", stop)

canvas.pack()
frame.mainloop()

