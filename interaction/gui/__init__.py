import os
import sys
from pathlib import Path

from PySide6.QtCore import QThread, Signal, QObject, QTimer
from PySide6.QtWidgets import QApplication, QWidget
from markdown2 import markdown

from executor import execute, ScriptStep
from executor.external import Cosmic
from interaction import InteractionLayer
from interaction.gui.Ui_auto_key import Ui_auto_key
from interaction.gui.shortcut_handler import bond_shortcut
from script_loader import pick_scripts, ScriptInfo
from script_loader.excel.__init__ import ExcelLoader
from script_loader.interfaces import ScriptLoader


class Command:
    EXIT: str = "exit"


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

    def __init__(
        self,
        redirect_output,
        script_info: ScriptInfo,
        key_scripts: list[ScriptStep],
        redo_times,
    ):
        super().__init__()
        self.redirect_output = redirect_output
        self.script_info = script_info
        self.key_scripts = key_scripts
        self.redo_times = redo_times

    def work(self):
        # 重定向 print 输出 到 图形界面
        self.redirect_output.start()

        # 执行脚本
        for i in range(self.redo_times):
            execute(self.script_info, self.key_scripts)
            if Cosmic.pause_executor:
                self.signal123.emit(f"脚本执行被手动暂停")
                break
            self.signal123.emit(f"脚本执行完成，第 {i + 1} 次")

        # 停止重定向 print 输出
        self.redirect_output.stop()

        # 请求线程退出事件循环
        self.thread().quit()


