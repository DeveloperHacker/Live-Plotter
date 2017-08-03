import numpy as np

from live_plotter.proxy.ProxyFigure import ProxyFigure

figure2 = ProxyFigure("sample-2", "proxy-plotting-figure2.png")
figure1 = ProxyFigure("sample-1", "proxy-plotting-figure1.png")
with figure1, figure2:
    graph1 = figure1.curve(1, 2, 1)
    graph2 = figure1.distributed_curve(2, 2, 2, alpha=0.5)
    graph3 = figure1.curve(2, 2, 4, mode="-g")
    graph4 = figure1.curve(2, 2, 4, mode="-b")
    figure2.append_graph(1, 1, 1, graph3)
    figure2.append_graph(1, 1, 1, graph4)
    figure1.set_label(1, 2, 1, "sinh")
    figure1.set_label(2, 2, 2, "fill_sinh")
    figure1.set_label(2, 2, 4, "sin and cos")
    figure1.set_x_label(2, 2, 4, "x")
    figure1.set_y_label(2, 2, 4, "y")
    figure1.set_x_lim(1, 2, 1, (0, 10))
    x = np.linspace(0, 2 * np.pi, 200)
    y1 = np.sinh(x)
    y2 = np.sin(x)
    y3 = np.cos(x)
    for _x, _y1, _y2, _y3 in zip(x, y1, y2, y3):
        graph1.append(_x, _y1)
        graph2.append(_x, _y1, 20)
        graph3.append(_x, _y2)
        graph4.append(_x, _y3)
        figure1.draw()
        figure2.draw()
