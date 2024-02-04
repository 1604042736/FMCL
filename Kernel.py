import logging
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

import qtawesome as qta
from PyQt5.QtCore import QCoreApplication, QEvent, QObject, Qt, QTranslator, qVersion
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
from Setting import Setting, DEFAULT_SETTING_PATH
from Window import Window

_translate = QCoreApplication.translate


class Kernel(QApplication):
    HELPINDEX_KEYWORD = ("name", "page")  # 帮助索引中的关键字

    def __init__(self, argv: list[str] = sys.argv) -> None:
        super().__init__(argv)
        self.setWindowIcon(QIcon(":/Icon/FMCL.ico"))
        self.setApplicationName("FMCL")
        self.setApplicationVersion("3.3")

        cur_path = os.path.abspath(".")
        if cur_path not in sys.path:
            sys.path.insert(0, cur_path)
        default_path = os.path.abspath("FMCL/Default")
        if default_path not in sys.path:
            sys.path.insert(1, default_path)

        splash = QSplashScreen(QPixmap(":/Image/icon.png").scaled(64, 64))
        splash.show()
        self.processEvents()

        # 在未加载翻译之前不能使用Setting
        tempdir = json.load(open(DEFAULT_SETTING_PATH, encoding="utf-8")).get(
            "system.temp_dir", "FMCL/Temp"
        )
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)

        self.unpack()

        self.loadTranslation()

        logging.info("初始化功能...")
        self.getAllFunctions()

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
    def getTranslationPath():
        default_path = "FMCL/Default/FMCL"
        return (
            (
                (
                    [
                        f"{default_path}/Functions/{i}/Translations"
                        for i in os.listdir("{default_path}/Functions")
                    ]
                )
                if os.path.exists("{default_path}/Functions")
                else []
            )
            + (
                (
                    [
                        f"FMCL/Functions/{i}/Translations"
                        for i in os.listdir("FMCL/Functions")
                    ]
                )
                if os.path.exists("FMCL/Functions")
                else []
            )
            + (
                [
                    f"{default_path}/Translations/{i}"
                    for i in os.listdir(f"{default_path}/Translations")
                    if os.path.isdir(os.path.join(f"{default_path}/Translations", i))
                ]
                if os.path.exists(f"{default_path}/Translations")
                else []
            )
            + (
                [
                    f"FMCL/Translations/{i}"
                    for i in os.listdir("FMCL/Translations")
                    if os.path.isdir(os.path.join("FMCL/Translations", i))
                ]
                if os.path.exists("FMCL/Translations")
                else []
            )
        )

    def loadTranslation(self):
        """加载翻译"""
        logging.info("加载翻译...")
        # 在未加载翻译之前不能使用Setting
        if os.path.exists(DEFAULT_SETTING_PATH):
            lang = (
                json.load(open(DEFAULT_SETTING_PATH, encoding="utf-8")).get(
                    "language.type", "简体中文"
                )
                + ".qm"
            )
        else:
            lang = "简体中文.qm"
        self.__translators = []  # 防止Translator被销毁
        # QTranslator优先搜索最新安装的文件
        for i in self.getTranslationPath():
            file = f"{i}/{lang}"
            if not os.path.exists(file):
                continue
            translator = QTranslator()
            if translator.load(file):
                if self.installTranslator(translator):
                    logging.info(f"已加载{file}")
                    self.__translators.append(translator)
                else:
                    logging.error(f"无法加载{file}")

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

    @staticmethod
    def getFunction(function_name: str):
        """获取功能"""
        # 并不捕获异常而是留给调用者捕获
        if f"FMCL.Functions.{function_name}" in sys.modules:
            return sys.modules[f"FMCL.Functions.{function_name}"]
        function = import_module(f"FMCL.Functions.{function_name}")
        logging.info(f"已获取功能: {function_name}({function}")
        return function

    @staticmethod
    def execFunction(function_name: str, *args, **kwargs):
        """运行功能"""
        # 并不捕获异常而是留给调用者捕获
        function = Kernel.getFunction(function_name)
        logging.info(f"运行:{function_name}")
        return getattr(function, "main")(*args, **kwargs)

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
    def getAllFunctions():
        """获取所有功能"""
        functions = {}
        for functions_path in ("FMCL/Functions", "FMCL/Default/FMCL/Functions"):
            if not os.path.exists(functions_path):
                continue
            for function_name in os.listdir(functions_path):
                try:
                    functions[function_name] = Kernel.getFunction(function_name)
                except:
                    logging.warning(
                        f"功能{function_name}将被忽略:\n{traceback.format_exc()}"
                    )
        return functions.values()

    @staticmethod
    def defaultFunctionInfo(function):
        """默认功能信息"""
        name = function.__name__.split(".")[-1]
        return {"name": name, "id": name, "icon": qta.icon("mdi6.application-outline")}

    @staticmethod
    def getFunctionInfo(function):
        """获取功能信息"""
        info = (
            Kernel.defaultFunctionInfo(function)
            | getattr(function, "functionInfo", lambda: {})()
        )
        return info

    @staticmethod
    def getAllFunctionInfo():
        """获取全部功能信息"""
        function_info = []
        for function in Kernel.getAllFunctions():
            function_info.append(Kernel.getFunctionInfo(function))
        return function_info

    @staticmethod
    def getFunctionHelpIndex(function) -> dict:
        """获得功能的帮助索引"""
        return getattr(function, "helpIndex", lambda: {})()

    @staticmethod
    def getAllFunctionHelpIndex() -> list:
        """获取全部功能的帮助索引"""
        function_helpindex = []
        for function in Kernel.getAllFunctions():
            function_helpindex.append(Kernel.getFunctionHelpIndex(function))
        return function_helpindex

    @staticmethod
    def getHelpIndex() -> dict:
        """获取帮助索引"""

        def merge(a: dict, b: dict):
            for key, val in b.items():
                if key not in a:
                    a[key] = val
                elif isinstance(val, dict) and isinstance(a[key], dict):
                    merge(a[key], val)
                elif isinstance(val, list) and isinstance(a[key], list):
                    a[key].extend(val)
                else:
                    a[key] = val

        helpindex = {}
        for root in ("FMCL/Help", "FMCL/Default/FMCL/Help"):
            if not os.path.exists(root):
                continue
            for i in os.listdir(root):
                try:
                    module = import_module(f"FMCL.Help.{i}")
                    merge(helpindex, getattr(module, "helpIndex", lambda: {})())
                except:
                    logging.error(traceback.format_exc())
        for i in Kernel.getAllFunctionHelpIndex():
            merge(helpindex, i)
        return helpindex

    @staticmethod
    def getHelpIndexAttr(helpindex: dict, id: str):
        """通过id获得帮助索引中的属性"""
        splitid = id.split(".")
        val = helpindex
        for i in splitid:
            val = val[i]
        return val

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
    def getAllLanguages():
        """获取所有语言"""
        lang = []
        for path in Kernel.getTranslationPath():
            if not os.path.exists(path):
                continue
            for i in os.listdir(path):
                full_path = os.path.join(path, i)
                if os.path.isdir(full_path):
                    continue
                name, ext = os.path.splitext(i)
                if ext == ".qm":
                    lang.append(name)
        return set(lang)

    @staticmethod
    def runCommand(command: str):
        function, *args = command.split(maxsplit=1)
        pargs = []
        kwargs = {}
        args = " ".join(args)
        s = ""
        i = 0
        while i < len(args):
            if args[i] == " ":
                if "=" in s:
                    exec(s, kwargs)
                else:
                    pargs.append(eval(s))
                while i < len(args) and args[i] == " ":
                    i += 1
                s = ""
            elif args[i] == "'":
                s += args[i]
                i += 1
                while i < len(args) and args[i] != "'":
                    s += args[i]
                    i += 1
                s += args[i]
                i += 1
            elif i == '"':
                s += args[i]
                i += 1
                while i < len(args) and args[i] != '"':
                    s += args[i]
                    i += 1
                s += args[i]
                i += 1
            else:
                s += args[i]
                i += 1
        if s != "":
            if "=" in s:
                exec(s, kwargs)
            else:
                pargs.append(eval(s))
        Kernel.execFunction(function, *pargs, **kwargs)

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
            ],
        }

    @staticmethod
    def getWidgetFromUi(ui_object):
        """通过Ui文件生成代码得到QWidget"""
        widget = QWidget()
        ui = ui_object()
        ui.setupUi(widget)
        return widget
