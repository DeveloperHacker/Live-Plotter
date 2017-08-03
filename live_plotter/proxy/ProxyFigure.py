from typing import Union

from live_plotter.base.Figure import Figure
from live_plotter.proxy.Proxy import Proxy
from live_plotter.proxy.ProxyAxes import ProxyAxes
from live_plotter.proxy.ProxyGraph import ProxyGraph, ProxyDistributedCurve, ProxyCurve, ProxySmoothedCurve
from live_plotter.proxy.ProxyPlotter import ProxyPlotter
from live_plotter.proxy.Server import Server
from live_plotter.proxy.Task import CreateTask, UpdateTask, DestroyTask


class ProxyFigure(Proxy):
    @staticmethod
    def _create(title: Union[int, str], save_path: str) -> Figure:
        from live_plotter.base.Figure import Figure
        Figure.ion()
        return Figure(title, save_path)

    def __init__(self, title: Union[int, str] = None, save_path: str = None):
        super().__init__()
        self._proxies = {}
        self._append_task(CreateTask(self.id, ProxyFigure._create, title, save_path))
        self._title = title

    def get_title(self):
        return self._title

    def set_label(self, width: int, height: int, idx: int, label: str):
        self._append_task(UpdateTask(self.id, "set_label", width, height, idx, label))

    def set_x_label(self, width: int, height: int, idx: int, x_label: str):
        self._append_task(UpdateTask(self.id, "set_x_label", width, height, idx, x_label))

    def set_y_label(self, width: int, height: int, idx: int, y_label: str):
        self._append_task(UpdateTask(self.id, "set_y_label", width, height, idx, y_label))

    def set_x_lim(self, width: int, height: int, idx: int, x_lim: (float, float)):
        self._append_task(UpdateTask(self.id, "set_x_lim", width, height, idx, x_lim))

    def set_y_lim(self, width: int, height: int, idx: int, y_lim: (float, float)):
        self._append_task(UpdateTask(self.id, "set_y_lim", width, height, idx, y_lim))

    def get_subplot(self, width: int, height: int, idx: int) -> ProxyPlotter:
        hash_code = Figure.hash(width, height, idx)
        if hash_code in self._proxies:
            axes = self._proxies[hash_code]
            return axes.get_plotter()
        return ProxyPlotter(width, height, idx, self)

    def axes(self, width: int, height: int, idx: int, label: str = None, x_label: str = None, y_label: str = None):
        hash_code = Figure.hash(width, height, idx)
        subplot = self.get_subplot(width, height, idx)
        axes = ProxyAxes(subplot, label, x_label, y_label)
        self._proxies[hash_code] = axes
        self._append_task(UpdateTask(self.id, "append_axes", width, height, idx, axes))
        return axes

    def get_axes(self, width: int, height: int, idx: int) -> ProxyAxes:
        hash_code = Figure.hash(width, height, idx)
        if hash_code not in self._proxies:
            return self.axes(width, height, idx)
        return self._proxies[hash_code]

    def append_axes(self, width: int, height: int, idx: int, axes: ProxyAxes):
        self._append_task(UpdateTask(self.id, "append_axes", width, height, idx, axes.identified))
        self._proxies[Figure.hash(width, height, idx)] = axes

    def append(self, width: int, height: int, idx: int, i_graph: int, *args, **kwargs):
        self._append_task(UpdateTask(self.id, "append", width, height, idx, i_graph, *args, **kwargs))

    def draw(self):
        self._append_task(UpdateTask(self.id, "draw"))

    def flush(self):
        self._append_task(UpdateTask(self.id, "flush"))

    def curve(self, width: int, height: int, idx: int, mode: str = None) -> ProxyCurve:
        curve = ProxyCurve(mode)
        self.append_graph(width, height, idx, curve)
        return curve

    def smoothed_curve(self,
                       width: int, height: int, idx: int,
                       smoothing: float,
                       mode: str = None) -> ProxySmoothedCurve:
        curve = ProxySmoothedCurve(smoothing, mode)
        self.append_graph(width, height, idx, curve)
        return curve

    def distributed_curve(self,
                          width: int, height: int, idx: int,
                          mode: str = None,
                          color: str = "blue",
                          alpha: float = 1.0,
                          interpolate: bool = True) -> ProxyDistributedCurve:
        curve = ProxyDistributedCurve(mode, color, alpha, interpolate)
        self.append_graph(width, height, idx, curve)
        return curve

    def append_graph(self, width: int, height: int, idx: int, graph: ProxyGraph):
        self._append_task(UpdateTask(self.id, "append_graph", width, height, idx, graph.identified))
        self._proxies[graph.id] = graph

    def save(self, save_path: str = None):
        self._append_task(UpdateTask(self.id, "save", save_path))

    def close(self):
        self._append_task(UpdateTask(self.id, "close"))
        self._append_task(DestroyTask(self.id))
        for proxy in self._proxies.values():
            self._append_task(DestroyTask(proxy.id))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def destroy():
        Server().stop()
