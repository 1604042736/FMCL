from QtFBN.QFBNWidget import QFBNWidget
from Translate import tr, all_languages
from Ui.Setting.ColorSetting import ColorSetting
from Ui.Setting.IntSetting import IntSetting
from Ui.Setting.ListSetting import ListSetting
from Ui.Setting.SelectSetting import SelectSetting
from Ui.Setting.StrSetting import StrSetting
from Ui.Setting.ui_Setting import Ui_Setting
import Globals as g
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import QSize
import qtawesome as qta


class Setting(QFBNWidget, Ui_Setting):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(tr("设置"))
        self.setWindowIcon(qta.icon("ri.settings-5-line"))
        self.load_settings()

    def load_settings(self):
        self.lw_settings.clear()
        config = {
            tr("游戏路径"): [g.all_gamepath, "all_gamepath"],
            tr("游戏窗口宽度"): [g.gamewidth, "gamewidth"],
            tr("游戏窗口高度"): [g.gameheight, "gameheight"],
            tr("最大内存"): [g.maxmem, "maxmem"],
            tr("最小内存"): [g.minmem, "minmem"],
            tr("Java路径"): [g.java_path, "java_path"],
            tr("背景图片"): [g.background_image, "background_image"],
            tr("主题"): [g.theme, "theme"],
            tr("语言"): [all_languages, "language"],
            tr("下载的最大线程数"): [g.max_thread_count, "max_thread_count"]
        }
        for key, val in config.items():
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 64))
            if isinstance(val[0], str) and "rgb" in val[0]:
                widget = ColorSetting(
                    val[1], key, val[0], do_after_save=lambda: g.set_theme() or g.save())
            elif isinstance(val[0], str):
                widget = StrSetting(val[1], key, val[0], do_after_save=g.save)
            elif isinstance(val[0], list):
                widget = ListSetting(
                    val[1], key, val[0], "cur_gamepath", "file", do_after_save=g.save)
            elif isinstance(val[0], int):
                widget = IntSetting(val[1], key, val[0], do_after_save=g.save)
            elif isinstance(val[0], tuple):
                widget = SelectSetting(
                    val[1], key, val[0], do_after_save=g.save)
            else:
                continue

            self.lw_settings.addItem(item)
            self.lw_settings.setItemWidget(item, widget)
