import sys
import webbrowser

import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, qApp

from .AboutItem import AboutItem
from .ui_About import Ui_About

_translate = QCoreApplication.translate


class About(QWidget, Ui_About):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.information-outline"))

        self.ABOUT = {
            "launcher": [
                (
                    f"Functional Minecraft Launcher",
                    f"v{qApp.applicationVersion()}",
                    QPixmap(":/Image/icon.png"),
                    (
                        lambda:webbrowser.open(
                            "https://github.com/1604042736/FMCL"),
                        "GitHub"
                    )
                )
            ],
            "thanks": [
                (
                    "bangbang93",
                    _translate("About", "提供镜像源"),
                    QPixmap(":/Image/bangbang93.jpg"),
                    (
                        lambda:webbrowser.open(
                            "https://afdian.net/a/bangbang93"),
                        _translate("About", "赞助")
                    )
                ),
                (
                    "HMCL",
                    _translate("About", "提供技术帮助"),
                    QPixmap(":/Image/hmcl.png"),
                    (
                        lambda:webbrowser.open(
                            "https://github.com/huanghongxun/HMCL"),
                        "GitHub"
                    )
                )
            ],
            "3rdparty": [
                (
                    "Python",
                    sys.version,
                    None,
                    (
                        lambda:webbrowser.open("https://www.python.org"),
                        _translate("About", "官网")
                    )
                ),
                (
                    "minecraft_launcher_lib",
                    "v5.3",
                    None,
                    (
                        lambda:webbrowser.open(
                            "https://github.com/BobDotCom/minecraft-launcher-lib"),
                        "GitHub"
                    )
                ),
                (
                    "multitasking",
                    "v0.0.11",
                    None,
                    (
                        lambda:webbrowser.open(
                            "https://github.com/ranaroussi/multitasking"),
                        "GitHub"
                    )
                ),
                (
                    "Pillow",
                    "v9.4.0",
                    None,
                    (
                        lambda:webbrowser.open(
                            "https://github.com/python-pillow/Pillow"),
                        "GitHub"
                    )
                ),
                (
                    "PyQt5",
                    "v5.15.9",
                    None,
                    (
                        qApp.aboutQt,
                        _translate("About", "关于Qt")
                    )
                ),
                (
                    "PyQt5_Frameless_Window",
                    "v0.2.3",
                    None,
                    (
                        lambda:webbrowser.open(
                            "https://github.com/zhiyiYo/PyQt-Frameless-Window"),
                        "GitHub"
                    )
                ),
                ("PyQtWebEngine", "v5.15.6"),
                (
                    "QtAwesome",
                    "v1.2.3",
                    None,
                    (
                        lambda:webbrowser.open(
                            "https://github.com/spyder-ide/qtawesome"),
                        "GitHub"
                    )
                ),
                (
                    "requests",
                    "v2.28.2",
                    None,
                    (
                        lambda:webbrowser.open(
                            "https://github.com/psf/requests"),
                        "GitHub"
                    )
                ),
                (
                    "toml",
                    "v0.10.2",
                    None,
                    (
                        lambda:webbrowser.open("https://github.com/uiri/toml"),
                        "GitHub"
                    )
                )
            ]
        }

        for key, val in self.ABOUT.items():
            gl = getattr(self, f"gl_{key}")
            for i in val:
                widget = AboutItem(*i)
                gl.addWidget(widget)
