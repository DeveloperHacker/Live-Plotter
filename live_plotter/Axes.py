from live_plotter.Graph import Graph


class Axes:
    def __init__(self, plotter, label: str = None, x_label: str = None, y_label: str = None):
        self._graphs = []
        self._plotter = plotter
        self._label = label
        self._x_label = x_label
        self._y_label = y_label
        self._x_lim = None
        self._y_lim = None
        if self._label is not None:
            self._plotter.set_label(self._label)
        if self._x_label is not None:
            self._plotter.set_xlabel(self._x_label)
        if self._y_label is not None:
            self._plotter.set_ylabel(self._y_label)

    def set_label(self, label: str):
        self._label = label
        self._plotter.set_title(self._label)

    def set_x_label(self, x_label: str):
        self._x_label = x_label
        self._plotter.set_xlabel(self._x_label)

    def set_y_label(self, y_label: str):
        self._y_label = y_label
        self._plotter.set_ylabel(self._y_label)

    def set_x_lim(self, x_lim: (float, float)):
        self._plotter.set_xlim(*x_lim)
        self._x_lim = x_lim

    def set_y_lim(self, y_lim: (float, float)):
        self._plotter.set_ylim(*y_lim)
        self._y_lim = y_lim

    def get_graph(self, i_graph: int) -> Graph:
        return self._graphs[i_graph]

    def append_graph(self, graph: Graph):
        self._graphs.append(graph)

    def append(self, i_graph: int, *args, **kwargs):
        graph = self.get_graph(i_graph)
        graph.append(*args, **kwargs)

    def draw(self):
        lim = self._plotter.viewLim
        if self._x_lim is not None:
            x_lim = (lim.x0, lim.x1)
            x0 = min(*x_lim, *self._x_lim)
            x1 = max(*x_lim, *self._x_lim)
            self.set_x_lim((x0, x1))
        if self._y_lim is not None:
            y_lim = (lim.y0, lim.y1)
            y0 = min(*y_lim, *self._y_lim)
            y1 = max(*y_lim, *self._y_lim)
            self.set_y_lim((y0, y1))
        if self._label:
            self.set_label(self._label)
        if self._x_label:
            self.set_x_label(self._x_label)
        if self._y_label:
            self.set_y_label(self._y_label)
        for graph in self._graphs:
            graph.draw(self._plotter)

    def clear(self):
        self._plotter.clear()
