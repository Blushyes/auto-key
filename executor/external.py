from enum import Enum


class CommandType(Enum):
    MOVE = 0
    SINGLE_CLICK = 1
    DOUBLE_CLICK = 2
    RIGHT_CLICK = 3
    INPUT = 4
    WAIT = 5
    SCROLL = 6
    HOTKEY = 7
    DRAG = 8
    CMD = 9
    JUST_LEFT_CLICK = 10
    JUST_RIGHT_CLICK = 11
    JUST_LEFT_PRESS = 12
    JUST_RIGHT_PRESS = 13


class Cosmic:
    """
    用一个 class 存储需要跨模块访问的变量值，命名为 Cosmic
    """

    pause_executor = False  # 手动暂停标志
    run_script_shortcut = "F6"  # 运行脚本快捷键
    pause_script_shortcut = "F9"  # 暂停脚本快捷键
    do_run_script = False  # 是否运行脚本
    do_pause_script = False  # 是否暂停脚本
