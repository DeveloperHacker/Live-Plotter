import time
from multiprocessing import Process, Value, Queue, Lock
from queue import Empty

import matplotlib.pyplot as plt

from live_plotter.proxy.Task import Task, CreateTask, DestroyTask


class Server(Process):
    PAUSE = 1 / 50
    DELAY = 1 / 2
    _instance = None

    def __new__(cls, _object=None) -> 'Server':
        return object.__new__(Server) if Server._instance is None else Server._instance

    def __init__(self):
        if Server._instance is None:
            Server._instance = self
            self._lock = Lock()
            self._max_uid = Value("i", 0)
            self._queue = Queue()
            self._stop_requests = Value("i", True)
            super().__init__(target=self._handle)
        self.__start()

    def __start(self):
        with self._lock:
            if self._stop_requests.value:
                self._stop_requests.value = False
                self.start()

    def __stop(self):
        self._stop_requests.value = True

    def _handle(self):
        import warnings
        import matplotlib.cbook
        warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)
        instances = {}
        start = time.time()
        while not self._stop_requests.value:
            with self._lock:
                try:
                    task: Task = self._queue.get(block=True, timeout=Server.DELAY)
                    args = task.args(instances)
                    kwargs = task.kwargs(instances)
                    instance = task.execute(*args, **kwargs)
                    if isinstance(task, CreateTask):
                        instances[task.instance_id] = instance
                    elif isinstance(task, DestroyTask):
                        del instances[task.instance_id]
                    if len(instances) == 0:
                        self.__stop()
                except Empty:
                    pass
                if time.time() - start > Server.DELAY:
                    plt.pause(Server.PAUSE)
                    start = time.time()

    def get_uid(self) -> int:
        with self._max_uid.get_lock():
            self._max_uid.value += 1
            result = self._max_uid.value
        return result

    def append(self, task: Task):
        self._queue.put(task)

    def stop(self):
        with self._lock:
            self.__stop()