class GuiInteractionLayer(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_auto_key()
        self.ui.setupUi(self)
        self.set_markdown("README.md")
        self.setup_signals()

    def set_markdown(self, markdown_file_path):
        # 读取Markdown文件
        with open(markdown_file_path, "r", encoding="utf-8") as file:
            markdown_text = file.read()
        # 将Markdown文本转换为HTML
        html_text = markdown(markdown_text)
        # 将HTML文本设置到QTextEdit中
        self.ui.textEdit_about.setHtml(html_text)

    def setup_signals(self) -> None:
        # 初始无脚本运行，停用 暂停脚本 按钮
        self.ui.pushButton_pause_script.setEnabled(False)
        # 获取脚本列表
        self.scripts_list: list[ScriptInfo] = pick_scripts()
        # 显示脚本列表
        for i, script in enumerate(self.scripts_list):
            # 从 1 开始计数
            self.ui.plainTextEdit_script_list.appendPlainText(f"{i + 1}. {script.name}")
            self.ui.comboBox_select_script.addItem(f"{i + 1}. {script.name}")

        # 连接 运行脚本 按钮 信号/槽
        self.ui.pushButton_run_script.clicked.connect(self.run_script)
        # 连接 暂停脚本 按钮 信号/槽
        self.ui.pushButton_pause_script.clicked.connect(self.pause_script)
        # 连接 退出 按钮 信号/槽
        self.ui.pushButton_exit.clicked.connect(self.close)
        # 限制文本框字数，自动清空
        self.ui.plainTextEdit_script_execute_status.textChanged.connect(
            self.auto_clear_execute_status
        )
        # 连接 编辑脚本 按钮 信号/槽
        self.ui.pushButton_edit_script.clicked.connect(self.edit_script)
        # 连接 打开脚本文件夹 按钮 信号/槽
        self.ui.pushButton_open_script_folder.clicked.connect(self.open_script_folder)
        # 绑定系统全局快捷键
        bond_shortcut()
        # 定时检查 cosmic 启动/暂停脚本 快捷键执行需求
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_cosmic_do_run_or_pause_scripts_status)
        self.timer.start(200)

    def check_cosmic_do_run_or_pause_scripts_status(self) -> None:
        if Cosmic.do_run_script:
            self.run_script()
            Cosmic.do_run_script = False

        if Cosmic.do_pause_script:
            self.pause_script()
            Cosmic.do_pause_script = False

    def get_select_path(self):
        try:
            # 获取用户输入的脚本序号
            self.select_script = self.ui.comboBox_select_script.currentText()
            self.select_script_index = int(self.select_script.split(".")[0])
        except Exception as e:
            self.ui.plainTextEdit_script_execute_status.appendPlainText(
                f"脚本格式错误！！！{e}"
            )
            return

        # TODO 可以根据 meta.json 配置脚本类型如：Excel等
        if (
            self.select_script_index > len(self.scripts_list)
            or self.select_script_index < 0
        ):
            self.ui.plainTextEdit_script_execute_status.appendPlainText(
                f"不存在的脚本 “ {self.select_script} ” ！！！"
            )
            return

        # 获取用户输入的脚本序号
        # 因为显示时从 1 开始计数，所以需要减 1
        self.select_path = Path(self.scripts_list[self.select_script_index - 1].path)

    def run_script(self) -> None:
        Cosmic.pause_executor = False  # 恢复手动暂停标志
        self.get_select_path()
        # 加载脚本路径
        loader: ScriptLoader = ExcelLoader()
        key_scripts: list[ScriptStep] = loader.loads(self.select_path)

        # 多线程执行脚本，避免阻塞图形界面
        self.ui.plainTextEdit_script_execute_status.appendPlainText(
            f"脚本 “ {self.select_script} ” 执行中..."
        )
        # 重定向 print 输出 到 图形界面
        redirect_output = RedirectOutput()
        redirect_output.output_signal.connect(
            self.ui.plainTextEdit_script_execute_status.appendPlainText
        )
        # 获取脚本信息
        script_info = self.scripts_list[
            self.select_script_index - 1
        ]  # 因为显示时从 1 开始计数，所以需要减 1
        # 获取执行次数
        redo_times = self.ui.spinBox_redo_times.value()
        # 设置线程
        self.workThread = WorkThread(
            redirect_output, script_info, key_scripts, redo_times
        )
        self.threadList = QThread()
        self.workThread.moveToThread(self.threadList)
        self.workThread.signal123.connect(
            self.ui.plainTextEdit_script_execute_status.appendPlainText
        )
        self.threadList.started.connect(self.workThread.work)
        self.threadList.finished.connect(self.threadList_finished)
        # 启动线程
        self.threadList.start()
        # 停用 运行脚本 按钮
        self.ui.pushButton_run_script.setEnabled(False)
        # 启用 暂停脚本 按钮
        self.ui.pushButton_pause_script.setEnabled(True)
        # 停用 退出 按钮
        self.ui.pushButton_exit.setEnabled(False)

    def threadList_finished(self) -> None:
        self.threadList.quit()  # 请求线程退出事件循环
        self.threadList.wait()  # 等待线程完成
        self.threadList.deleteLater()  # 删除线程对象
        self.ui.plainTextEdit_script_execute_status.appendPlainText(f"脚本执行停止")
        # 启用 运行脚本 按钮
        self.ui.pushButton_run_script.setEnabled(True)
        # 启用 退出 按钮
        self.ui.pushButton_exit.setEnabled(True)

    def pause_script(self) -> None:
        Cosmic.pause_executor = True  # 设置手动暂停标志
        self.ui.pushButton_run_script.setEnabled(True)
        self.ui.pushButton_pause_script.setEnabled(False)
        self.ui.pushButton_exit.setEnabled(True)

    def edit_script(self) -> None:
        self.get_select_path()
        # 拼接 index.xlsx 路径
        self.xlsx_path = self.select_path / "index.xlsx"
        # 打开脚本文件
        os.system(f"start excel {self.xlsx_path}")

    def open_script_folder(self) -> None:
        self.get_select_path()
        # 打开脚本文件夹
        print(f"打开脚本文件夹：{self.select_path}")
        os.system(f'start explorer "{self.select_path}"')

    # 限制文本框字数，自动清空
    def auto_clear_execute_status(self) -> None:
        if len(self.ui.plainTextEdit_script_execute_status.toPlainText()) > 10000:
            self.ui.plainTextEdit_script_execute_status.clear()


class QTGUIInteractionLayer(InteractionLayer):
    def start(self) -> None:
        app = QApplication([])
        window = GuiInteractionLayer()
        window.show()
        app.exec()
