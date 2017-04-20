from typing import Union

from live_plotter.Figure import Figure
from live_plotter.proxy.Proxy import Proxy
from live_plotter.proxy.ProxyAxes import ProxyAxes
from live_plotter.proxy.ProxyGraph import ProxyGraph, ProxyFillGraph, ProxyCurve
from live_plotter.proxy.ProxyPlotter import ProxyPlotter
from live_plotter.proxy.Server import Server
from live_plotter.proxy.Task import CreateTask, UpdateTask


class ProxyFigure(Proxy):
    @staticmethod
    def _create(title: Union[int, str] = None) -> Figure:
        from live_plotter.Figure import Figure
        return Figure(title)

    def __init__(self, title: Union[int, str] = None):
        super().__init__()
        self._proxies = {}
        self._server.append(CreateTask(self.id, ProxyFigure._create, title))

    def set_label(self, x: int, y: int, idx: int, label: str):
        self._server.append(UpdateTask(self.id, "set_label", x, y, idx, label))

    def set_x_label(self, x: int, y: int, idx: int, x_label: str):
        self._server.append(UpdateTask(self.id, "set_x_label", x, y, idx, x_label))

    def set_y_label(self, x: int, y: int, idx: int, y_label: str):
        self._server.append(UpdateTask(self.id, "set_y_label", x, y, idx, y_label))

    def set_x_lim(self, x: int, y: int, idx: int, x_lim: (float, float)):
        self._server.append(UpdateTask(self.id, "set_x_lim", x, y, idx, x_lim))

    def set_y_lim(self, x: int, y: int, idx: int, y_lim: (float, float)):
        self._server.append(UpdateTask(self.id, "set_y_lim", x, y, idx, y_lim))

    def get_subplot(self, x: int, y: int, idx: int) -> ProxyPlotter:
        hash_code = Figure.hash(x, y, idx)
        if hash_code in self._proxies:
            axes = self._proxies[hash_code]
            return axes.get_plotter()
        return ProxyPlotter(x, y, idx, self)

    def axes(self, x: int, y: int, idx: int, label: str = None, x_label: str = None, y_label: str = None):
        hash_code = Figure.hash(x, y, idx)
        subplot = self.get_subplot(x, y, idx)
        axes = ProxyAxes(subplot, label, x_label, y_label)
        self._proxies[hash_code] = axes
        self._server.append(UpdateTask(self.id, "append_axes", x, y, idx, axes))
        return axes

    def get_axes(self, x: int, y: int, idx: int) -> ProxyAxes:
        hash_code = Figure.hash(x, y, idx)
        if hash_code not in self._proxies:
            return self.axes(x, y, idx)
        return self._proxies[hash_code]

    def append_axes(self, x: int, y: int, idx: int, axes: ProxyAxes):
        self._server.append(UpdateTask(self.id, "append_axes", x, y, idx, axes.identified))
        self._proxies[Figure.hash(x, y, idx)] = axes

    def append(self, x: int, y: int, idx: int, i_graph: int, *args, **kwargs):
        self._server.append(UpdateTask(self.id, "append", x, y, idx, i_graph, *args, **kwargs))

    def draw(self):
        self._server.append(UpdateTask(self.id, "draw"))

    def flush(self):
        self._server.append(UpdateTask(self.id, "flush"))

    def curve(self, x: int, y: int, idx: int, mode: str = None, name: str = None) -> ProxyCurve:
        curve = ProxyCurve(mode, name)
        self.append_graph(x, y, idx, curve)
        return curve

    def fill_graph(
            self, x: int, y: int, idx: int,
            mode: str = None,
            color: str = "blue",
            alpha: float = 1.0,
            interpolate: bool = True,
            name: str = None
    ) -> ProxyFillGraph:
        curve = ProxyFillGraph(mode, color, alpha, interpolate, name)
        self.append_graph(x, y, idx, curve)
        return curve

    def append_graph(self, x: int, y: int, idx: int, graph: ProxyGraph):
        self._server.append(UpdateTask(self.id, "append_graph", x, y, idx, graph.identified))
        self._proxies[graph.id] = graph

    def save(self, save_path: str):
        self._server.append(UpdateTask(self.id, "save", save_path))

    @staticmethod
    def destroy():
        server = Server()
        server.stop()
