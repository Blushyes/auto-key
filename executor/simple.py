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


class PauseException(Exception):
    def __init__(self, message: str = '暂停'):
        self.message = message
        super().__init__(self.message)


def _get_pos(img: str) -> tuple[int, int]:
    image = Image.open(img)

    # 有时候图片还没加载完，或者画面是动态的，需要循环查找
    while pyautogui.locateCenterOnScreen(image) is None:
        print('waiting...')

        if Cosmic.pause_executor:  # 如果用户选择暂停执行，则退出循环
            raise PauseException()

    return pyautogui.locateCenterOnScreen(image)


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
                            pyautogui.click(x, y, interval=.2, duration=.2)
                        except TypeError:  # 用户选择暂停执行
                            return

                    case CommandType.DOUBLE_CLICK:
                        try:
                            x, y = _get_pos(Path(self._script_info.path) / script.content)
                            pyautogui.click(x, y, interval=.2, duration=.2, clicks=2)
                        except TypeError:  # 用户选择暂停执行
                            return

                    case CommandType.RIGHT_CLICK:
                        try:
                            x, y = _get_pos(Path(self._script_info.path) / script.content)
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
            except PauseException:
                print("脚本已暂停。")
                return

            if script.jump_to == -1:
                i += 1
            else:
                i = int(script.jump_to)