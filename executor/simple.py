import pyautogui
import pyperclip
from PIL import Image

from executor.main import ScriptExecutor
from script_loader.main import KeyScript, ScriptInfo
from pathlib import Path
from executor.cosmic import Cosmic


class CommandType:
    SINGLE_CLICK = 1
    DOUBLE_CLICK = 2
    RIGHT_CLICK = 3
    INPUT = 4
    WAIT = 5
    SCROLL = 6


def _get_pos(img_path: Path) -> tuple[int, int] | None:
    image = Image.open(img_path)
    while True:
        try:
            return pyautogui.locateCenterOnScreen(image, confidence=.9)
        except pyautogui.ImageNotFoundException:
            print(f"未在屏幕区域匹配到与 {img_path} 相同的图片")
            if Cosmic.pause_executor:  # 如果用户选择暂停执行，则退出循环
                return None


class SimpleExecutor(ScriptExecutor):
    def __init__(self, script_info: ScriptInfo):
        self._script_info = script_info

    def execute(self, scripts: list[KeyScript]) -> None:
        i = 0
        while i < len(scripts):
            script: KeyScript = scripts[i]
            print(i, script.command)
            try:
                match script.command:

                    case CommandType.SINGLE_CLICK:
                        try:
                            x, y = _get_pos(Path(self._script_info.path) / script.content)
                            x, y = x + script.offset_x, y + script.offset_y  # 偏移量
                            pyautogui.click(x, y, interval=.2, duration=.2)
                        except TypeError:  # 用户选择暂停执行
                            return

                    case CommandType.DOUBLE_CLICK:
                        try:
                            x, y = _get_pos(Path(self._script_info.path) / script.content)
                            x, y = x + script.offset_x, y + script.offset_y  # 偏移量
                            pyautogui.click(x, y, interval=.2, duration=.2, clicks=2)
                        except TypeError:  # 用户选择暂停执行
                            return

                    case CommandType.RIGHT_CLICK:
                        try:
                            x, y = _get_pos(Path(self._script_info.path) / script.content)
                            x, y = x + script.offset_x, y + script.offset_y  # 偏移量
                            pyautogui.click(x, y, interval=.2, duration=.2, button='right')
                        except TypeError:  # 用户选择暂停执行
                            return

                    case CommandType.INPUT:
                        pyperclip.copy(script.content)
                        pyautogui.hotkey('ctrl', 'v')

                    case CommandType.WAIT:
                        pass

                    case CommandType.SCROLL:
                        pyautogui.scroll(int(script.content))

            except pyautogui.FailSafeException:
                print("鼠标移动到屏幕左上边缘，触发了安全保护，脚本执行已停止。")
                return

            if script.jump_to == -1:
                i += 1
            else:
                i = int(script.jump_to)