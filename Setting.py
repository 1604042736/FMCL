import json
import os
from typing import Any, Literal, TypedDict, Callable
from PyQt5.QtCore import QCoreApplication
from qfluentwidgets import Theme, setTheme, setThemeColor

_translate = QCoreApplication.translate


# 默认设置路径
DEFAULT_SETTING_PATH = os.path.join("FMCL", "settings.json")
# 默认设置
DEFAULT_SETTING = {
    "system.startup_functions": [],
    "system.theme_color": "#00ff00",
    "game.directories": [".minecraft"],
    "game.java_path": "java",
    "game.width": 1000,
    "game.height": 618,
    "game.maxmem": 2048,
    "users": [],
    "users.selectindex": 0,
    "language.type": "简体中文",
}


class Link(TypedDict):
    name: str  # 链接名称
    action: Callable  # 链接操作


class SettingAttr(TypedDict):
    """设置属性类型"""

    name: str  # 名称
    callback: list[Callable[[Any], None]]  # 回调函数, 在对应设置项被修改后调用
    enable_condition: Callable[["Setting"], bool]  # 启用条件, 禁用后, 它的子设置也会被禁用
    link: Link  # 链接
    # 一下类型将用于List设置项
    static: bool  # 是否为静态(不可更改, 当成tuple)
    type: Literal["directory", "file", "input"]  # 列表中每项的类型
    atleast: int  # 至少要有几项


def defaultSettingAttr() -> SettingAttr:
    return {
        "system": {"name": _translate("Setting", "系统")},
        "system.startup_functions": {"name": _translate("Setting", "启动项")},
        "system.theme_color": {
            "name": _translate("Setting", "主题颜色"),
            "callback": [lambda a: setThemeColor(a)],
        },
        "game": {"name": _translate("Setting", "游戏")},
        "game.directories": {
            "name": _translate("Setting", "游戏目录"),
            "type": "directory",
            "atleast": 1,
        },
        "game.java_path": {"name": _translate("Setting", "Java路径")},
        "game.width": {"name": _translate("Setting", "游戏窗口宽度")},
        "game.height": {"name": _translate("Setting", "游戏窗口高度")},
        "game.maxmem": {"name": _translate("Setting", "最大内存")},
        "users": {"name": _translate("Setting", "用户")},
        "users.selectindex": {"name": _translate("Setting", "选择用户索引")},
        "language": {
            "name": _translate("Setting", "语言"),
        },
        "language.type": {"name": _translate("Setting", "语言类型")},
    }


class ListSettingTrace(list):
    """跟踪设置中的列表项, 在该列表被修改时同时更改设置"""

    def __init__(self, l, id: str, setting: "Setting"):
        super().__init__(l)
        self.id = id
        self.setting = setting

    def __setitem__(self, key, val):
        super().__setitem__(key, val)
        self.setting.set(self.id, self)

    def append(self, __object) -> None:
        super().append(__object)
        self.setting.set(self.id, self)

    def pop(self, __index=-1):
        ret = super().pop(__index)
        self.setting.set(self.id, self)
        return ret

    def insert(self, __index, __object):
        super().insert(__index, __object)
        self.setting.set(self.id, self)

    def extend(self, __iterable):
        super().extend(__iterable)
        self.setting.set(self.id, self)

    def remove(self, __value):
        super().remove(__value)
        self.setting.set(self.id, self)

    def sort(self, *args):
        super().sort(*args)
        self.setting.set(self.id, self)


class Setting:
    """管理设置文件"""

    instances = {}
    new_count = {}

    def __new__(cls, setting_path: str = DEFAULT_SETTING_PATH):
        if setting_path not in Setting.instances:
            Setting.instances[setting_path] = super().__new__(cls)
            Setting.new_count[setting_path] = 0
        Setting.new_count[setting_path] += 1
        return Setting.instances[setting_path]

    def __init__(self, setting_path: str = DEFAULT_SETTING_PATH):
        if Setting.new_count[setting_path] > 1:  # 防止重复初始化
            return
        self.attrs: SettingAttr = {}
        self.setting_path = setting_path
        self.modifiedsetting = {}  # 修改过的设置
        self.defaultsetting = {}  # 默认设置
        if setting_path == DEFAULT_SETTING_PATH:
            self.add(DEFAULT_SETTING)
            self.loadFunctionSetting()
        if os.path.exists(setting_path):
            for key, val in json.load(open(setting_path, encoding="utf-8")).items():
                self.modifiedsetting[key] = val

    def add(self, new_setting: dict):
        """添加新的默认设置"""
        for key, val in new_setting.items():
            if key not in self.defaultsetting:
                self.defaultsetting[key] = val

        for id in new_setting:
            if id not in self.attrs:  # 防止以前加载过[Version可能会频繁执行此操作(调用generate_setting)]
                self.attrs[id] = {"name": id}

    def addAttr(self, attr: SettingAttr):
        """添加设置属性"""
        for key, val in attr.items():
            if key not in self.attrs:
                self.attrs[key] = val
            else:  # 防止之前已经加载过
                self.attrs[key] |= val

    def getAttr(self, id: str, attr: str, default=None):
        """获取设置项的属性"""
        return self.attrs[id].get(attr, default)

    def sync(self):
        if not os.path.exists(os.path.dirname(self.setting_path)):
            os.makedirs(os.path.dirname(self.setting_path))
        json.dump(
            self.modifiedsetting,
            open(self.setting_path, mode="w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4,
        )

    def set(self, id: str, val):
        self[id] = val
        self.sync()
        self.callback(id, val)

    def callback(self, id: str, val=None):
        if val == None:
            val = self.get(id)
        for i in self.getAttr(id, "callback", tuple()):
            i(val)

    def loadFunctionSetting(self):
        """加载功能的设置"""
        from Kernel import Kernel

        for function in Kernel.getAllFunctions():
            self.add(getattr(function, "defaultSetting", lambda: {})())

    def loadFunctionSettingAttr(self):
        """加载功能的设置属性"""
        from Kernel import Kernel

        for function in Kernel.getAllFunctions():
            self.addAttr(getattr(function, "defaultSettingAttr", lambda: {})())

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        if key in self.modifiedsetting:
            val = self.modifiedsetting[key]
            if isinstance(val, list):  # 对list设置项的操作将会被捕捉
                return ListSettingTrace(val, key, self)
            return val
        elif key in self.defaultsetting:
            val = self.defaultsetting[key]
            if isinstance(val, list):  # 对list设置项的操作将会被捕捉
                return ListSettingTrace(val, key, self)
            return val
        raise KeyError(key)

    def items(self):
        return (self.defaultsetting | self.modifiedsetting).items()

    def __setitem__(self, key, value):
        self.modifiedsetting[key] = value
        if key in self.defaultsetting and self.defaultsetting[key] == value:
            self.modifiedsetting.pop(key)

    def restore(self, id):
        """恢复默认设置"""
        self.set(id, self.defaultsetting[id])
