from executor import ScriptStep, execute
from interaction import InteractionLayer
from script_loader import pick_scripts, ScriptInfo
from script_loader.excel.__init__ import ExcelLoader
from script_loader.interfaces import ScriptLoader


class Command:
    EXIT: str = "exit"


class CommandLineInteractionLayer(InteractionLayer):
    def start(self) -> None:
        print("欢迎使用auto-key")
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
