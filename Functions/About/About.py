import sys
import webbrowser

import qtawesome as qta
from Globals import Globals
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton

from .ui_About import Ui_About

REQUESTMENTS = f"""Python=={sys.version}
minecraft_launcher_lib==5.2
multitasking==0.0.11
Pillow==9.2.0
PyQt5==5.15.7
PyQt5_Frameless_Window==0.1.0
QtAwesome==1.1.1
requests==2.27.1"""

THINKS = (("bangbang93: 提供镜像源", "https://bmclapidoc.bangbang93.com"),
          ("huanghongxun: 提供技术帮助(HMCL)", "https://github.com/huanghongxun/HMCL"))


class About(QWidget, Ui_About):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.information-outline"))

        self.pb_fmcl.setText(
            f"Functional Minecraft Launcher[v{Globals.TAG_NAME}]")

        for i in REQUESTMENTS.split("\n"):
            name, version = i.split("==")
            label = QLabel()
            label.setText(f"{name}[v{version}]")
            self.gl_thirdparty.addWidget(label)

        for name, url in THINKS:
            button = QPushButton()
            button.setText(name)
            button.clicked.connect(lambda _, url=url: webbrowser.open(url))
            self.gl_thinks.addWidget(button)

    @pyqtSlot(bool)
    def on_pb_fmcl_clicked(self, _):
        webbrowser.open("https://github.com/1604042736/FMCL")
