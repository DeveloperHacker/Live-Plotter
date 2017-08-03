import numpy as np

from live_plotter.proxy.ProxyFigure import ProxyFigure

with ProxyFigure("sample", "smoothed-plotting-figure.png") as figure:
    graph1 = figure.curve(1, 1, 1, "-r")
    graph2 = figure.smoothed_curve(1, 1, 1, 0.99, "-g")
    figure.set_label(1, 1, 1, "Smoothed normal distributed values")
    figure.set_x_label(1, 1, 1, "time")
    figure.set_y_label(1, 1, 1, "value")
    for time in range(200):
        value = np.random.normal(10, 15)
        graph1.append(time, value)
        graph2.append(time, value)
        figure.draw()
