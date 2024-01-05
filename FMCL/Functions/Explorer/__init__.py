from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QFileDialog
from qfluentwidgets import PrimaryPushButton
from Setting import Setting
from Kernel import Kernel

from .Explorer import Explorer
from .Help.ui_Launcher import Ui_Launcher
from .Help.ui_Desktop import Ui_Desktop
from .Help.ui_Start import Ui_Start

_translate = QCoreApplication.translate


def helpIndex():
    return {
        "launcher": {
            "name": _translate("ExplorerHelp", "启动器"),
            "page": lambda: Kernel.getWidgetFromUi(Ui_Launcher),
            "desktop": {
                "name": _translate("ExplorerHelp", "桌面"),
                "page": lambda: Kernel.getWidgetFromUi(Ui_Desktop),
            },
            "start": {
                "name": _translate("ExplorerHelp", "开始"),
                "page": lambda: Kernel.getWidgetFromUi(Ui_Start),
            },
        }
    }


def defaultSetting() -> dict:
    setting = Setting()
    if "system.startup_functions" in setting.defaultsetting:
        a = setting.defaultsetting.get("system.startup_functions")
        if "Explorer" not in a:
            a.insert(0, "Explorer")
    return {
        "explorer.desktop.background_image": "",
        "explorer.desktop.item_rightclicked_actions": [],
        "explorer.desktop.rightclicked_actions": [],
        "explorer.desktop.quick_switch_gamedir": True,
        "explorer.title_rightclicked_actions": [],
        "explorer.width": 1000,
        "explorer.height": 618,
        "explorer.auto_sync_size": True,
    }


def defaultSettingAttr() -> dict:
    def chooseimage():
        file, _ = QFileDialog.getOpenFileName(
            None, _translate("Explorer", "选择图片"), filter="Image File (*.png;*.jpg)"
        )
        if file:
            Setting().set("explorer.desktop.background_image", file)

    def chooseimagebutton():
        pb_chooseimage = PrimaryPushButton()
        pb_chooseimage.setText(_translate("Explorer", "选择图片"))
        pb_chooseimage.clicked.connect(chooseimage)
        return pb_chooseimage

    return {
        "explorer": {"name": "Explorer"},
        "explorer.desktop": {"name": _translate("Explorer", "桌面")},
        "explorer.desktop.background_image": {
            "name": _translate("Explorer", "背景图片"),
            "side_widgets": [chooseimagebutton],
        },
        "explorer.desktop.item_rightclicked_actions": {
            "name": _translate("Explorer", "游戏右键操作")
        },
        "explorer.desktop.rightclicked_actions": {
            "name": _translate("Explorer", "右键(空白处)操作")
        },
        "explorer.desktop.quick_switch_gamedir": {
            "name": _translate("Explorer", "快捷更改游戏目录")
        },
        "explorer.title_rightclicked_actions": {
            "name": _translate("Explorer", "标题栏右键操作")
        },
        "explorer.width": {"name": _translate("Explorer", "启动器高度")},
        "explorer.height": {"name": _translate("Explorer", "启动器宽度")},
        "explorer.auto_sync_size": {"name": _translate("Explorer", "自动同步启动器大小")},
    }


def main():
    explorer = Explorer()
    explorer.show()
