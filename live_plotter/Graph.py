from abc import ABCMeta, abstractmethod

import numpy as np
from typing import Iterable, Union


class Graph(metaclass=ABCMeta):
    class NotEqualsLengthsError(ValueError):
        pass

    def __init__(self, name: str = None):
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name

    @abstractmethod
    def draw(self, plotter):
        pass

    @abstractmethod
    def append(self, *args, **kwargs):
        pass


class Curve(Graph):
    def __init__(self, mode: str = None, name: str = None):
        super().__init__(name)
        self._mode = "-or" if mode is None else mode
        self._xes = []
        self._yes = []

    def append(self, x: {float, Iterable[float]}, y: {float, Iterable[float]}):
        if not isinstance(x, Iterable):
            x = (x,)
        if not isinstance(y, Iterable):
            y = (y,)
        if len(x) != len(y):
            raise Graph.NotEqualsLengthsError()
        self._xes.extend(x)
        self._yes.extend(y)

    def draw(self, plotter):
        plotter.plot(self._xes, self._yes, self._mode)


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

    def draw(self, plotter):
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
        plotter.plot(self._xes, self._yes, self._mode)
