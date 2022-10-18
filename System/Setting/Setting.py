import json
import os

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import qApp
from System.Setting.SettingItems.SettingItem import SettingItem

from .SettingWidget import SettingWidget


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

    def __init__(self, setting_path: str = None) -> None:
        if setting_path == None:
            setting_path = f"{qApp.applicationName()}/setting.json"
        if self.__new_count[setting_path] > 1:
            return
        super().__init__()
        self.setting_path = setting_path
        self.setting = {}
        self.setting_attr = {}
        if os.path.exists(self.setting_path):
            self.setting = json.load(open(self.setting_path, encoding="utf-8"))

        self.setting_widget = None

    def addSetting(self, default_setting: dict):
        """添加默认设置"""
        # 注意合并顺序，防止覆盖已有设置
        self.setting = default_setting | self.setting

        # 设置默认属性
        for id in default_setting:
            self.setting_attr[id] = {
                "name": id,
                "description": "",
                "setting_item": lambda id=id: SettingItem(id, self)
            }

    def addSettingAttr(self, attr: dict):
        """添加设置属性"""
        self.merge(self.setting_attr, attr)

    def merge(self, a: dict, b: dict):
        """合并a和b"""
        for key, val in b.items():
            if key not in a:
                a[key] = val
            elif isinstance(val, dict):
                self.merge(a[key], val)
            else:
                a[key] = val

    def get(self, id: str, default=None):
        """获取设置项"""
        return self.setting.get(id, default)

    def getAttr(self, id: str, attr: str, default=None):
        """获取设置项的属性"""
        return self.setting_attr[id].get(attr, default)

    def set(self, id: str, val):
        self.setting[id] = val

    def show(self, id: str = ""):
        self.getWidget().show(id)

    def getWidget(self):
        if self.setting_widget == None:
            self.setting_widget = SettingWidget(self)
        return self.setting_widget

    def sync(self):
        if not os.path.exists(os.path.dirname(self.setting_path)):
            os.makedirs(os.path.dirname(self.setting_path))
        json.dump(self.setting, open(
            self.setting_path, mode="w", encoding="utf-8"))

    def refresh(self):
        if self.setting_widget != None:
            self.setting_widget.refresh()
