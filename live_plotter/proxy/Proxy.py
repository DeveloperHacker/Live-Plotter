from live_plotter.proxy.Identified import Identified
from live_plotter.proxy.Server import Server


class Proxy(Identified):
    def __init__(self):
        self._server = Server()
        super().__init__(self._server.get_uid())
        self.identified = Identified(self.id)
