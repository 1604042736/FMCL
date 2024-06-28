import logging
import re
import os
import json
import shutil
import sys
import traceback
import webbrowser
from importlib import import_module
from zipfile import *
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
from PyQt5.QtCore import QCoreApplication, QEvent, QObject, Qt, qVersion
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QMessageBox,
    QWidget,
    qApp,
    QSplashScreen,
)
from qfluentwidgets import RoundMenu, setThemeColor

from Events import *
from Setting import Setting, DEFAULT_SETTING_PATH, DEFAULT_SETTING
from Window import Window
from Core.Function import Function
from Core.Translation import Translation
from Core.Help import Help

_translate = QCoreApplication.translate


class Kernel(QApplication):
    HELPINDEX_KEYWORD = ("name", "page")  # 帮助索引中的关键字

    def __init__(self, argv: list[str] = sys.argv) -> None:
        super().__init__(argv)
        self.setWindowIcon(QIcon(":/Icon/FMCL.ico"))
        self.setApplicationName("FMCL")
        self.setApplicationVersion("3.4")

        cur_path = os.path.abspath(".")
        if cur_path not in sys.path:
            sys.path.insert(0, cur_path)
        default_path = os.path.abspath("FMCL/Default")
        if default_path not in sys.path:
            sys.path.insert(1, default_path)

        import_paths = json.load(open(DEFAULT_SETTING_PATH, encoding="utf-8")).get(
            "system.import_paths", DEFAULT_SETTING["system.import_paths"]
        )
        try:
            index = sys.argv.index("-I") + 1
            import_paths.extends(sys.argv[index].split(";"))
        except:
            pass
        i = 2
        for path in import_paths:
            path = os.path.abspath(path)
            if path not in sys.path:
                Function.PATH.append(os.path.join(path, "FMCL", "Functions"))
                Translation.PATH.append(os.path.join(path, "FMCL", "Translations"))
                Help.PATH.append(os.path.join(path, "FMCL", "Help"))
                sys.path.insert(i, path)
                i += 1

        splash = QSplashScreen(QPixmap(":/Image/icon.png").scaled(64, 64))
        splash.setWindowFlags(splash.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        splash.show()
        self.processEvents()

        if not os.path.exists(DEFAULT_SETTING_PATH):
            with open(DEFAULT_SETTING_PATH, mode="w", encoding="utf-8") as file:
                file.write("{}")

        # 在未加载翻译之前不能使用Setting
        tempdir = json.load(open(DEFAULT_SETTING_PATH, encoding="utf-8")).get(
            "system.temp_dir", DEFAULT_SETTING["system.temp_dir"]
        )
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)

        self.unpack()

        Translation.load(self)

        logging.info("初始化功能...")
        Function.get_all()

        setThemeColor(Setting().get("system.theme_color"))

        logging.info("运行启动项...")
        self.execStartupFunctions()

        splash.close()

    def notify(self, a0: QObject, a1: QEvent) -> bool:
        if a1.type() == SeparateWidgetEvent.EventType:
            a1.widget.resize(a1.size)
            self.separateWidget(a1.widget)
        elif (
            isinstance(a0, QWidget)
            and not isinstance(a0, Window)
            and not isinstance(a0, QDialog)
            and not isinstance(a0, RoundMenu)
            and not isinstance(a0, QSplashScreen)
            and a0.windowType() != Qt.WindowType.ToolTip
        ):
            if a1.type() == QEvent.Type.Show:
                if a0.parent() == None:
                    self.sendEvent(self, WidgetCaughtEvent(a0))
                    if a0.parent() == None:  # 使用默认方法
                        self.showWidget(a0)
        if (
            isinstance(a0, QWidget)
            and a0.window() == a0
            and a1.type() == QEvent.Type.WindowActivate
        ):
            self.sendEvent(self, WindowActivatedEvent(a0))
        return super().notify(a0, a1)

    def separateWidget(self, widget: QWidget):
        """分离控件"""
        self.showWidget(widget)

    @staticmethod
    def unpack():
        if os.path.exists("FMCL/Default"):
            shutil.rmtree("FMCL/Default")
        # 由Scripts/Pack.py生成打包文件
        logging.info("解压...")
        try:
            from Pack.Default import zipfile_bytes
        except ImportError:
            pass
        else:
            zip = ZipFile(zipfile_bytes)
            for path in zip.namelist():
                functions_path = "FMCL/Default/FMCL"
                logging.info(f"解压:{path}")
                zip.extract(path, functions_path)
            zip.close()

    def execStartupFunctions(self):
        """运行启动项"""
        actions = Setting()["system.startup_functions"]
        for action in actions:
            for command in action["commands"]:
                try:
                    self.runCommand(command)
                except:
                    title = _translate("Kernel", "无法运行") + command
                    msg = traceback.format_exc()
                    logging.error(f"{title}:\n{msg}")
                    QMessageBox.critical(None, title, msg)

    @staticmethod
    def activateWidget(widget: QWidget):
        """激活一个控件"""
        if not widget.isVisible():
            widget.show()  # 自己要显示
            widget.window().show()  # 自己的窗口也得显示
        widget.activateWindow()

    @staticmethod
    def showWidget(widget: QWidget):
        """使用Window来显示控件"""
        window = Window(widget)
        window.show()

    @staticmethod
    def runCommand(command: str):
        function, *args = command.split(maxsplit=1)
        pargs = []
        kwargs = {}
        args = " ".join(args)
        pattern = r"""'.*?'|".*?"|\S+"""
        for s in re.findall(pattern, args):
            if s == "":
                continue
            if "=" in s:
                exec(s, kwargs)
            else:
                pargs.append(eval(s))
        Function(function).exec(*pargs, **kwargs)

    @staticmethod
    def getAbout():
        return {
            "launcher": [
                (
                    f"Functional Minecraft Launcher",
                    f"v{qApp.applicationVersion()}",
                    QPixmap(":/Image/icon.png"),
                    (
                        (
                            lambda: webbrowser.open(
                                "https://github.com/1604042736/FMCL"
                            ),
                            "GitHub",
                        ),
                    ),
                )
            ],
            "thanks": [
                (
                    "bangbang93",
                    _translate("About", "提供镜像源"),
                    QPixmap(":/Image/bangbang93.jpg"),
                    (
                        (
                            lambda: webbrowser.open(
                                "https://bmclapidoc.bangbang93.com/"
                            ),
                            _translate("About", "官网"),
                        ),
                        (
                            lambda: webbrowser.open("https://afdian.net/a/bangbang93"),
                            _translate("About", "赞助"),
                        ),
                    ),
                ),
                (
                    "HMCL",
                    _translate("About", "提供技术帮助"),
                    QPixmap(":/Image/hmcl.png"),
                    (
                        (
                            lambda: webbrowser.open("https://hmcl.huangyuhui.net/"),
                            _translate("About", "官网"),
                        ),
                        (
                            lambda: webbrowser.open(
                                "https://afdian.net/a/huanghongxun"
                            ),
                            _translate("About", "赞助"),
                        ),
                        (
                            lambda: webbrowser.open(
                                "https://github.com/huanghongxun/HMCL"
                            ),
                            "GitHub",
                        ),
                    ),
                ),
                (
                    "PCL",
                    _translate("About", "提供技术帮助"),
                    QPixmap(":/Image/pcl.png"),
                    (
                        (
                            lambda: webbrowser.open("https://afdian.net/a/LTCat"),
                            _translate("About", "赞助"),
                        ),
                        (
                            lambda: webbrowser.open(
                                "https://github.com/Hex-Dragon/PCL2"
                            ),
                            "GitHub",
                        ),
                    ),
                ),
            ],
            "3rdparty": [
                (
                    "Python",
                    sys.version,
                    None,
                    (
                        (
                            lambda: webbrowser.open("https://www.python.org"),
                            _translate("About", "官网"),
                        ),
                        (
                            lambda: webbrowser.open(
                                "https://github.com/python/cpython"
                            ),
                            "Github",
                        ),
                    ),
                ),
                (
                    "minecraft_launcher_lib",
                    "v6.1",
                    None,
                    (
                        (
                            lambda: webbrowser.open(
                                "https://github.com/BobDotCom/minecraft-launcher-lib"
                            ),
                            "GitHub",
                        ),
                    ),
                ),
                (
                    "multitasking",
                    "v" + multitasking.__version__,
                    None,
                    (
                        (
                            lambda: webbrowser.open(
                                "https://github.com/ranaroussi/multitasking"
                            ),
                            "GitHub",
                        ),
                    ),
                ),
                (
                    "Pillow",
                    "v" + PIL.__version__,
                    None,
                    (
                        (
                            lambda: webbrowser.open(
                                "https://github.com/python-pillow/Pillow"
                            ),
                            "GitHub",
                        ),
                    ),
                ),
                (
                    "PyQt5",
                    "v" + qVersion(),
                    None,
                    (
                        (qApp.aboutQt, _translate("About", "关于Qt")),
                        (
                            lambda: webbrowser.open("https://www.qt.io"),
                            _translate("About", "官网"),
                        ),
                    ),
                ),
                (
                    "PyQt-Fluent-Widgets",
                    "v" + qfluentwidgets.__version__,
                    None,
                    (
                        (
                            lambda: webbrowser.open("https://afdian.net/a/zhiyiYo"),
                            _translate("About", "赞助"),
                        ),
                        (
                            lambda: webbrowser.open("https://qfluentwidgets.com/"),
                            _translate("About", "官网"),
                        ),
                        (
                            lambda: webbrowser.open(
                                "https://github.com/zhiyiYo/PyQt-Fluent-Widgets"
                            ),
                            "GitHub",
                        ),
                    ),
                ),
                (
                    "PyQt5_Frameless_Window",
                    "v" + qframelesswindow.__version__,
                    None,
                    (
                        (
                            lambda: webbrowser.open("https://afdian.net/a/zhiyiYo"),
                            _translate("About", "赞助"),
                        ),
                        (
                            lambda: webbrowser.open(
                                "https://github.com/zhiyiYo/PyQt-Frameless-Window"
                            ),
                            "GitHub",
                        ),
                    ),
                ),
                (
                    "requests",
                    "v" + requests.__version__,
                    None,
                    (
                        (
                            lambda: webbrowser.open("https://github.com/psf/requests"),
                            "GitHub",
                        ),
                    ),
                ),
                (
                    "toml",
                    "v" + toml.__version__,
                    None,
                    (
                        (
                            lambda: webbrowser.open("https://github.com/uiri/toml"),
                            "GitHub",
                        ),
                    ),
                ),
                (
                    "Python-NBT",
                    "v" + ".".join(map(str, python_nbt.VERSION)),
                    None,
                    (
                        (
                            lambda: webbrowser.open(
                                "https://github.com/TowardtheStars/Python-NBT"
                            ),
                            "GitHub",
                        ),
                    ),
                ),
                (
                    "qtawesome",
                    f"v{qta.__version__}",
                    None,
                    (
                        (
                            lambda: webbrowser.open(
                                "https://github.com/spyder-ide/qtawesome"
                            ),
                            "GitHub",
                        ),
                    ),
                ),
                (
                    "psutil",
                    f"v{psutil.__version__}",
                    None,
                    (
                        (
                            lambda: webbrowser.open(
                                "https://github.com/giampaolo/psutil"
                            ),
                            "GitHub",
                        ),
                    ),
                ),
                (
                    "watchdog",
                    f"v{watchdog.version.VERSION_STRING}",
                    None,
                    (
                        (
                            lambda: webbrowser.open(
                                "https://github.com/gorakhargosh/watchdog"
                            ),
                            "GitHub",
                        ),
                    ),
                ),
            ],
        }

    @staticmethod
    def getWidgetFromUi(ui_object):
        """通过Ui文件生成代码得到QWidget"""
        widget = QWidget()
        ui = ui_object()
        ui.setupUi(widget)
        return widget
