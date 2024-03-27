from enum import Enum


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
