from live_plotter.proxy.Identified import Identified
from live_plotter.proxy.Server import Server
from live_plotter.proxy.Task import Task


class Proxy(Identified):
    def __init__(self):
        self.__server = Server()
        uid = self.__server.get_uid()
        super().__init__(uid)

    @property
    def identified(self):
        return Identified(self.id)

    def _append_task(self, task: Task):
        self.__server.append(task)
