import json
from dataclasses import dataclass
from pathlib import Path

import pyautogui
import pyperclip
from PIL import Image

from executor.external import CommandType, Cosmic
from executor.interfaces import CommandExecutorFactory, CommandExecutor
from executor.simple.format_hotkey_string import format_hotkey_string
from script_loader import ScriptInfo

import subprocess


@dataclass
class ClickArgWithOffset:
    img_name: str
    offset_x: int
    offset_y: int


def _get_pos(img_path: Path) -> tuple[int, int] | None:
    image = Image.open(img_path)
    while True:
        try:
            return pyautogui.locateCenterOnScreen(image, confidence=0.9)
        except pyautogui.ImageNotFoundException:
            print(f"未在屏幕区域匹配到与 {img_path} 相同的图片")
            if Cosmic.pause_executor:  # 如果用户选择暂停执行，则退出循环
                return None


def _get_pos_with_offset(
    img_path: Path, offset_x: int, offset_y: int
) -> tuple[int, int] | None:
    pos = _get_pos(img_path)
    if pos is None:
        return None

    x, y = pos
    return x + offset_x, y + offset_y  # 偏移量


class SimpleCommandExecutorFactory(CommandExecutorFactory):
    def create(self, command_type: CommandType) -> CommandExecutor:
        executor_classes = {
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
        }
        executor_class = executor_classes.get(command_type)
        if executor_class:
            return executor_class()
        else:
            raise ValueError(f"No executor available for command type: {command_type}")


class SimpleInputExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        pyperclip.copy(arg)
        pyautogui.hotkey("ctrl", "v")


class SimpleWaitExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        pass


class SimpleScrollExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        pyautogui.scroll(int(arg))


class SimpleHotkeyExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        pyautogui.hotkey(*format_hotkey_string(arg))


class SimpleMoveExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        x, y = map(int, arg.split(","))
        pyautogui.moveTo(x, y, duration=0.2)


class SimpleSingleClickExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:

        parsed_arg = ClickArgWithOffset(**json.loads(arg))

        img_path = Path(context.path) / parsed_arg.img_name
        pos = _get_pos_with_offset(img_path, parsed_arg.offset_x, parsed_arg.offset_y)

        if pos is None:
            return

        x, y = pos
        pyautogui.click(x, y, interval=0.2, duration=0.2)


class SimpleDoubleClickExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        parsed_arg = ClickArgWithOffset(**json.loads(arg))
        img_path = Path(context.path) / parsed_arg.img_name
        pos = _get_pos_with_offset(img_path, parsed_arg.offset_x, parsed_arg.offset_y)

        if pos is None:
            return

        x, y = pos
        pyautogui.click(x, y, interval=0.2, duration=0.2, clicks=2)


class SimpleRightClickExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        parsed_arg = ClickArgWithOffset(**json.loads(arg))
        img_path = Path(context.path) / parsed_arg.img_name
        pos = _get_pos_with_offset(img_path, parsed_arg.offset_x, parsed_arg.offset_y)

        if pos is None:
            return

        x, y = pos
        pyautogui.click(x, y, interval=0.2, duration=0.2, button="right")


class SimpleDragExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        parsed_arg = ClickArgWithOffset(**json.loads(arg))
        pyautogui.dragRel(parsed_arg.offset_x, parsed_arg.offset_y, duration=float(parsed_arg.img_name))  # 使用 内容列来存持续时间，
                                                                                                        # TODO img_name 这个命名不太好吧，要不要改改？


class SimpleCommandExecutor(CommandExecutor):
    def execute(self, context: ScriptInfo, arg: str) -> None:
        bat_file_path = Path(context.path) / arg
        print(f"执行批处理文件: {bat_file_path}")  # print 会被重定向到图形界面 脚本运行状态 文本框
        process = subprocess.Popen(['cmd', '/c', str(bat_file_path)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process.wait()
        stdout, stderr = process.communicate()
        print(stdout, stderr)