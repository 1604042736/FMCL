from importlib import import_module
import logging
import re
import os
import json
import shutil
import sys
import traceback
from zipfile import ZipFile

from PyQt5.QtCore import QCoreApplication, QEvent, QObject, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QMessageBox,
    QWidget,
    QSplashScreen,
)
from qfluentwidgets import RoundMenu, setThemeColor

from Events import *
import FMCL_About
from Setting import Setting, DEFAULT_SETTING_PATH, DEFAULT_SETTING, set_theme, merge
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

        if not os.path.exists(DEFAULT_SETTING_PATH):
            with open(DEFAULT_SETTING_PATH, mode="w", encoding="utf-8") as file:
                file.write("{}")

        import_paths = json.load(open(DEFAULT_SETTING_PATH, encoding="utf-8")).get(
            "system.import_paths", DEFAULT_SETTING["system.import_paths"]
        )
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
        set_theme(Setting().get("system.theme"))

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
        all_about = FMCL_About.about()

        import_paths = Setting()["system.import_paths"]
        for path in import_paths:
            if not os.path.exists(path):
                continue
            for i in os.listdir(path):
                if i == "FMCL":
                    continue
                module_name = i
                if os.path.isfile(os.path.join(path, i)):
                    module_name, _ = os.path.splitext(i)
                try:
                    module = import_module(module_name + ".FMCL_About")
                except:
                    continue
                about = getattr(module, "about", lambda: {})()
                merge(all_about, about)
        return all_about

    @staticmethod
    def getWidgetFromUi(ui_object):
        """通过Ui文件生成代码得到QWidget"""
        widget = QWidget()
        ui = ui_object()
        ui.setupUi(widget)
        return widget
