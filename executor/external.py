from dataclasses import dataclass
from enum import Enum
from typing import Any, TypeVar


class CommandType(Enum):
    MOVE = 'move'
    SINGLE_CLICK = 'click'
    DOUBLE_CLICK = 'db_click'
    RIGHT_CLICK = 'r_click'
    INPUT = 'input'
    WAIT = 'wait'
    SCROLL = 'scroll'
    HOTKEY = 'key'
    DRAG = 'drag'
    CMD = 'cmd'
    JUST_LEFT_CLICK = 'just_click'
    JUST_RIGHT_CLICK = 'just_r_click'
    JUST_LEFT_PRESS = 'just_press'
    JUST_RIGHT_PRESS = 'just_r_press'


class Cosmic:
    """
    用一个 class 存储需要跨模块访问的变量值，命名为 Cosmic
    """

    pause_executor = False  # 手动暂停标志
    run_script_shortcut = "F6"  # 运行脚本快捷键
    pause_script_shortcut = "F9"  # 暂停脚本快捷键
    do_run_script = False  # 是否运行脚本
    do_pause_script = False  # 是否暂停脚本


class SeparableArg:
    SEP: str = '|'

    def __str__(self):
        attributes = [
            str(getattr(self, attr))
            for attr in dir(self)
            if not attr.startswith('__') and not callable(getattr(self, attr))
        ]
        return SeparableArg.SEP.join(attributes)


@dataclass
class ClickArgWithOffset(SeparableArg):
    arg: str
    offset_x: int
    offset_y: int


@dataclass
class CoordTransformWithDurationArg(SeparableArg):
    x: float
    y: float
    duration: float


# NOTE 指令类型以及其执行器接收的参数的类型
ARG_MAPPING = {
    CommandType.INPUT: str,
    CommandType.WAIT: str,
    CommandType.SCROLL: CoordTransformWithDurationArg,
    CommandType.HOTKEY: str,
    CommandType.MOVE: CoordTransformWithDurationArg,
    CommandType.SINGLE_CLICK: ClickArgWithOffset,
    CommandType.DOUBLE_CLICK: ClickArgWithOffset,
    CommandType.RIGHT_CLICK: ClickArgWithOffset,
    CommandType.DRAG: str,
    CommandType.CMD: str,
    CommandType.JUST_LEFT_CLICK: CoordTransformWithDurationArg,
    CommandType.JUST_RIGHT_CLICK: CoordTransformWithDurationArg,
    CommandType.JUST_LEFT_PRESS: CoordTransformWithDurationArg,
    CommandType.JUST_RIGHT_PRESS: CoordTransformWithDurationArg,
}
