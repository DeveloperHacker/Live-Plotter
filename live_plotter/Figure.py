from abc import abstractmethod, ABCMeta
from typing import Union, Iterable

import matplotlib.pyplot as pl
import numpy as np


class Graph(metaclass=ABCMeta):
    class NotEqualsLengthsError(ValueError):
        pass

    def __init__(self, name: str = None):
        self._name = name

    def get_name(self):
        return self._name

    @abstractmethod
    def draw(self, plotter, to_legend: bool):
        pass


class Curve(Graph):
    def __init__(self, mode: str = None, name: str = None):
        super().__init__(name)
        self._mode = "-or" if mode is None else mode
        self._xes = []
        self._yes = []
        self._legend = False

    def append(self, x: {float, Iterable[float]}, y: {float, Iterable[float]}):
        if not isinstance(x, Iterable):
            x = (x,)
        if not isinstance(y, Iterable):
            y = (y,)
        if len(x) != len(y):
            raise Graph.NotEqualsLengthsError()
        self._xes.extend(x)
        self._yes.extend(y)

    def draw(self, plotter, to_legend: bool):
        inst = plotter.plot(self._xes, self._yes, self._mode)
        if not self._legend and to_legend:
            plotter.legend([inst], [self.get_name()])
            self._legend = True


class FillGraph(Graph):
    def __init__(
            self,
            mode: str = None,
            color: str = "blue",
            alpha: float = 1.0,
            interpolate: bool = True,
            name: str = None
    ):
        super().__init__(name)
        self._color = color
        self._alpha = alpha
        self._interpolate = interpolate
        self._xes = []
        self._yes = []
        self._deltas = []
        self._mode = "-or" if mode is None else mode
        self._legend = False

    def append(
            self, x: Union[float, Iterable[float]], y: Union[float, Iterable[float]],
            delta: Union[float, Iterable[float]]
    ):
        if not isinstance(x, Iterable):
            x = (x,)
        if not isinstance(y, Iterable):
            y = (y,)
        if not isinstance(delta, Iterable):
            delta = (delta,)
        if len(x) != len(y) and len(y) != len(delta):
            raise Graph.NotEqualsLengthsError()
        self._xes.extend(x)
        self._yes.extend(y)
        self._deltas.extend(delta)

    def draw(self, plotter, to_legend: bool):
        yes = np.asarray(self._yes)
        deltas = np.asarray(self._deltas)
        plotter.fill_between(
            self._xes,
            yes - deltas,
            yes + deltas,
            alpha=self._alpha,
            facecolor=self._color,
            interpolate=self._interpolate
        )
        inst = plotter.plot(self._xes, self._yes, self._mode)
        if not self._legend and to_legend:
            plotter.legend([inst], [self.get_name()])
            self._legend = True


class Axes:
    def __init__(self, plotter, name: str = None):
        self._graphs = []
        self._plotter = plotter
        self._title = name
        self._x_lim = None
        self._y_lim = None
        if self._title is not None:
            self._plotter.title(self._title)

    def set_title(self, title: str):
        self._title = title
        self._plotter.title(self._title)

    def set_x_lim(self, x_lim: (float, float)):
        self._plotter.set_xlim(*x_lim)
        self._x_lim = x_lim

    def set_y_lim(self, y_lim: (float, float)):
        self._plotter.set_ylim(*y_lim)
        self._y_lim = y_lim

    def get_graph(self, i_graph: int):
        return self._graphs[i_graph]

    def append_graph(self, graph: Graph, to_legend: bool = False):
        self._graphs.append((graph, to_legend))

    def append(self, i_graph: int, *args, **kwargs):
        graph = self.get_graph(i_graph)
        graph.append(*args, **kwargs)

    def draw(self):
        for graph, to_legend in self._graphs:
            graph.draw(self._plotter, to_legend)
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

    def clear(self):
        self._plotter.clear()


class Figure:
    _ion = False

    def __init__(self, number: int = None):
        self._figure = pl.figure(number)
        self._axes = {}

    def set_title(self, x: int, y: int, idx: int, title: str):
        hash_code = Figure.hash(x, y, idx)
        self._axes[hash_code].set_title(title)

    def set_x_lim(self, x: int, y: int, idx: int, x_lim: (float, float)):
        self.get_axes(x, y, idx).set_x_lim(x_lim)

    def set_y_lim(self, x: int, y: int, idx: int, y_lim: (float, float)):
        self.get_axes(x, y, idx).set_y_lim(y_lim)

    def get_axes(self, x: int, y: int, idx: int) -> Axes:
        hash_code = Figure.hash(x, y, idx)
        return self._axes[hash_code]

    def append_axes(self, x: int, y: int, idx: int, axes: Axes):
        hash_code = Figure.hash(x, y, idx)
        self._axes[hash_code] = axes

    def append(self, x: int, y: int, idx: int, i_graph: int, *args, **kwargs):
        axes = self.get_axes(x, y, idx)
        axes.append(i_graph, *args, **kwargs)

    def draw(self):
        for axes in self._axes.values():
            axes.clear()
            axes.draw()
        self.flush()

    def flush(self):
        self._figure.canvas.flush_events()

    def curve(self, x: int, y: int, idx: int, mode: str = None, name: str = None) -> Curve:
        graph = Curve(mode, name)
        self.append_graph(x, y, idx, graph)
        return graph

    def fill_graph(
            self, x: int, y: int, idx: int,
            mode: str = None,
            color: str = "blue",
            alpha: float = 1.0,
            interpolate: bool = True,
            name: str = None
    ) -> FillGraph:
        graph = FillGraph(mode, color, alpha, interpolate, name)
        self.append_graph(x, y, idx, graph)
        return graph

    def append_graph(self, x: int, y: int, idx: int, graph: Graph):
        hash_code = Figure.hash(x, y, idx)
        if hash_code not in self._axes:
            self._axes[hash_code] = Axes(self._figure.add_subplot(x, y, idx))
        axes = self._axes[hash_code]
        axes.append_graph(graph)

    def save(self, save_path: str):
        ion = Figure._ion
        if ion:
            Figure.ioff()
        self._figure.savefig(save_path)
        if ion:
            Figure.ion()

    @staticmethod
    def hash(x: int, y: int, idx: int) -> str:
        return "_".join((str(x), str(y), str(idx)))

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