from live_plotter.base.Axes import Axes
from live_plotter.proxy.Proxy import Proxy
from live_plotter.proxy.ProxyGraph import ProxyGraph
from live_plotter.proxy.ProxyPlotter import ProxyPlotter
from live_plotter.proxy.Task import UpdateTask, CreateTask


class ProxyAxes(Proxy):
    @staticmethod
    def _create(plotter, label: str, x_label: str, y_label: str) -> Axes:
        from live_plotter.base.Axes import Axes
        return Axes(plotter, label, x_label, y_label)

    def __init__(self, plotter: ProxyPlotter, label: str = None, x_label: str = None, y_label: str = None):
        super().__init__()
        self._plotter = plotter
        self._graphs = []
        self._append_task(CreateTask(self.id, ProxyAxes._create, plotter.identified, label, x_label, y_label))

    def get_plotter(self) -> ProxyPlotter:
        return self._plotter

    def set_label(self, label: str):
        self._append_task(UpdateTask(self.id, "set_label", label))

    def set_x_label(self, x_label: str):
        self._append_task(UpdateTask(self.id, "set_x_label", x_label))

    def set_y_label(self, y_label: str):
        self._append_task(UpdateTask(self.id, "set_y_label", y_label))

    def set_x_lim(self, x_lim: (float, float)):
        self._append_task(UpdateTask(self.id, "set_x_lim", x_lim))

    def set_y_lim(self, y_lim: (float, float)):
        self._append_task(UpdateTask(self.id, "set_y_lim", y_lim))

    def get_graph(self, i_graph: int) -> ProxyGraph:
        return self._graphs[i_graph]

    def append_graph(self, graph: ProxyGraph):
        self._append_task(UpdateTask(self.id, "append_graph", graph.identified))
        self._graphs.append(graph)

    def append(self, i_graph: int, *args, **kwargs):
        self._append_task(UpdateTask(self.id, "append", i_graph, *args, **kwargs))

    def draw(self):
        self._append_task(UpdateTask(self.id, "draw"))

    def clear(self):
        self._append_task(UpdateTask(self.id, "clear"))
