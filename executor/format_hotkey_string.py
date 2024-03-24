import re

def format_hotkey_string(hotkey_str):
    # 使用正则表达式来匹配键名，并将它们转换为小写
    keys = re.findall(r'\w+', hotkey_str.lower())
    # 将键名转换为pyautogui可以识别的格式
    formatted_keys = tuple(keys)
    return formatted_keys

if __name__ == "__main__":
    # 示例使用
    hotkey_str = "Win+R"
    formatted_keys = format_hotkey_string(hotkey_str)
    print(formatted_keys)
    # 模拟按键
    import pyautogui
    pyautogui.hotkey(*formatted_keys)
