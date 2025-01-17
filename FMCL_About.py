import sys
import webbrowser
import multitasking
import PIL
import qfluentwidgets
import qframelesswindow
import requests
import toml
import python_nbt
import psutil
import watchdog.version

import qtawesome as qta
from PyQt5.QtCore import QCoreApplication, qVersion
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    qApp,
)

from Events import *
from PyQt5.Qsci import QSCINTILLA_VERSION_STR

_translate = QCoreApplication.translate


def about():
    return {
        "launcher": [
            {
                "name": f"Functional Minecraft Launcher",
                "description": f"v{qApp.applicationVersion()}",
                "icon": QPixmap(":/Image/icon.png"),
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/wyj2006/FMCL"
                        ),
                        "name": "GitHub",
                    },
                ),
            }
        ],
        "thanks": [
            {
                "name": "bangbang93",
                "description": _translate("About", "提供镜像源"),
                "icon": QPixmap(":/Image/bangbang93.jpg"),
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://bmclapidoc.bangbang93.com/"
                        ),
                        "name": _translate("About", "官网"),
                    },
                    {
                        "action": lambda: webbrowser.open(
                            "https://afdian.net/a/bangbang93"
                        ),
                        "name": _translate("About", "赞助"),
                    },
                ),
            },
            {
                "name": "HMCL",
                "description": _translate("About", "提供技术帮助"),
                "icon": QPixmap(":/Image/hmcl.png"),
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://hmcl.huangyuhui.net/"
                        ),
                        "name": _translate("About", "官网"),
                    },
                    {
                        "action": lambda: webbrowser.open(
                            "https://afdian.net/a/huanghongxun"
                        ),
                        "name": _translate("About", "赞助"),
                    },
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/huanghongxun/HMCL"
                        ),
                        "name": "GitHub",
                    },
                ),
            },
            {
                "name": "PCL",
                "description": _translate("About", "提供技术帮助"),
                "icon": QPixmap(":/Image/pcl.png"),
                "operators": (
                    {
                        "action": lambda: webbrowser.open("https://afdian.net/a/LTCat"),
                        "name": _translate("About", "赞助"),
                    },
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/Hex-Dragon/PCL2"
                        ),
                        "name": "GitHub",
                    },
                ),
            },
        ],
        "3rdparty": [
            {
                "name": "Python",
                "description": sys.version,
                "icon": None,
                "operators": (
                    {
                        "action": lambda: webbrowser.open("https://www.python.org"),
                        "name": _translate("About", "官网"),
                    },
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/python/cpython"
                        ),
                        "name": "Github",
                    },
                ),
            },
            {
                "name": "minecraft_launcher_lib",
                "description": "v6.1",
                "icon": None,
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/BobDotCom/minecraft-launcher-lib"
                        ),
                        "name": "GitHub",
                    },
                ),
            },
            {
                "name": "multitasking",
                "description": "v" + multitasking.__version__,
                "icon": None,
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/ranaroussi/multitasking"
                        ),
                        "name": "GitHub",
                    },
                ),
            },
            {
                "name": "Pillow",
                "description": "v" + PIL.__version__,
                "icon": None,
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/python-pillow/Pillow"
                        ),
                        "name": "GitHub",
                    },
                ),
            },
            {
                "name": "PyQt5",
                "description": "v" + qVersion(),
                "icon": None,
                "operators": (
                    {"action": qApp.aboutQt, "name": _translate("About", "关于Qt")},
                    {
                        "action": lambda: webbrowser.open("https://www.qt.io"),
                        "name": _translate("About", "官网"),
                    },
                ),
            },
            {
                "name": "PyQt-Fluent-Widgets",
                "description": "v" + qfluentwidgets.__version__,
                "icon": None,
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://afdian.net/a/zhiyiYo"
                        ),
                        "name": _translate("About", "赞助"),
                    },
                    {
                        "action": lambda: webbrowser.open(
                            "https://qfluentwidgets.com/"
                        ),
                        "name": _translate("About", "官网"),
                    },
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/zhiyiYo/PyQt-Fluent-Widgets"
                        ),
                        "name": "GitHub",
                    },
                ),
            },
            {
                "name": "PyQt5_Frameless_Window",
                "description": "v" + qframelesswindow.__version__,
                "icon": None,
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://afdian.net/a/zhiyiYo"
                        ),
                        "name": _translate("About", "赞助"),
                    },
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/zhiyiYo/PyQt-Frameless-Window"
                        ),
                        "name": "GitHub",
                    },
                ),
            },
            {
                "name": "requests",
                "description": "v" + requests.__version__,
                "icon": None,
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/psf/requests"
                        ),
                        "name": "GitHub",
                    },
                ),
            },
            {
                "name": "toml",
                "description": "v" + toml.__version__,
                "icon": None,
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/uiri/toml"
                        ),
                        "name": "GitHub",
                    },
                ),
            },
            {
                "name": "Python-NBT",
                "description": "v" + ".".join(map(str, python_nbt.VERSION)),
                "icon": None,
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/TowardtheStars/Python-NBT"
                        ),
                        "name": "GitHub",
                    },
                ),
            },
            {
                "name": "qtawesome",
                "description": f"v{qta.__version__}",
                "icon": None,
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/spyder-ide/qtawesome"
                        ),
                        "name": "GitHub",
                    },
                ),
            },
            {
                "name": "psutil",
                "description": f"v{psutil.__version__}",
                "icon": None,
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/giampaolo/psutil"
                        ),
                        "name": "GitHub",
                    },
                ),
            },
            {
                "name": "watchdog",
                "description": f"v{watchdog.version.VERSION_STRING}",
                "icon": None,
                "operators": (
                    {
                        "action": lambda: webbrowser.open(
                            "https://github.com/gorakhargosh/watchdog"
                        ),
                        "name": "GitHub",
                    },
                ),
            },
            {
                "name": "QScintilla",
                "description": f"v{QSCINTILLA_VERSION_STR}",
                "icon": None,
                "operators": (
                    {
                        "action": lambda: webbrowser.open("https://www.scintilla.org/"),
                        "name": _translate("About", "官网"),
                    },
                ),
            },
        ],
    }
