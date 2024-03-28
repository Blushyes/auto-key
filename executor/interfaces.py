from abc import abstractmethod, ABC
from typing import Any

from executor.external import CommandType
from script_loader import ScriptInfo


class CommandExecutor(ABC):
    @abstractmethod
    def execute(self, context: ScriptInfo, arg: Any) -> None: ...


class CommandExecutorFactory(ABC):
    @abstractmethod
    def create(self, command_type: CommandType) -> CommandExecutor: ...

    @abstractmethod
    def typeof(self, executor: CommandExecutor) -> CommandType: ...
