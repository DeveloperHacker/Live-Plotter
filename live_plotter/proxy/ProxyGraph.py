from typing import Union, Iterable

from live_plotter.base.Graph import Curve, DistributedCurve, SmoothedCurve
from live_plotter.proxy.Proxy import Proxy
from live_plotter.proxy.ProxyPlotter import ProxyPlotter
from live_plotter.proxy.Task import CreateTask, UpdateTask


class ProxyGraph(Proxy):
    def __init__(self):
        super().__init__()

    def draw(self, plotter: ProxyPlotter):
        self._append_task(UpdateTask(self.id, "draw", plotter.identified))


class ProxyCurve(ProxyGraph):
    @staticmethod
    def _create(mode: str = None) -> Curve:
        from live_plotter.base.Graph import Curve
        return Curve(mode)

    def __init__(self, mode: str = None):
        super().__init__()
        self._append_task(CreateTask(self.id, ProxyCurve._create, mode))

    def append(self, x: {float, Iterable[float]}, y: {float, Iterable[float]}):
        self._append_task(UpdateTask(self.id, "append", x, y))


class ProxySmoothedCurve(ProxyGraph):
    @staticmethod
    def _create(smoothing: float, mode: str = None) -> Curve:
        return SmoothedCurve(smoothing, mode)

    def __init__(self, smoothing: float, mode: str = None):
        super().__init__()
        self._append_task(CreateTask(self.id, ProxySmoothedCurve._create, smoothing, mode))

    def append(self, x: {float, Iterable[float]}, y: {float, Iterable[float]}):
        self._append_task(UpdateTask(self.id, "append", x, y))


class ProxyDistributedCurve(ProxyGraph):
    @staticmethod
    def _create(mode: str = None, color: str = "blue", alpha: float = 1.0,
                interpolate: bool = True) -> DistributedCurve:
        from live_plotter.base.Graph import DistributedCurve
        return DistributedCurve(mode, color, alpha, interpolate)

    def __init__(self, mode: str = None, color: str = "blue", alpha: float = 1.0, interpolate: bool = True):
        super().__init__()
        self._append_task(CreateTask(self.id, ProxyDistributedCurve._create, mode, color, alpha, interpolate))

    def append(self,
               x: Union[float, Iterable[float]], y: Union[float, Iterable[float]],
               delta: Union[float, Iterable[float]]):
        self._append_task(UpdateTask(self.id, "append", x, y, delta))
