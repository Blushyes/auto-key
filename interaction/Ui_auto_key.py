# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'auto_key.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtWidgets import (QComboBox, QHBoxLayout, QLabel,
                               QPlainTextEdit, QPushButton, QSizePolicy, QSpinBox,
                               QTabWidget, QTextEdit, QVBoxLayout, QWidget)

ABOUT_MARKDOWN_WRAPPER = u'''
<!DOCTYPE HTML>
<html>
<head>
    <meta name="qrichtext" content="1"/>
    <meta charset="utf-8"/>
    <style>
      p, li {
        white-space: pre-wrap;
      }

      hr {
        height: 1px;
        border-width: 0;
      }

      li.unchecked::marker {
        content: "\\2610";
      }

      li.checked::marker {
        content: "\\2612";
      }
    </style>
</head>
<body style=" font-family:'Microsoft YaHei UI', sans-serif; font-size:9pt; font-weight:400; font-style:normal;">
<p style="-qt-paragraph-type:empty; margin: 12px 0px;-qt-block-indent:0; text-indent:0px;"><br/></p>
</body>
</html>
'''


class Ui_auto_key(object):
    def setupUi(self, auto_key):
        if not auto_key.objectName():
            auto_key.setObjectName(u"auto_key")
        auto_key.resize(329, 633)
        self.verticalLayout_2 = QVBoxLayout(auto_key)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(auto_key)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_main = QWidget()
        self.tab_main.setObjectName(u"tab_main")
        self.verticalLayout = QVBoxLayout(self.tab_main)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_welcome = QLabel(self.tab_main)
        self.label_welcome.setObjectName(u"label_welcome")

        self.verticalLayout.addWidget(self.label_welcome)

        self.label_script_list = QLabel(self.tab_main)
        self.label_script_list.setObjectName(u"label_script_list")

        self.verticalLayout.addWidget(self.label_script_list)

        self.plainTextEdit_script_list = QPlainTextEdit(self.tab_main)
        self.plainTextEdit_script_list.setObjectName(u"plainTextEdit_script_list")
        self.plainTextEdit_script_list.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.plainTextEdit_script_list.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_script_list.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.plainTextEdit_script_list)

        self.label_ask_to_select_script = QLabel(self.tab_main)
        self.label_ask_to_select_script.setObjectName(u"label_ask_to_select_script")

        self.verticalLayout.addWidget(self.label_ask_to_select_script)

        self.comboBox_select_script = QComboBox(self.tab_main)
        self.comboBox_select_script.setObjectName(u"comboBox_select_script")

        self.verticalLayout.addWidget(self.comboBox_select_script)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_redo_times = QLabel(self.tab_main)
        self.label_redo_times.setObjectName(u"label_redo_times")

        self.horizontalLayout_2.addWidget(self.label_redo_times)

        self.spinBox_redo_times = QSpinBox(self.tab_main)
        self.spinBox_redo_times.setObjectName(u"spinBox_redo_times")
        self.spinBox_redo_times.setMinimum(1)
        self.spinBox_redo_times.setMaximum(999999)

        self.horizontalLayout_2.addWidget(self.spinBox_redo_times)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.pushButton_run_script = QPushButton(self.tab_main)
        self.pushButton_run_script.setObjectName(u"pushButton_run_script")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.pushButton_run_script.sizePolicy().hasHeightForWidth())
        self.pushButton_run_script.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.pushButton_run_script)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_edit_script = QPushButton(self.tab_main)
        self.pushButton_edit_script.setObjectName(u"pushButton_edit_script")

        self.horizontalLayout.addWidget(self.pushButton_edit_script)

        self.pushButton_open_script_folder = QPushButton(self.tab_main)
        self.pushButton_open_script_folder.setObjectName(u"pushButton_open_script_folder")

        self.horizontalLayout.addWidget(self.pushButton_open_script_folder)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.pushButton_exit = QPushButton(self.tab_main)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        sizePolicy1.setHeightForWidth(self.pushButton_exit.sizePolicy().hasHeightForWidth())
        self.pushButton_exit.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.pushButton_exit)

        self.label_script_execute_status = QLabel(self.tab_main)
        self.label_script_execute_status.setObjectName(u"label_script_execute_status")

        self.verticalLayout.addWidget(self.label_script_execute_status)

        self.plainTextEdit_script_execute_status = QPlainTextEdit(self.tab_main)
        self.plainTextEdit_script_execute_status.setObjectName(u"plainTextEdit_script_execute_status")

        self.verticalLayout.addWidget(self.plainTextEdit_script_execute_status)

        self.tabWidget.addTab(self.tab_main, "")
        self.tab_about = QWidget()
        self.tab_about.setObjectName(u"tab_about")
        self.verticalLayout_3 = QVBoxLayout(self.tab_about)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.textEdit_about = QTextEdit(self.tab_about)
        self.textEdit_about.setObjectName(u"textEdit_about")

        self.verticalLayout_3.addWidget(self.textEdit_about)

        self.tabWidget.addTab(self.tab_about, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(auto_key)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(auto_key)

    # setupUi

    def retranslateUi(self, auto_key):
        auto_key.setWindowTitle(QCoreApplication.translate("auto_key", u"auto-key", None))
        self.label_welcome.setText(QCoreApplication.translate("auto_key", u"\u6b22\u8fce\u4f7f\u7528auto-key", None))
        self.label_script_list.setText(
            QCoreApplication.translate("auto_key", u"\u83b7\u53d6\u5230\u7684\u811a\u672c\u6709", None))
        self.label_ask_to_select_script.setText(QCoreApplication.translate("auto_key",
                                                                           u"\u8bf7\u95ee\u4f60\u8981\u6267\u884c\u54ea\u4e2a\u811a\u672c\u5462\uff1f",
                                                                           None))
        self.label_redo_times.setText(QCoreApplication.translate("auto_key", u"\u6267\u884c\u6b21\u6570", None))
        self.pushButton_run_script.setText(
            QCoreApplication.translate("auto_key", u"\u8fd0\u884c\u811a\u672c(F6)", None))
        # if QT_CONFIG(shortcut)
        self.pushButton_run_script.setShortcut(QCoreApplication.translate("auto_key", u"F6", None))
        # endif // QT_CONFIG(shortcut)
        self.pushButton_edit_script.setText(QCoreApplication.translate("auto_key", u"\u7f16\u8f91\u811a\u672c", None))
        self.pushButton_open_script_folder.setText(
            QCoreApplication.translate("auto_key", u"\u6253\u5f00\u811a\u672c\u6587\u4ef6\u5939", None))
        self.pushButton_exit.setText(QCoreApplication.translate("auto_key", u"\u9000\u51fa\u7a0b\u5e8f", None))
        self.label_script_execute_status.setText(
            QCoreApplication.translate("auto_key", u"\u811a\u672c\u8fd0\u884c\u72b6\u6001", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_main),
                                  QCoreApplication.translate("auto_key", u"\u4e3b\u754c\u9762", None))

        self.textEdit_about.setHtml(QCoreApplication.translate("auto_key",
                                                               ABOUT_MARKDOWN_WRAPPER,
                                                               None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_about),
                                  QCoreApplication.translate("auto_key", u"\u5173\u4e8e", None))
    # retranslateUi
