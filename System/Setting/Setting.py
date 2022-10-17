import json
import os

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import qApp

from .SettingWidgets import DictSettingWidget, SettingWidget


class Setting(QObject):
    __instances = {}
    __new_count = {}

    def __new__(cls, setting_path: str = None):
        if setting_path == None:
            setting_path = f"{qApp.applicationName()}/setting.json"
        if setting_path not in cls.__instances:
            cls.__instances[setting_path] = super().__new__(cls)
            cls.__new_count[setting_path] = 0
        cls.__new_count[setting_path] += 1
        return cls.__instances[setting_path]

    def __init__(self, setting_path: str = None):
        if setting_path == None:
            setting_path = f"{qApp.applicationName()}/setting.json"
        if self.__new_count[setting_path] > 1:
            return
        super().__init__()
        self.SETTING_PATH = setting_path
        self.id_prefix = self.SETTING_PATH+"#"

        self.setting = {}
        if os.path.exists(self.SETTING_PATH):
            self.setting = json.load(open(self.SETTING_PATH, encoding="utf-8"))

    def addSetting(self, setting: dict):
        """
        添加新的设置(默认)
        我们会将它与原有设置合并以保证结构相同
        """
        self.merge(self.setting, setting)

    def merge(self, a: dict, b: dict):
        """合并a和b"""
        for key, val in b.items():
            if key not in a:
                a[key] = val
            elif isinstance(val, dict):
                self.merge(a[key], val)
            elif key == "name" or key == "description":  # 确保翻译
                a[key] = val

    def get(self, id: str):
        """获得一个设置项的值"""
        id = id.replace(self.id_prefix, "")
        a = self.setting
        for i in id.split("."):
            if i:
                a = a[i]["value"]
        return a

    def get_setting(self, id: str):
        """获得一个设置项"""
        id = id.replace(self.id_prefix, "")
        a = self.setting
        keys = id.split(".")
        for i, val in enumerate(keys):
            if val:
                if i == len(keys)-1:
                    a = a[val]
                else:
                    a = a[val]["value"]
        return a

    def set_value(self, id: str, value):
        id = id.replace(self.id_prefix, "")
        a = self.setting
        keys = id.split(".")
        for i, val in enumerate(keys):
            if val:
                if i == len(keys)-1:
                    a = a[val]
                else:
                    a = a[val]["value"]
        a["value"] = value
        self.sync()
        if "callback" in a:
            a["callback"]()

    def show(self, id: str = ""):
        self.get_widget(id).show()

    def get_widget(self, id: str = ""):
        if id:
            return SettingWidget(self.id_prefix+id, self.get(id))
        else:
            return DictSettingWidget(self.id_prefix+id, self.setting)

    def filter(self, a: dict) -> dict:
        """过滤字典中没必要的值"""
        result = {}
        for key, val in a.items():
            if isinstance(val, dict):
                result[key] = self.filter(val)
            elif (isinstance(val, int)
                  or isinstance(val, str)
                  or isinstance(val, bool)
                  or isinstance(val, list)):
                result[key] = val
        return result

    def sync(self):
        new_setting = self.filter(self.setting)
        if not os.path.exists(os.path.dirname(self.SETTING_PATH)):
            os.makedirs(os.path.dirname(self.SETTING_PATH))
        json.dump(new_setting,
                  open(self.SETTING_PATH, mode="w", encoding="utf-8"))
