from importlib import import_module
import sys
import qtawesome as qta
import os
import logging
import traceback


class Function:
    """功能"""

    PATH = ["FMCL/Functions", "FMCL/Default/FMCL/Functions"]

    @staticmethod
    def get_all() -> list["Function"]:
        """获取所有功能"""
        functions = {}
        for functions_path in Function.PATH:
            if not os.path.exists(functions_path):
                continue
            for function_name in os.listdir(functions_path):
                try:
                    functions[function_name] = Function(function_name)
                except:
                    logging.warning(
                        f"功能{function_name}将被忽略:\n{traceback.format_exc()}"
                    )
        return functions.values()

    @staticmethod
    def get_all_info():
        """获取全部功能信息"""
        function_info = []
        for function in Function.get_all():
            function_info.append(function.get_info())
        return function_info

    @staticmethod
    def get_all_help_index() -> list:
        """获取全部功能的帮助索引"""
        function_helpindex = []
        for function in Function.get_all():
            function_helpindex.append(function.get_help_index())
        return function_helpindex

    def __init__(self, name) -> None:
        self.name = name
        if f"FMCL.Functions.{name}" not in sys.modules:
            self.module = import_module(f"FMCL.Functions.{name}")
            logging.info(f"加载功能: {name} ({self.module})")
        else:
            self.module = import_module(f"FMCL.Functions.{name}")

    def exec(self, *args, **kwargs):
        """运行功能"""
        return getattr(self.module, "main")(*args, **kwargs)

    def default_info(self):
        return {
            "name": self.name,
            "id": self.name,
            "icon": qta.icon("mdi6.application-outline"),
        }

    def get_info(self):
        return self.default_info() | getattr(self.module, "functionInfo", lambda: {})()

    def get_default_setting(self):
        """获取默认设置"""
        return getattr(self.module, "defaultSetting", lambda: {})()

    def get_default_settingattr(self):
        """获取默认设置属性"""
        return getattr(self.module, "defaultSettingAttr", lambda: {})()

    def get_help_index(self):
        return getattr(self.module, "helpIndex", lambda: {})()
