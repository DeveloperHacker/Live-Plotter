import numpy as np

from live_plotter.Figure import Figure

Figure.ion()
figure = Figure()
graph1 = figure.curve(1, 2, 1)
graph2 = figure.fill_graph(2, 2, 2, alpha=0.5)
graph3 = figure.curve(2, 2, 4, mode="-g")
graph4 = figure.curve(2, 2, 4, mode="-b")
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
figure.show()
figure.save("graph.png")
