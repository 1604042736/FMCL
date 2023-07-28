import json
import logging
import os
import sys
import traceback
from importlib import import_module
from zipfile import *

import qtawesome as qta
from PyQt5.QtCore import QEvent, QObject, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QWidget
from qfluentwidgets import RoundMenu

from Events import *
from Exceptions import *
from Setting import Setting
from Window import Window


class Kernel(QApplication):
    tasks = set()
    translation = {}  # 翻译

    def __init__(self, argv: list[str] = sys.argv) -> None:
        super().__init__(argv)
        self.setWindowIcon(QIcon(":/Icon/FMCL.ico"))
        self.setApplicationName("FMCL")
        self.setApplicationVersion("3.2")

        cur_path = os.path.abspath(".")
        if cur_path not in sys.path:
            sys.path.insert(0, os.path.abspath("."))

        if "--notunpack" not in argv:
            self.unpack()
        self.loadTranslation()

        logging.debug("初始化功能...")
        self.getAllFunctions()
        logging.debug("运行启动项...")
        self.execStartupFunctions()

    def notify(self, a0: QObject, a1: QEvent) -> bool:
        if a1.type() == QEvent.Type.Show:
            Kernel.tasks.add(a0)
        elif a1.type() in (QEvent.Type.Close, QEvent.Type.DeferredDelete):
            if a0 in Kernel.tasks:
                Kernel.tasks.remove(a0)
        if a1.type() == SeparateWidgetEvent.EventType:
            a1.widget.resize(a1.size)
            self.separateWidget(a1.widget)
        elif (isinstance(a0, QWidget)
                and not isinstance(a0, Window)
                and not isinstance(a0, QDialog)
                and not isinstance(a0, RoundMenu)
                and a0.windowType() != Qt.WindowType.ToolTip):
            if a1.type() == QEvent.Type.Show:
                if a0.parent() == None:
                    self.sendEvent(self, WidgetCaughtEvent(a0))
                    if a0.parent() == None:  # 使用默认方法
                        self.showWidget(a0)
        if a1.type() == QEvent.Type.WindowTitleChange:
            oldtitle = a0.windowTitle()
            newtitle = Kernel.translate(oldtitle)
            if newtitle != oldtitle:
                a0.setWindowTitle(newtitle)
        return super().notify(a0, a1)

    def separateWidget(self, widget: QWidget):
        """分离控件"""
        self.showWidget(widget)

    @staticmethod
    def loadTranslation():
        """加载翻译"""
        logging.debug("加载翻译...")
        lang_type = Setting()["language.type"]
        functions_path = "FMCL/Functions"
        paths = ["FMCL/Translations"]
        paths.extend([os.path.join(functions_path, i, "Translations")
                      for i in os.listdir(functions_path)])
        for path in paths:
            if not os.path.exists(f"{path}/{lang_type}.json"):
                continue
            Kernel.translation |= json.load(
                open(f"{path}/{lang_type}.json", encoding="utf-8"))
        logging.debug(Kernel.translation)

    @staticmethod
    def translate(text: str) -> str:
        """翻译"""
        if text in Kernel.translation:
            return Kernel.translation[text]
        lang_type = Setting()["language.type"]
        logging.warning(f"未翻译的文本({lang_type}):{text}")
        Kernel.translation[text] = text
        return text

    @staticmethod
    def unpack():
        # 由Scripts/Pack.py生成打包文件
        logging.debug("解压功能...")
        try:
            from Pack.Functions import zipfile_bytes
        except ImportError:
            pass
        else:
            zip = ZipFile(zipfile_bytes)
            for path in zip.namelist():
                if "__pycache__" in path:
                    continue
                functions_path = "FMCL/Functions"
                logging.debug(f"解压:{path}")
                zip.extract(path, functions_path)
            zip.close()

        logging.debug("解压翻译...")
        try:
            from Pack.Translations import zipfile_bytes
        except ImportError:
            pass
        else:
            zip = ZipFile(zipfile_bytes)
            for path in zip.namelist():
                if "__pycache__" in path:
                    continue
                translation_path = 'FMCL/Translations'
                logging.debug(f"解压:{path}")
                zip.extract(path, translation_path)
            zip.close()

    @staticmethod
    def getFunction(function_name: str):
        """获取功能"""
        if f"FMCL.Functions.{function_name}" in sys.modules:
            return sys.modules[f"FMCL.Functions.{function_name}"]
        try:
            logging.debug(f"获取功能:{function_name}...")
            function = import_module(f"FMCL.Functions.{function_name}")
            logging.debug(function)
            return function
        except:
            logging.error(f"无法获取功能:{function_name}:\n{traceback.format_exc()}")
            raise GetFunctionFailException(function_name)

    @staticmethod
    def execFunction(function_name: str, *args, **kwargs):
        """运行功能"""
        function = Kernel.getFunction(function_name)
        if not hasattr(function, "main"):
            raise NoEntryException(function_name)
        logging.debug(f"运行:{function_name}")
        return getattr(function, "main")(*args, **kwargs)

    def execStartupFunctions(self):
        """运行启动项"""
        startup_functions = Setting()["system.startup_functions"]
        for function_name in startup_functions:
            try:
                self.execFunction(function_name)
            except Exception as e:
                QMessageBox.critical(None,
                                     Kernel.translate("无法运行")+function_name,
                                     str(e))

    @staticmethod
    def getAllFunctions():
        """获取所有功能"""
        functions_path = "FMCL/Functions"
        functions = []
        for function_name in os.listdir(functions_path):
            try:
                functions.append(Kernel.getFunction(function_name))
            except:
                logging.error(traceback.format_exc())
        return functions

    @staticmethod
    def defaultFunctionInfo(function):
        """默认功能信息"""
        name = function.__name__.split(".")[-1]
        return {
            "name": name,
            "id": name,
            "icon": qta.icon("mdi6.application-outline")
        }

    @staticmethod
    def getFunctionInfo(function):
        """获取功能信息"""
        info = Kernel.defaultFunctionInfo(function) | getattr(
            function, "functionInfo", lambda: {})()
        info["name"] = Kernel.translate(info["name"])
        return info

    @staticmethod
    def getAllFunctionInfo():
        """获取全部功能信息"""
        function_info = []
        for function in Kernel.getAllFunctions():
            function_info.append(Kernel.getFunctionInfo(function))
        return function_info

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
