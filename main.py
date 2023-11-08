import pandas as pd
import pyautogui
import pyperclip
from PIL import Image
from pandas import DataFrame, Series

FILE_NAME = '1.xlsx'


class CommandType:
    SINGLE_CLICK = 1
    DOUBLE_CLICK = 2
    RIGHT_CLICK = 3
    INPUT = 4
    WAIT = 5
    SCROLL = 6


def get_col(df: DataFrame, col_index: int) -> list:
    col: Series = df.iloc[:, col_index]
    return col.to_list()


def loads_script():
    df: DataFrame = pd.read_excel(FILE_NAME)
    commands: list = get_col(df, 0)
    contents: list = get_col(df, 1)
    jump_list: list = get_col(df, 2)
    return commands, contents, jump_list


def get_pos(img: str):
    image = Image.open(img)
    while pyautogui.locateCenterOnScreen(image) is None:
        print('waiting...')
    return pyautogui.locateCenterOnScreen(image)


commands, contents, jump_list = loads_script()
i = 0
while i < len(commands):
    print(i, commands[i])
    match commands[i]:
        case CommandType.SINGLE_CLICK:
            x, y = get_pos(contents[i])
            pyautogui.click(x, y, interval=.2, duration=.2)
        case CommandType.DOUBLE_CLICK:
            x, y = get_pos(contents[i])
            pyautogui.click(x, y, interval=.2, duration=.2, clicks=2)
        case CommandType.RIGHT_CLICK:
            x, y = get_pos(contents[i])
            pyautogui.click(x, y, interval=.2, duration=.2, button='right')
        case CommandType.INPUT:
            pyperclip.copy(contents[i])
            pyautogui.hotkey('ctrl', 'v')
        case CommandType.WAIT:
            pass
        case CommandType.SCROLL:
            pyautogui.scroll(int(contents[i]))
    if pd.isna(jump_list[i]):
        i += 1
    else:
        i = int(jump_list[i])
