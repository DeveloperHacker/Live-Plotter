from live_plotter.Figure import Figure

from live_plotter.proxy.Proxy import Proxy
from live_plotter.proxy.Task import CreateTask


class ProxyPlotter(Proxy):
    @staticmethod
    def _create(x, y, idx, figure: Figure):
        return figure.get_subplot(x, y, idx)

    def __init__(self, x: int, y: int, idx: int, figure: 'ProxyFigure'):
        super().__init__()
        self._server.append(CreateTask(self.id, ProxyPlotter._create, x, y, idx, figure.identified))
