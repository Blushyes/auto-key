import json
import logging
import platform
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pyautogui
import pyperclip
from PIL import Image
from pynput import mouse

from context.utils import singleton
from executor.external import CommandType, Cosmic
from executor.interfaces import CommandExecutorFactory, CommandExecutor
from executor.simple.format_hotkey_string import format_hotkey_string
from script_loader import ScriptInfo

# NOTE 用于分隔次要图片，比如arg的图片为hello.png，那么hello-1.png和hello-2.png以及hello_1.png都会被尝试读取坐标
# NOTE 只要有一张图片能读取到坐标即可返回
SECONDARY_SYMBOLS = ('-', '_', '.')


# TODO 这些Arg交给Arg Register统一管理，实现配置化
@dataclass
class ClickArgWithOffset:
    arg: str
    offset_x: int
    offset_y: int


@dataclass
class CoordTransformWithDurationArg:
    x: float
    y: float
    duration: float


def _get_pos(img_paths: Path | list[Path]) -> tuple[int, int] | None:
    """
    获取某个图片在屏幕上的坐标，该函数会一直循环获取直到用户主动暂停脚本或者发生未知错误

    Args:
        img_paths: 图片与项目根目录的相对路径列表（也可以为一张图片的Path路径），找到其中一张的坐标即返回

    Returns:
        - x, y
        - 用户主动暂停或者发生错误时返回None
    """
    if isinstance(img_paths, Path):
        img_paths = [img_paths]

    images = [Image.open(img) for img in img_paths]
    i = -1
    while True:
        try:
            i = (i + 1) % len(images)
            x, y = pyautogui.locateCenterOnScreen(images[i], confidence=0.9)

            # NOTE MacBook的屏幕的渲染分辨率和实际分辨率不是点对点关系，可能和内建视网膜显示器有关
            # NOTE 需要将返回的坐标分别乘上0.5，这样才可以准确定位
            return (x * 0.5, y * 0.5) if platform.system() == 'Darwin' else (x, y)
        except pyautogui.ImageNotFoundException:
            print(f"未在屏幕区域匹配到与 {img_paths} 相同的图片")

            if Cosmic.pause_executor:  # 如果用户选择暂停执行，则退出循环
                return None


def _get_pos_with_offset(
    img_paths: Path | list[Path], offset_x: int, offset_y: int
) -> tuple[int, int] | None:
    """
    获取某个图片在屏幕上的坐标，并且返回结果附带偏移值，该函数会一直循环获取直到用户主动暂停脚本或者发生未知错误

    Args:
        img_paths: 图片与项目根目录的相对路径列表（也可以为一张图片的Path路径），找到其中一张的坐标即返回
        offset_x: 偏移x坐标
        offset_y: 便宜y坐标

    Returns:
        - x(with offset), y(with offset)
        - 用户主动暂停或者发生错误时返回None
    """
    pos = _get_pos(img_paths)
    if pos is None:
        return None

    x, y = pos
    return x + offset_x, y + offset_y  # 偏移量


def _get_pos_loosely(
    img_path: Path, handler: Callable[[Path | list[Path]], tuple[int, int] | None]
) -> tuple[int, int] | None:
    """
    相对宽松地获取图片坐标（即可以用次要图片来代替获取）

    See: SECONDARY_SYMBOLS
    """
    parent_dir = img_path.parent
    images = []
    for SYMBOL in SECONDARY_SYMBOLS:
        images.extend(list(parent_dir.glob(f'{img_path.name.split(".")[0]}{SYMBOL}*')))
    return handler(images)


@singleton
class SimpleCommandExecutorFactory(CommandExecutorFactory):
    def __init__(self):
        self._command_to_executor = {
            CommandType.INPUT: SimpleInputExecutor,
            CommandType.WAIT: SimpleWaitExecutor,
            CommandType.SCROLL: SimpleScrollExecutor,
            CommandType.HOTKEY: SimpleHotkeyExecutor,
            CommandType.MOVE: SimpleMoveExecutor,
            CommandType.SINGLE_CLICK: SimpleSingleClickExecutor,
            CommandType.DOUBLE_CLICK: SimpleDoubleClickExecutor,
            CommandType.RIGHT_CLICK: SimpleRightClickExecutor,
            CommandType.DRAG: SimpleDragExecutor,
            CommandType.CMD: SimpleCommandExecutor,
            CommandType.JUST_LEFT_CLICK: SimpleJustLeftClickExecutor,
            CommandType.JUST_RIGHT_CLICK: SimpleJustRightClickExecutor,
            CommandType.JUST_LEFT_PRESS: SimpleJustLeftPressExecutor,
            CommandType.JUST_RIGHT_PRESS: SimpleJustRightPressExecutor,
        }

        self._executor_to_command = {
            type(executor()): command
            for command, executor in self._command_to_executor.items()
        }

    def create(self, command_type: CommandType) -> CommandExecutor:
        executor_class = self._command_to_executor.get(command_type)
        if executor_class:
            return executor_class()
        else:
            raise ValueError(f"No executor available for command type: {command_type}")

    def typeof(self, executor: CommandExecutor) -> CommandType:
        return self._executor_to_command.get(type(executor))


