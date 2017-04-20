from abc import abstractmethod

from live_plotter.proxy.Identified import Identified


class Task:
    def __init__(self, instance_id: int, *args, **kwargs):
        self.instance_id = instance_id
        self.args = args
        self.kwargs = kwargs

    @abstractmethod
    def execute(self, instances: dict):
        pass


class UpdateTask(Task):
    def __init__(self, instance_id: int, method_name: str, *args, **kwargs):
        super().__init__(instance_id, *args, **kwargs)
        self.method_name = method_name

    def execute(self, instances: dict):
        instance = instances[self.instance_id]
        method = getattr(instance, self.method_name)
        args = (instances[arg.id] if isinstance(arg, Identified) else arg for arg in self.args)
        kwargs = {label: instances[arg.id] if isinstance(arg, Identified) else arg for label, arg in
                  self.kwargs.items()}
        method(*args, **kwargs)


class CreateTask(Task):
    def __init__(self, instance_id: int, creator, *args, **kwargs):
        super().__init__(instance_id, *args, **kwargs)
        self.creator = creator

    def execute(self, instances: dict):
        args = (instances[arg.id] if isinstance(arg, Identified) else arg for arg in self.args)
        kwargs = {label: instances[arg.id] if isinstance(arg, Identified) else arg for label, arg in
                  self.kwargs.items()}
        instances[self.instance_id] = self.creator(*args, **kwargs)
