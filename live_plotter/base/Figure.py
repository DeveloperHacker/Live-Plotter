from typing import Union

import matplotlib.pyplot as pl

from live_plotter.base.Axes import Axes
from live_plotter.base.Graph import Graph, Curve, DistributedCurve, SmoothedCurve


class Figure:
    _ion = False

    def __init__(self, title: Union[int, str] = None, save_path: str = None):
        self._title = title
        self._save_path = save_path
        self._figure = pl.figure(title)
        self._axes = {}

    def set_label(self, width: int, height: int, idx: int, label: str):
        hash_code = Figure.hash(width, height, idx)
        self._axes[hash_code].set_label(label)

    def set_x_label(self, width: int, height: int, idx: int, x_label: str):
        hash_code = Figure.hash(width, height, idx)
        self._axes[hash_code].set_x_label(x_label)

    def set_y_label(self, width: int, height: int, idx: int, y_label: str):
        hash_code = Figure.hash(width, height, idx)
        self._axes[hash_code].set_y_label(y_label)

    def set_x_lim(self, width: int, height: int, idx: int, x_lim: (float, float)):
        self.get_axes(width, height, idx).set_x_lim(x_lim)

    def set_y_lim(self, width: int, height: int, idx: int, y_lim: (float, float)):
        self.get_axes(width, height, idx).set_y_lim(y_lim)

    def get_subplot(self, width: int, height: int, idx: int):
        return self._figure.add_subplot(width, height, idx)

    def axes(self, width: int, height: int, idx: int, label: str = None, x_label: str = None,
             y_label: str = None) -> Axes:
        subplot = self.get_subplot(width, height, idx)
        axes = Axes(subplot, label, x_label, y_label)
        self.append_axes(width, height, idx, axes)
        return axes

    def get_axes(self, width: int, height: int, idx: int) -> Axes:
        hash_code = Figure.hash(width, height, idx)
        if hash_code not in self._axes:
            subplot = self.get_subplot(width, height, idx)
            self._axes[hash_code] = Axes(subplot)
        return self._axes[hash_code]

    def append_axes(self, width: int, height: int, idx: int, axes: Axes):
        hash_code = Figure.hash(width, height, idx)
        self._axes[hash_code] = axes

    def append(self, width: int, height: int, idx: int, i_graph: int, *args, **kwargs):
        axes = self.get_axes(width, height, idx)
        axes.append(i_graph, *args, **kwargs)

    def draw(self):
        for axes in self._axes.values():
            axes.clear()
            axes.draw()
        self.flush()

    def flush(self):
        self._figure.canvas.flush_events()

    def curve(self, width: int, height: int, idx: int, mode: str = None) -> Curve:
        graph = Curve(mode)
        self.append_graph(width, height, idx, graph)
        return graph

    def smoothed_curve(self,
                       width: int, height: int, idx: int,
                       smoothing: float,
                       mode: str = None) -> SmoothedCurve:
        graph = SmoothedCurve(smoothing, mode)
        self.append_graph(width, height, idx, graph)
        return graph

    def distributed_curve(self,
                          width: int, height: int, idx: int,
                          mode: str = None,
                          color: str = "blue",
                          alpha: float = 1.0,
                          interpolate: bool = True) -> DistributedCurve:
        graph = DistributedCurve(mode, color, alpha, interpolate)
        self.append_graph(width, height, idx, graph)
        return graph

    def append_graph(self, width: int, height: int, idx: int, graph: Graph):
        axes = self.get_axes(width, height, idx)
        axes.append_graph(graph)

    def save(self, save_path: str = None):
        save_path = save_path or self._save_path
        if save_path is not None:
            ion = Figure._ion
            if ion:
                Figure.ioff()
            self._figure.savefig(save_path)
            if ion:
                Figure.ion()

    def close(self):
        self.draw()
        self.save()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def hash(width: int, height: int, idx: int) -> str:
        return "_".join((str(width), str(height), str(idx)))

    @staticmethod
    def ion():
        if not Figure._ion:
            Figure._ion = True
            pl.ion()

    @staticmethod
    def ioff():
        if Figure._ion:
            Figure._ion = False
            pl.ioff()

    @staticmethod
    def show():
        Figure.ioff()
        pl.show()
