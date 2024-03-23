import os
import sys
from executor.main import ScriptExecutor
from executor.simple import SimpleExecutor
from script_loader.excel_loader import ExcelLoader
from script_loader.main import pick_scripts, ScriptInfo, ScriptLoader, KeyScript
from interaction.Ui_auto_key import Ui_auto_key
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QThread, Signal, QObject


class Command:
    EXIT: str = 'exit'


# # 重定向 print 输出 到 图形界面
class RedirectOutput(QObject):
    # 创建一个信号，用于将输出传递回主线程
    output_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.stdout = None
        self.stderr = None

    def write(self, message):
        # 发送输出信号
        self.output_signal.emit(message)

    def flush(self):
        # Python 3要求实现flush方法
        pass

    def start(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def stop(self):
        if self.stdout:
            sys.stdout = self.stdout
        if self.stderr:
            sys.stderr = self.stderr



# 多线程执行脚本，避免阻塞图形界面
class WorkThread(QObject):
    signal123 = Signal(str)

    def __init__(self, redirect_output, script_info, key_scripts):
        super().__init__()
        self.redirect_output = redirect_output
        self.script_info = script_info
        self.key_scripts = key_scripts

    def work(self):
        # 重定向 print 输出 到 图形界面
        self.redirect_output.start()
        # 执行脚本
        executor: ScriptExecutor = SimpleExecutor(self.script_info)
        executor.execute(self.key_scripts)
        # 停止重定向 print 输出
        self.redirect_output.stop()
        # 请求线程退出事件循环
        self.thread().quit()


class GuiInteractionLayer(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_auto_key()
        self.ui.setupUi(self)
        self.setup_signals()


    def setup_signals(self) -> None:
        # 获取脚本列表
        self.scripts_list: list[ScriptInfo] = pick_scripts()
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

        # 多线程执行脚本，避免阻塞图形界面
        self.ui.plainTextEdit_script_execute_status.appendPlainText(f'脚本 “ {select_script} ” 执行中...')
        # 重定向 print 输出 到 图形界面
        redirect_output = RedirectOutput()
        redirect_output.output_signal.connect(self.ui.plainTextEdit_script_execute_status.appendPlainText)
        # 获取脚本信息
        script_info = self.scripts_list[select_script_index -1]  # 因为显示时从 1 开始计数，所以需要减 1
        # 设置线程
        self.workThread = WorkThread(redirect_output, script_info, key_scripts)
        self.threadList = QThread()
        self.workThread.moveToThread(self.threadList)
        self.threadList.started.connect(self.workThread.work)
        self.threadList.finished.connect(self.threadList_finished)
        # 启动线程
        self.threadList.start()
        # 停用 运行脚本 按钮
        self.ui.pushButton_run_script.setEnabled(False)
        
    def threadList_finished(self) -> None:
        self.threadList.quit()  # 请求线程退出事件循环
        self.threadList.wait()  # 等待线程完成
        self.threadList.deleteLater()  # 删除线程对象
        self.ui.plainTextEdit_script_execute_status.appendPlainText(f'脚本执行停止')
        # 启用 运行脚本 按钮
        self.ui.pushButton_run_script.setEnabled(True)


def start():
    app = QApplication([])
    window = GuiInteractionLayer()
    window.show()
    app.exec()