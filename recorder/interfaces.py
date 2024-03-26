from abc import ABC, abstractmethod

from executor import ScriptStep


class Recorder(ABC):
    """
    脚本录制器，录制脚本并转换为Script
    """

    @abstractmethod
    def start(self): ...

    @abstractmethod
    def stop(self): ...

    @abstractmethod
    def record(self) -> list[ScriptStep]: ...
