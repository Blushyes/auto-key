from dataclasses import dataclass
from typing import Optional

from executor.interfaces import CommandExecutor
from script_loader import ScriptInfo


@dataclass
class CommandExecutorWrapper:
    executor: CommandExecutor
    arg: str
    jump_to: Optional[int] = None


def execute(context: ScriptInfo, script: list[CommandExecutorWrapper]):
    for wrapper in script:
        wrapper.executor.execute(context, wrapper.arg)
