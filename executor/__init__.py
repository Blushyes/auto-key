from dataclasses import dataclass
from typing import Optional

from executor.interfaces import CommandExecutor
from script_loader import ScriptInfo


@dataclass
class ScriptStep:
    executor: CommandExecutor
    arg: str
    jump_to: Optional[int] = None


def execute(context: ScriptInfo, script: list[ScriptStep]):
    i = 0
    while i < len(script):
        cmd = script[i]
        cmd.executor.execute(context, cmd.arg)

        if cmd.jump_to is not None:
            i = cmd.jump_to
        else:
            i += 1
