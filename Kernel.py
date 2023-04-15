import logging
import os
import sys
import traceback
from importlib import import_module
from zipfile import *

import qtawesome as qta
from PyQt5.QtCore import QEvent, QObject, Qt, QTranslator
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QWidget

from Events import *
from Exceptions import *
from Setting import Setting
from Window import Window


class Kernel(QApplication):
    tasks = set()

    def __init__(self, argv: list[str] = sys.argv) -> None:
        super().__init__(argv)
        self.setWindowIcon(QIcon(":/Icon/FMCL.ico"))
        self.setApplicationName("FMCL")
        self.setApplicationVersion("3.0")

        cur_path = os.path.abspath(".")
        if cur_path not in sys.path:
            sys.path.insert(0, os.path.abspath("."))

        translator = QTranslator()
        translator.load(Setting()["launcher.language"])
        self.installTranslator(translator)

        logging.debug("解压默认功能...")
        self.unpackFunction()
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
                and a0.windowType() != Qt.WindowType.ToolTip):
            if a1.type() == QEvent.Type.Show:
                if a0.parent() == None:
                    self.sendEvent(self, WidgetCaughtEvent(a0))
                    if a0.parent() == None:  # 使用默认方法
                        self.showWidget(a0)
        return super().notify(a0, a1)

    def separateWidget(self, widget: QWidget):
        """分离控件"""
        self.showWidget(widget)

    @staticmethod
    def unpackFunction():
        try:
            # FunctionPack.py由Scripts/ReleaseBuilder.py生成
            from FunctionPack import zipfile_bytes
        except ImportError:
            return
        zip = ZipFile(zipfile_bytes)
        for path in zip.namelist():
            if "__pycache__" in path:
                continue
            functions_path = Setting()["system.functions_path"]
            target_path = os.path.join(functions_path, path)
            if not os.path.exists(target_path):
                logging.debug(f"解压:{path}")
                zip.extract(path, functions_path)
        zip.close()

    @staticmethod
    def getFunction(function_name: str):
        """获取功能"""
        functions_path = Setting()["system.functions_path"]
        try:
            logging.debug(f"获取功能:{function_name}...")
            function = import_module(
                f"{'.'.join(functions_path.split(os.sep))}.{function_name}")
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
            self.execFunction(function_name)

    @staticmethod
    def getAllFunctions():
        """获取所有功能"""
        functions_path = Setting()["system.functions_path"]
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
        return Kernel.defaultFunctionInfo(function) | getattr(function, "functionInfo", lambda: {})()

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
