import sys
import webbrowser

import multitasking
import PIL
import qfluentwidgets
import qframelesswindow
import qtawesome as qta
import requests
import toml
import python_nbt
from PyQt5.QtCore import qVersion
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, qApp
from .AboutItem import AboutItem
from .ui_About import Ui_About


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
                        lambda: webbrowser.open("https://github.com/1604042736/FMCL"),
                        "GitHub",
                    ),
                )
            ],
            "thanks": [
                (
                    "bangbang93",
                    self.tr("提供镜像源"),
                    QPixmap(":/Image/bangbang93.jpg"),
                    (
                        lambda: webbrowser.open("https://afdian.net/a/bangbang93"),
                        self.tr("赞助"),
                    ),
                ),
                (
                    "HMCL",
                    self.tr("提供技术帮助"),
                    QPixmap(":/Image/hmcl.png"),
                    (
                        lambda: webbrowser.open("https://github.com/huanghongxun/HMCL"),
                        "GitHub",
                    ),
                ),
                (
                    "PCL",
                    self.tr("提供技术帮助"),
                    QPixmap(":/Image/pcl.png"),
                    (
                        lambda: webbrowser.open("https://github.com/Hex-Dragon/PCL2"),
                        "GitHub",
                    ),
                ),
            ],
            "3rdparty": [
                (
                    "Python",
                    sys.version,
                    None,
                    (lambda: webbrowser.open("https://www.python.org"), self.tr("官网")),
                ),
                (
                    "minecraft_launcher_lib",
                    "v6.1",
                    None,
                    (
                        lambda: webbrowser.open(
                            "https://github.com/BobDotCom/minecraft-launcher-lib"
                        ),
                        "GitHub",
                    ),
                ),
                (
                    "multitasking",
                    "v" + multitasking.__version__,
                    None,
                    (
                        lambda: webbrowser.open(
                            "https://github.com/ranaroussi/multitasking"
                        ),
                        "GitHub",
                    ),
                ),
                (
                    "Pillow",
                    "v" + PIL.__version__,
                    None,
                    (
                        lambda: webbrowser.open(
                            "https://github.com/python-pillow/Pillow"
                        ),
                        "GitHub",
                    ),
                ),
                ("PyQt5", "v" + qVersion(), None, (qApp.aboutQt, self.tr("关于Qt"))),
                (
                    "PyQt-Fluent-Widgets",
                    "v" + qfluentwidgets.__version__,
                    None,
                    (
                        lambda: webbrowser.open(
                            "https://github.com/zhiyiYo/PyQt-Fluent-Widgets"
                        ),
                        "GitHub",
                    ),
                ),
                (
                    "PyQt5_Frameless_Window",
                    "v" + qframelesswindow.__version__,
                    None,
                    (
                        lambda: webbrowser.open(
                            "https://github.com/zhiyiYo/PyQt-Frameless-Window"
                        ),
                        "GitHub",
                    ),
                ),
                (
                    "requests",
                    "v" + requests.__version__,
                    None,
                    (
                        lambda: webbrowser.open("https://github.com/psf/requests"),
                        "GitHub",
                    ),
                ),
                (
                    "toml",
                    "v" + toml.__version__,
                    None,
                    (lambda: webbrowser.open("https://github.com/uiri/toml"), "GitHub"),
                ),
                (
                    "Python-NBT",
                    "v" + ".".join(map(str, python_nbt.VERSION)),
                    None,
                    (
                        lambda: webbrowser.open(
                            "https://github.com/TowardtheStars/Python-NBT"
                        ),
                        "GitHub",
                    ),
                ),
            ],
        }

        for key, val in self.ABOUT.items():
            gl = getattr(self, f"gl_{key}")
            for i in val:
                widget = AboutItem(*i)
                gl.addWidget(widget)
