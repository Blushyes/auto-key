from dataclasses import dataclass
from typing import Optional

from executor.interfaces import CommandExecutor
from script_loader import ScriptInfo


from executor.external import Cosmic

@dataclass
class ScriptStep:
    executor: CommandExecutor
    arg: str
    jump_to: Optional[int] = None


def execute(context: ScriptInfo, script: list[ScriptStep]):
    i = 0
    while i < len(script):
        cmd: ScriptStep = script[i]
        cmd.executor.execute(context, cmd.arg)

        if Cosmic.pause_executor:  # 如果用户选择暂停执行，则退出循环
            return None

        if cmd.jump_to is not None:
            i = cmd.jump_to
        else:
            i += 1
