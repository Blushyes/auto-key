from executor.main import ScriptExecutor
from executor.simple import SimpleExecutor
from interaction.main import InteractionLayer
from script_loader.excel_loader import ExcelLoader
from script_loader.main import pick_scripts, ScriptInfo, ScriptLoader, KeyScript


class Command:
    EXIT: str = 'exit'


class CommandLineInteractionLayer(InteractionLayer):
    def start(self) -> None:
        print('欢迎使用auto-key')
        scripts: list[ScriptInfo] = pick_scripts()
        print('获取到的脚本有')
        for i, script in enumerate(scripts):
            print(f'{i + 1}. {script.name}')
        while True:
            print('\n请问你要执行哪个脚本呢？')
            print('或者你可以输入下列的命令来执行对应步骤：')
            print('exit: 退出')
            command = input('请输入：')

            if command == Command.EXIT:
                print('准备退出程序')
                break

            try:
                select_script_index = int(command) - 1
            except:
                print('输入格式错误！！！')
                continue

            # TODO 可以根据 meta.json 配置脚本类型如：Excel等
            if select_script_index >= len(scripts) or select_script_index < 0:
                print('不存在的脚本！！！')
                continue
            select_path = scripts[select_script_index].path
            loader: ScriptLoader = ExcelLoader()
            key_scripts: list[KeyScript] = loader.loads(select_path)
            executor: ScriptExecutor = SimpleExecutor(scripts[select_script_index])
            executor.execute(key_scripts)
            print('脚本执行完毕')
