from spectrum.graph.graph import full_graph
from spectrum.gui.main_window import MainWindow

__author__ = 'Daniel Lytkin'

#root = Tk()

graph = full_graph(15)
#graph.add_edge(0, 1)
#graph.add_edge(1, 2)
graph.add_vertex(20)
graph.add_vertex(16)

MainWindow().mainloop()

#window = PanedWindow(root, orient='horizontal', sashrelief="ridge")

#group_select = GroupSelect(window)
#window.add(group_select)

#canvas = GraphViewer(SpringLayout(graph), master=window)
#window.add(canvas)

#window.grid()
#canvas = GraphViewer(CircleLayout(graph, 100, center=(200, 200), width=400, height=400))

#id = None
#
#def e():
#    global id
#    canvas.layout.step(0.1)
#    canvas.reset()
#    id = canvas.after(50, e)
#
#e()
#
##root.rowconfigure(0, weight=1)
#root.columnconfigure(0, weight=1)
#root.grid()
##canvas.grid(row=0, column=1, sticky="nesw")
##canvas.reset()
#
#def stop(event):
#    canvas.after_cancel(id)
#    canvas.layout.reset()
#    canvas.reset()
#
#canvas.bind_all("<space>", stop)

#root.mainloop()