@singleton
class SimpleInputExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        pyperclip.copy(arg)
        pyautogui.hotkey("command" if platform.system() == "Darwin" else "ctrl", "v")


@singleton
class SimpleWaitExecutor(CommandExecutor):
    """
    等待指定图片出现为止
    """

    def execute(self, context: ScriptInfo, arg: str) -> None:
        _get_pos_loosely(Path(context.path) / arg, _get_pos)


@singleton
class SimpleScrollExecutor(CommandExecutor):
    def __init__(self):
        self._controller = mouse.Controller()

    def execute(self, context: ScriptInfo, arg: str) -> None:
        scroll_arg = CoordTransformWithDurationArg(**json.loads(arg))
        self._controller.scroll(int(scroll_arg.x), int(scroll_arg.y))
        time.sleep(scroll_arg.duration)
        # pyautogui.scroll(int(arg))


@singleton
class SimpleHotkeyExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        pyautogui.hotkey(*format_hotkey_string(arg))


@singleton
class SimpleMoveExecutor(CommandExecutor):
    def __init__(self):
        self._controller = mouse.Controller()

    def execute(self, context: ScriptInfo, arg: str) -> None:
        move_arg = CoordTransformWithDurationArg(**json.loads(arg))
        self._controller.position = (move_arg.x, move_arg.y)
        time.sleep(move_arg.duration)
        # pyautogui duration粒度不够，最小好像只能0.1秒
        # pyautogui.moveTo(move_arg.x, move_arg.y, duration=move_arg.duration)


@singleton
class SimpleSingleClickExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        parsed_arg = ClickArgWithOffset(**json.loads(arg))
        img_path = Path(context.path) / parsed_arg.arg

        pos = _get_pos_loosely(
            img_path,
            lambda images: _get_pos_with_offset(
                images, parsed_arg.offset_x, parsed_arg.offset_y
            ),
        )
        if pos is None:
            return

        x, y = pos
        pyautogui.click(x, y, interval=0.2, duration=0.2)


@singleton
class SimpleDoubleClickExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        parsed_arg = ClickArgWithOffset(**json.loads(arg))
        img_path = Path(context.path) / parsed_arg.arg

        pos = _get_pos_loosely(
            img_path,
            lambda images: _get_pos_with_offset(
                images, parsed_arg.offset_x, parsed_arg.offset_y
            ),
        )
        if pos is None:
            return

        x, y = pos
        pyautogui.click(x, y, interval=0.2, duration=0.2, clicks=2)


@singleton
class SimpleRightClickExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        parsed_arg = ClickArgWithOffset(**json.loads(arg))
        img_path = Path(context.path) / parsed_arg.arg

        pos = _get_pos_loosely(
            img_path,
            lambda images: _get_pos_with_offset(
                images, parsed_arg.offset_x, parsed_arg.offset_y
            ),
        )
        if pos is None:
            return

        x, y = pos
        pyautogui.click(x, y, interval=0.2, duration=0.2, button="right")


@singleton
class SimpleDragExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        parsed_arg = ClickArgWithOffset(**json.loads(arg))
        pyautogui.dragRel(
            parsed_arg.offset_x, parsed_arg.offset_y, duration=float(parsed_arg.arg)
        )  # 使用 内容列来存持续时间，


@singleton
class SimpleCommandExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        bat_file_path = Path(context.path) / arg
        print(
            f"执行批处理文件: {bat_file_path}"
        )  # print 会被重定向到图形界面 脚本运行状态 文本框
        process = subprocess.Popen(
            ['cmd', '/c', str(bat_file_path)],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        process.wait()
        stdout, stderr = process.communicate()
        print(stdout, stderr)


@singleton
class SimpleJustLeftClickExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        pyautogui.click()


@singleton
class SimpleJustRightClickExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        pyautogui.click(button='right')


@singleton
class SimpleJustLeftPressExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        pyautogui.press('left')


@singleton
class SimpleJustRightPressExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        pyautogui.press('right')
