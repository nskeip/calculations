from spectrum.graph.drawing import GraphViewer
from spectrum.graph.graph import  FullGraph
from spectrum.graph.layout import  SpringLayout

__author__ = 'Daniel Lytkin'

from Tkinter import *

root = Tk()
frame = Frame(master=root)
frame.pack()

graph = FullGraph(15)
#graph.add_edge(0, 1)
#graph.add_edge(1, 2)


canvas = GraphViewer(SpringLayout(graph))

id = None

def e():
    global id
    canvas.layout.step(0.1)
    canvas.reset()
    id = frame.after(50, e)

e()

def stop(event):
    frame.after_cancel(id)

canvas.bind_all("<space>", stop)

canvas.pack()
frame.mainloop()

