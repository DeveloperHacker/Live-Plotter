from typing import Union, Iterable

from live_plotter.Graph import Curve, FillGraph
from live_plotter.proxy.Proxy import Proxy
from live_plotter.proxy.ProxyPlotter import ProxyPlotter
from live_plotter.proxy.Task import CreateTask, UpdateTask


class ProxyGraph(Proxy):
    def __init__(self, name: str):
        super().__init__()
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._server.append(UpdateTask(self.id, "set_name", name))
        self._name = name

    def draw(self, plotter: ProxyPlotter):
        self._server.append(UpdateTask(self.id, "draw", plotter.identified))


class ProxyCurve(ProxyGraph):
    @staticmethod
    def _create(mode: str = None, name: str = None) -> Curve:
        from live_plotter.Graph import Curve
        return Curve(mode, name)

    def __init__(self, mode: str = None, name: str = None):
        super().__init__(name)
        self._server.append(CreateTask(self.id, ProxyCurve._create, mode, name))

    def append(self, x: {float, Iterable[float]}, y: {float, Iterable[float]}):
        self._server.append(UpdateTask(self.id, "append", x, y))


class ProxyFillGraph(ProxyGraph):
    @staticmethod
    def _create(mode: str = None, color: str = "blue", alpha: float = 1.0, interpolate: bool = True,
                name: str = None) -> FillGraph:
        from live_plotter.Graph import FillGraph
        return FillGraph(mode, color, alpha, interpolate, name)

    def __init__(self, mode: str = None, color: str = "blue", alpha: float = 1.0, interpolate: bool = True,
                 name: str = None):
        super().__init__(name)
        self._server.append(CreateTask(self.id, ProxyFillGraph._create, mode, color, alpha, interpolate, name))

    def append(
            self, x: Union[float, Iterable[float]], y: Union[float, Iterable[float]],
            delta: Union[float, Iterable[float]]
    ):
        self._server.append(UpdateTask(self.id, "append", x, y, delta))
