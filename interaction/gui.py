import os
import sys
from executor.main import ScriptExecutor
from executor.simple import SimpleExecutor
from script_loader.excel_loader import ExcelLoader
from script_loader.main import pick_scripts, ScriptInfo, ScriptLoader, KeyScript
from interaction.Ui_auto_key import Ui_auto_key
from PySide6.QtWidgets import QApplication, QWidget



class Command:
    EXIT: str = 'exit'


class GuiInteractionLayer(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_auto_key()
        self.ui.setupUi(self)
        self.setup_signals()


    def setup_signals(self) -> None:
        # 获取脚本列表
        self.scripts_list: list[ScriptInfo] = pick_scripts()
        print(f'脚本列表：{self.scripts_list}')
        # 显示脚本列表
        for i, script in enumerate(self.scripts_list):
            # 从 1 开始计数
            self.ui.plainTextEdit_script_list.appendPlainText(f'{i + 1}. {script.name}')
            self.ui.comboBox_select_script.addItem(f'{i + 1}. {script.name}')
        # 连接 运行脚本 按钮 信号/槽
        self.ui.pushButton_run_script.clicked.connect(self.run_script)
        # 连接 退出 按钮 信号/槽
        # self.ui.pushButton_exit.clicked.connect(self.exit)


    def run_script(self) -> None:
        try:
            # 获取用户输入的脚本序号
            select_script = self.ui.comboBox_select_script.currentText()
            select_script_index = int(select_script.split('.')[0])
        except Exception as e:
            self.ui.plainTextEdit_script_execute_status.appendPlainText(f'脚本格式错误！！！{e}')
            return

        # TODO 可以根据 meta.json 配置脚本类型如：Excel等
        if select_script_index >= len(self.scripts_list) or select_script_index < 0:
            self.ui.plainTextEdit_script_execute_status.appendPlainText(f'不存在的脚本 “ {select_script} ” ！！！')
            return
        
        # 获取用户输入的脚本序号
        # 因为显示时从 1 开始计数，所以需要减 1
        select_path = self.scripts_list[select_script_index - 1].path

        # 加载脚本路径
        loader: ScriptLoader = ExcelLoader()
        key_scripts: list[KeyScript] = loader.loads(select_path)

        # 执行脚本
        # 因为显示时从 1 开始计数，所以需要减 1
        self.ui.plainTextEdit_script_execute_status.appendPlainText(f'脚本 “ {select_script} ” 执行中...')
        executor: ScriptExecutor = SimpleExecutor(self.scripts_list[select_script_index -1])
        executor.execute(key_scripts)
        # 显示脚本执行完毕
        self.ui.plainTextEdit_script_execute_status.appendPlainText(f'脚本 “ {select_script} ” 执行完毕')

def start():
    app = QApplication([])
    window = GuiInteractionLayer()
    window.show()
    app.exec()