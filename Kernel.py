import logging
import os
import sys
import traceback
from importlib import import_module
from zipfile import *

import qtawesome as qta
from PyQt5.QtCore import QCoreApplication, QEvent, QObject, Qt, QTranslator
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QWidget
from qfluentwidgets import RoundMenu, setThemeColor

from Events import *
from Setting import Setting, defaultSettingAttr, setThemeFromStr
from Window import Window

_translate = QCoreApplication.translate


class Kernel(QApplication):
    widgets = set()

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

        logging.info("初始化功能...")
        self.getAllFunctions()
        self.loadTranslation()

        setThemeColor(Setting().get("system.theme_color"))
        setThemeFromStr(Setting().get("system.theme")[0])

        logging.info("运行启动项...")
        self.execStartupFunctions()

    def notify(self, a0: QObject, a1: QEvent) -> bool:
        if a1.type() == QEvent.Type.Show:
            Kernel.widgets.add(a0)
        elif a1.type() in (QEvent.Type.Close, QEvent.Type.DeferredDelete):
            if a0 in Kernel.widgets:
                Kernel.widgets.remove(a0)
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
        return super().notify(a0, a1)

    def separateWidget(self, widget: QWidget):
        """分离控件"""
        self.showWidget(widget)

    def loadTranslation(self):
        """加载翻译"""
        logging.info("加载翻译...")
        lang = Setting().get("language.type")+".qm"
        self.__translators = []  # 防止Translator被销毁
        for i in ["FMCL/Translations"]+[f"FMCL/Functions/{i}/Translations"for i in os.listdir("FMCL/Functions")]:
            file = f"{i}/{lang}"
            if not os.path.exists(file):
                continue
            translator = QTranslator()
            if translator.load(file):
                if self.installTranslator(translator):
                    logging.info(f"已加载{file}")
                    self.__translators.append(translator)
        # 加载翻译后更新attr的值，因为之前加进去的attr没有翻译过
        Setting().addAttr(defaultSettingAttr())
        Setting().loadFunctionSettingAttr()

    @staticmethod
    def unpack():
        # 由Scripts/Pack.py生成打包文件
        logging.info("解压功能...")
        try:
            from Pack.Functions import zipfile_bytes
        except ImportError:
            pass
        else:
            zip = ZipFile(zipfile_bytes)
            for path in zip.namelist():
                functions_path = "FMCL/Functions"
                logging.info(f"解压:{path}")
                zip.extract(path, functions_path)
            zip.close()

        logging.info("解压翻译...")
        try:
            from Pack.Translations import zipfile_bytes
        except ImportError:
            pass
        else:
            zip = ZipFile(zipfile_bytes)
            for path in zip.namelist():
                translation_path = 'FMCL/Translations'
                logging.info(f"解压:{path}")
                zip.extract(path, translation_path)
            zip.close()

    @staticmethod
    def getFunction(function_name: str):
        """获取功能"""
        # 并不捕获异常而是留给调用者捕获
        if f"FMCL.Functions.{function_name}" in sys.modules:
            return sys.modules[f"FMCL.Functions.{function_name}"]
        function = import_module(f"FMCL.Functions.{function_name}")
        logging.info(f"已获取功能: {function_name}")
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
        startup_functions = Setting()["system.startup_functions"]
        for function_name in startup_functions:
            try:
                self.execFunction(function_name)
            except:
                QMessageBox.critical(None,
                                     _translate("Kernel", "无法运行") +
                                     function_name,
                                     traceback.format_exc())

    @staticmethod
    def getAllFunctions():
        """获取所有功能"""
        functions_path = "FMCL/Functions"
        functions = []
        for function_name in os.listdir(functions_path):
            functions.append(Kernel.getFunction(function_name))
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
