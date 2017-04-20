import numpy as np

from live_plotter.Figure import Figure

Figure.ion()
figure = Figure("sample-1")
graph1 = figure.curve(1, 2, 1)
graph2 = figure.fill_graph(2, 2, 2, alpha=0.5)
graph3 = figure.curve(2, 2, 4, mode="-g")
graph4 = figure.curve(2, 2, 4, mode="-b")
figure.set_label(1, 2, 1, "sinh")
figure.set_label(2, 2, 2, "fill_sinh")
figure.set_label(2, 2, 4, "sin and cos")
figure.set_x_label(2, 2, 4, "x")
figure.set_y_label(2, 2, 4, "y")
figure.set_x_lim(1, 2, 1, (0, 10))
x = np.arange(0, 2 * np.pi, 0.05)
y1 = np.sinh(x)
y2 = np.sin(x)
y3 = np.cos(x)
for _x, _y1, _y2, _y3 in zip(x, y1, y2, y3):
    graph1.append(_x, _y1)
    graph2.append(_x, _y1, 20)
    graph3.append(_x, _y2)
    graph4.append(_x, _y3)
    figure.draw()
    figure.flush()
figure.show()
figure.save("graph.png")
