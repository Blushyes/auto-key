from pathlib import Path

import keyboard

from executor import ScriptStep, execute
from interaction import InteractionLayer
from recorder.simple import SimpleRecorder
from script_loader import pick_scripts, ScriptInfo, script_exist, SCRIPT_DIR
from script_loader.excel import ExcelLoader
from script_loader.interfaces import ScriptLoader


class Command:
    EXIT: str = "exit"


def _select_and_execute_script() -> None:
    scripts: list[ScriptInfo] = pick_scripts()
    print("获取到的脚本有")
    for i, script in enumerate(scripts):
        print(f"{i + 1}. {script.name}")
    while True:
        print("\n请问你要执行哪个脚本呢？")
        print("或者你可以输入下列的命令来执行对应步骤：")
        print("exit: 退出")
        command = input("请输入：")

        if command == Command.EXIT:
            print("准备退出程序")
            break

        try:
            select_script_index = int(command) - 1
        except:
            print("输入格式错误！！！")
            continue

        # TODO 可以根据 meta.json 配置脚本类型如：Excel等
        if select_script_index >= len(scripts) or select_script_index < 0:
            print("不存在的脚本！！！")
            continue
        select_path = scripts[select_script_index].path
        loader: ScriptLoader = ExcelLoader()
        key_scripts: list[ScriptStep] = loader.loads(select_path)
        execute(scripts[select_script_index], key_scripts)
        print("脚本执行完毕")


def _record_script():
    loader: ScriptLoader = ExcelLoader()
    recorder = SimpleRecorder()
    recorder.start()
    print('脚本已开始录制，按f8结束录制')
    while not keyboard.is_pressed('f8'):
        pass
    script: list[ScriptStep] = recorder.record()
    print('录制完毕')
    print('请选择：')
    print('1. 保存录制')
    print('2. 回放')
    while True:
        code = input('请输入：')
        match code:
            case "1":
                while True:
                    name = input('请输入脚本名：')
                    if name == '':
                        print("脚本名不能为空")
                        continue
                    if script_exist(name):
                        print("脚本已存在")
                        continue
                    break

                description = input('请输入脚本描述：')
                if description == '':
                    description = '未知'
                version = input('请输入脚本版本号：')
                if version == '':
                    version = '0.0.1'
                author = input('请输入脚本作者：')
                if author == '':
                    author = '未知'
                loader.save(
                    script,
                    ScriptInfo(
                        Path(SCRIPT_DIR) / name, name, description, version, author
                    ),
                )
                print("脚本保存完毕")
                return
            case "2":
                execute(..., script)
                print("脚本执行完毕")
                return
            case _:
                print("未知的指令")


class CommandLineInteractionLayer(InteractionLayer):
    def start(self) -> None:
        print("欢迎使用auto-key")
        print('你需要干什么呢？')
        print('1. 执行脚本')
        print('2. 录制脚本')
        code = input('请输入：')
        match code:
            case "1":
                _select_and_execute_script()
            case "2":
                _record_script()
            case _:
                print("未知的指令")
