import json
import logging
import os
import traceback
from importlib import import_module

# 默认设置路径
DEFAULT_SETTING_PATH = os.path.join("FMCL", "settings.json")
# 默认设置
DEFAULT_SETTING = {
    "system.startup_functions": ["Explorer", "Update"],
    "system.theme_color": "#ffffff",
    "launcher.width": 1000,
    "launcher.height": 618,
    "game.directories": [".minecraft"],
    "game.java_path": "javaw",
    "game.width": 1000,
    "game.height": 618,
    "users": [],
    "language.type": "简体中文"
}
# 默认设置属性
DEFAULT_SETTING_ATTR = {
    "system": {
        "name": "系统"
    },
    "system.startup_functions": {
        "name": "启动项"
    },
    "system.theme_color": {
        "name": "主题颜色"
    },
    "launcher": {
        "name": "启动器"
    },
    "launcher.width": {
        "name":  "启动器宽度"
    },
    "launcher.height": {
        "name":  "启动器高度"
    },
    "game": {
        "name":  "游戏"
    },
    "game.directories": {
        "name":  "游戏目录",
        "method": "directory",
        "atleast": 1
    },
    "game.java_path": {
        "name": "Java路径"
    },
    "game.width": {
        "name":  "游戏窗口宽度"
    },
    "game.height": {
        "name": "游戏窗口高度"
    },
    "users": {
        "name":  "用户"
    },
    "language": {
        "name": "语言",
    },
    "language.type": {
        "name": "语言类型"
    }
}


class Setting(dict):
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
        self.attrs = {}
        self.setting_path = setting_path
        if setting_path == DEFAULT_SETTING_PATH:
            from Kernel import Kernel
            DEFAULT_SETTING_ATTR["users"]["method"] = lambda: Kernel.execFunction(
                "CreateUser")
            try:
                from FMCL.Functions.LanguageChooser import LanguageChooser
                DEFAULT_SETTING_ATTR["language.type"]["setting_item"] = LanguageChooser
            except:
                pass
            self.add(DEFAULT_SETTING)
            self.addAttr(DEFAULT_SETTING_ATTR)
            self.loadFunctionSetting()
        if os.path.exists(setting_path):
            for key, val in json.load(open(setting_path, encoding="utf-8")).items():
                self[key] = val

    def add(self, new_setting: dict):
        """添加新的设置"""
        for key, val in new_setting.items():
            if key not in self:
                self[key] = val

        for id in new_setting:
            self.attrs[id] = {
                "name": id
            }

    def addAttr(self, attr: dict):
        """添加设置属性"""
        self.merge(self.attrs, attr)

    def merge(self, a: dict, b: dict):
        """合并a和b"""
        for key, val in b.items():
            if key not in a:
                a[key] = val
            elif isinstance(val, dict):
                self.merge(a[key], val)
            else:
                a[key] = val

    def getAttr(self, id: str, attr: str, default=None):
        """获取设置项的属性"""
        return self.attrs[id].get(attr, default)

    def sync(self):
        if not os.path.exists(os.path.dirname(self.setting_path)):
            os.makedirs(os.path.dirname(self.setting_path))
        json.dump(self,
                  open(self.setting_path, mode="w", encoding="utf-8"),
                  ensure_ascii=False)

    def set(self, id: str, val):
        self[id] = val
        self.sync()

    def loadFunctionSetting(self):
        """加载功能的设置"""
        functions_path = "FMCL/Functions"
        for function_name in os.listdir(functions_path):
            try:
                function = import_module(f"FMCL.Functions.{function_name}")
                self.add(getattr(function, "defaultSetting", lambda: {})())
                self.addAttr(
                    getattr(function, "defaultSettingAttr", lambda: {})())
            except:
                logging.error(traceback.format_exc())
