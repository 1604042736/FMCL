from PyQt5.QtCore import QCoreApplication
from Setting import Setting

from .Explorer import Explorer

_translate = QCoreApplication.translate


def defaultSetting() -> dict:
    setting = Setting()
    a = setting.get("system.startup_functions", tuple())
    if "Explorer" not in a:
        a.insert(0, "Explorer")
    return {
        "explorer.desktop.background_image": "",
        "explorer.desktop.item_rightclicked_actions": [],
        "explorer.title_rightclicked_actions": []
    }


def defaultSettingAttr() -> dict:
    return {
        "explorer": {
            "name": "Explorer"
        },
        "explorer.desktop": {
            "name": _translate("Explorer", "桌面")
        },
        "explorer.desktop.background_image": {
            "name": _translate("Explorer", "背景图片")
        },
        "explorer.desktop.item_rightclicked_actions": {
            "name": _translate("Explorer", "游戏右键操作")
        },
        "explorer.title_rightclicked_actions": {
            "name": _translate("Explorer", "标题栏右键操作")
        }
    }


def main():
    explorer = Explorer()
    explorer.show()
