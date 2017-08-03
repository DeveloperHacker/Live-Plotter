import itertools
from abc import abstractmethod

from live_plotter.proxy.Identified import Identified


class Task:
    def __init__(self, instance_id: int, *args, **kwargs):
        self.instance_id = instance_id
        self._args = args
        self._kwargs = kwargs

    def args(self, instances: dict):
        instance = instances.get(self.instance_id, None)
        args = (instances[arg.id] if isinstance(arg, Identified) else arg for arg in self._args)
        return itertools.chain([instance], args)

    def kwargs(self, instances: dict):
        return {label: instances[arg.id] if isinstance(arg, Identified) else arg for label, arg in
                self._kwargs.items()}

    @abstractmethod
    def execute(self, instance, *args, **kwargs):
        pass


class UpdateTask(Task):
    def __init__(self, instance_id: int, method_name: str, *args, **kwargs):
        super().__init__(instance_id, *args, **kwargs)
        self.method_name = method_name

    def execute(self, instance, *args, **kwargs):
        method = getattr(instance, self.method_name)
        method(*args, **kwargs)
        return instance


class CreateTask(Task):
    def __init__(self, instance_id: int, creator, *args, **kwargs):
        super().__init__(instance_id, *args, **kwargs)
        self.creator = creator

    def execute(self, instance, *args, **kwargs):
        assert instance is None
        instance = self.creator(*args, **kwargs)
        return instance


class DestroyTask(Task):
    def __init__(self, instance_id: int):
        super().__init__(instance_id)

    def execute(self, instance, *args, **kwargs):
        return instance
