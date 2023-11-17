import os

import pyautogui
import pyperclip
from PIL import Image

from executor.main import ScriptExecutor
from script_loader.main import KeyScript, ScriptInfo


class CommandType:
    SINGLE_CLICK = 1
    DOUBLE_CLICK = 2
    RIGHT_CLICK = 3
    INPUT = 4
    WAIT = 5
    SCROLL = 6


def _get_pos(img: str):
    image = Image.open(img)
    while pyautogui.locateCenterOnScreen(image, confidence=.9) is None:
        print('waiting...')
    return pyautogui.locateCenterOnScreen(image, confidence=.9)


class SimpleExecutor(ScriptExecutor):
    def __init__(self, script_info: ScriptInfo):
        self._script_info = script_info

    def execute(self, script: KeyScript) -> None:
        commands, contents, jump_list = script.commands, script.contents, script.jump_list
        i = 0
        while i < len(commands):
            print(i, commands[i])
            match commands[i]:
                case CommandType.SINGLE_CLICK:
                    x, y = _get_pos(os.path.join(self._script_info.path, contents[i]))
                    pyautogui.click(x, y, interval=.2, duration=.2)
                case CommandType.DOUBLE_CLICK:
                    x, y = _get_pos(os.path.join(self._script_info.path, contents[i]))
                    pyautogui.click(x, y, interval=.2, duration=.2, clicks=2)
                case CommandType.RIGHT_CLICK:
                    x, y = _get_pos(os.path.join(self._script_info.path, contents[i]))
                    pyautogui.click(x, y, interval=.2, duration=.2, button='right')
                case CommandType.INPUT:
                    pyperclip.copy(contents[i])
                    pyautogui.hotkey('ctrl', 'v')
                case CommandType.WAIT:
                    pass
                case CommandType.SCROLL:
                    pyautogui.scroll(int(contents[i]))
            if jump_list[i] == -1:
                i += 1
            else:
                i = int(jump_list[i])
