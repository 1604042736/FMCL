from QtFBN.QFBNWidget import QFBNWidget
from Ui.Setting.ColorSetting import ColorSetting
from Ui.Setting.IntSetting import IntSetting
from Ui.Setting.ListSetting import ListSetting
from Ui.Setting.StrSetting import StrSetting
from Ui.Setting.ui_Setting import Ui_Setting
import Globals as g
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import QSize


class Setting(QFBNWidget, Ui_Setting):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.load_settings()

    def load_settings(self):
        self.lw_settings.clear()
        config = {
            "游戏路径": [g.all_gamepath, "all_gamepath"],
            "游戏窗口宽度": [g.width, "width"],
            "游戏窗口高度": [g.height, "height"],
            "最大内存": [g.maxmem, "maxmem"],
            "最小内存": [g.minmem, "minmem"],
            "Java路径": [g.java_path, "java_path"],
            "QML文件路径": [g.homepage_qml, "homepage_qml"],
            "主题": [g.theme, "theme"]
        }
        for key, val in config.items():
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 64))
            if isinstance(val[0], str) and "rgb" in val[0]:
                widget = ColorSetting(val[1], key, val[0])
            elif isinstance(val[0], str):
                widget = StrSetting(val[1], key, val[0])
            elif isinstance(val[0], list):
                widget = ListSetting(
                    val[1], key, val[0], "cur_gamepath", "file")
            elif isinstance(val[0], int):
                widget = IntSetting(val[1], key, val[0])
            else:
                continue

            self.lw_settings.addItem(item)
            self.lw_settings.setItemWidget(item, widget)
