import time
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

class WorkThread(QObject):
    signal123 = Signal(str)

    def __init__(self):
        super().__init__()
        print('run')

    def work(self):
        for i in range(10):
            self.signal123.emit(str(i))
            print(i)
            time.sleep(1)
        # 请求线程退出事件循环
        self.thread().quit()

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.lb = QLabel('当前的值为:0')



        self.workThread = WorkThread()
        self.threadList = QThread()
        self.workThread.moveToThread(self.threadList)
        self.workThread.signal123.connect(lambda x: self.lb.setText(f'当前的值为:{x}'))

        self.threadList.started.connect(self.workThread.work)
        self.threadList.finished.connect(lambda: print('finished'))
        self.threadList.start()



        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.lb)
        self.setLayout(self.mainLayout)


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
