import time
from multiprocessing import Process, Value, Queue
from queue import Empty

import matplotlib.pyplot as plt

from live_plotter.proxy.Task import Task


class Server(Process):
    PAUSE = 0.005
    DELAY = 1.0 / 2.0
    _instance = None
    FLUSHABLE = "flushable"

    def __new__(cls, _object=None) -> 'Server':
        return object.__new__(Server) if Server._instance is None else Server._instance

    def __init__(self):
        if Server._instance is None:
            Server._instance = self
            self._max_uid = Value("i", 0)
            self._queue = Queue()
            self._stop_requests = Value("i", False)
            super().__init__(target=self._handle)
            self.start()

    def _handle(self):
        import warnings
        import matplotlib.cbook
        warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)
        instances = {}
        start = time.time()
        while not self._stop_requests.value or not self._queue.empty():
            try:
                task = self._queue.get(block=True, timeout=Server.DELAY)
                task.execute(instances)
            except Empty:
                pass
            if time.time() - start > Server.DELAY:
                plt.pause(Server.PAUSE)
                start = time.time()

    def get_uid(self) -> int:
        with self._max_uid.get_lock():
            self._max_uid.value += 1
        return self._max_uid.value

    def append(self, task: Task):
        self._queue.put(task)

    def stop(self):
        self._stop_requests.value = True
