from abc import ABC, abstractmethod
from pathlib import Path

from executor import ScriptStep
from script_loader import ScriptInfo


class ScriptLoader(ABC):

    @abstractmethod
    def loads(self, path: Path | str) -> list[ScriptStep]: ...

    @abstractmethod
    def save(self, script: list[ScriptStep], info: ScriptInfo) -> None: ...
