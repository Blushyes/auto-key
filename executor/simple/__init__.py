import platform
import random
import re
import subprocess
import time
from pathlib import Path
from typing import Callable, Any

import pyautogui
import pyperclip
from PIL import Image
from pynput import mouse
from pynput.mouse import Button

from context.utils import singleton
from executor.external import (
    CommandType,
    Cosmic,
    CoordTransformWithDurationArg,
    ClickArgWithOffset,
)
from executor.interfaces import CommandExecutorFactory, CommandExecutor
from executor.simple.format_hotkey_string import format_hotkey_string
from script_loader import ScriptInfo
from fast_script_utils.time import parse_time_to_ms

# NOTE 用于分隔次要图片，比如arg的图片为hello.png，那么hello-1.png和hello-2.png以及hello_1.png都会被尝试读取坐标
# NOTE 只要有一张图片能读取到坐标即可返回
SECONDARY_SYMBOLS = ('-', '_', '.')

MOUSE_CONTROLLER = mouse.Controller()


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
            CommandType.PAUSE: SimplePauseExecutor,
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
    def execute(self, context: ScriptInfo, arg: CoordTransformWithDurationArg) -> None:
        MOUSE_CONTROLLER.scroll(int(arg.x), int(arg.y))
        time.sleep(arg.duration)
        # pyautogui.scroll(int(arg))


@singleton
class SimpleHotkeyExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        pyautogui.hotkey(*format_hotkey_string(arg))


@singleton
class SimpleMoveExecutor(CommandExecutor):

    def execute(self, context: ScriptInfo, arg: CoordTransformWithDurationArg) -> None:
        MOUSE_CONTROLLER.position = (arg.x, arg.y)
        time.sleep(arg.duration)


@singleton
class SimpleSingleClickExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: ClickArgWithOffset) -> None:
        img_path = Path(context.path) / arg.arg

        pos = _get_pos_loosely(
            img_path,
            lambda images: _get_pos_with_offset(images, arg.offset_x, arg.offset_y),
        )
        if pos is None:
            return

        x, y = pos
        pyautogui.click(x, y, interval=0.2, duration=0.2)


@singleton
class SimpleDoubleClickExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: ClickArgWithOffset) -> None:
        img_path = Path(context.path) / arg.arg

        pos = _get_pos_loosely(
            img_path,
            lambda images: _get_pos_with_offset(images, arg.offset_x, arg.offset_y),
        )
        if pos is None:
            return

        x, y = pos
        pyautogui.click(x, y, interval=0.2, duration=0.2, clicks=2)


@singleton
class SimpleRightClickExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: ClickArgWithOffset) -> None:
        img_path = Path(context.path) / arg.arg

        pos = _get_pos_loosely(
            img_path,
            lambda images: _get_pos_with_offset(images, arg.offset_x, arg.offset_y),
        )
        if pos is None:
            return

        x, y = pos
        pyautogui.click(x, y, interval=0.2, duration=0.2, button="right")


@singleton
class SimpleDragExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: ClickArgWithOffset) -> None:
        pyautogui.dragRel(
            arg.offset_x, arg.offset_y, duration=float(arg.arg)
        )  # 使用 内容列来存持续时间，


@singleton
class SimpleCommandExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: Any) -> None:
        bat_file_path = Path(context.path) / str(arg)
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
    def execute(self, context: ScriptInfo, arg: Any) -> None:
        pyautogui.click()


@singleton
class SimpleJustRightClickExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: Any) -> None:
        pyautogui.click()


@singleton
class SimpleJustLeftPressExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: Any) -> None:
        MOUSE_CONTROLLER.press(Button.left)


@singleton
class SimpleJustRightPressExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: Any) -> None:
        MOUSE_CONTROLLER.press(Button.right)


@singleton
class SimplePauseExecutor(CommandExecutor):
    @staticmethod
    def _parse_time(time_str: str) -> float:
        if 'random' not in time_str.strip():
            return parse_time_to_ms(time_str)

        # Handle random cases
        if 'random(' in time_str and ')' in time_str:
            # Case: random(10s) or random(1min)
            match = re.search(r'random\(([^)]+)\)', time_str)
            if match:
                inner = match.group(1)
                if ',' in inner:
                    # Case: random(1s, 2s)
                    start, end = map(str.strip, inner.split(','))
                    start_ms = parse_time_to_ms(start)
                    end_ms = parse_time_to_ms(end)
                    return random.uniform(start_ms, end_ms)
                else:
                    # Case: random(10s) or random(1min)
                    max_ms = parse_time_to_ms(inner)
                    return random.uniform(0, max_ms)

        # Case: 3s + random(1s) or 3s +- random(1s)
        parts = re.split(r'\s*([+-])\s*', time_str)
        total_ms = 0
        for i, part in enumerate(parts):
            if 'random(' in part:
                match = re.search(r'random\(([^)]+)\)', part)
                if match:
                    random_ms = parse_time_to_ms(match.group(1))
                    if i > 0 and parts[i - 1] == '-':
                        total_ms -= random.uniform(0, random_ms)
                    elif i > 1 and parts[i - 2] == '+-':
                        total_ms += random.uniform(-random_ms, random_ms)
                    else:
                        total_ms += random.uniform(0, random_ms)
            elif part not in ['+', '-', '+-']:
                total_ms += parse_time_to_ms(part)

        return total_ms

    def execute(self, context: ScriptInfo, arg: str) -> None:
        time.sleep(self._parse_time(arg) * 0.001)
