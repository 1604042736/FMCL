import os
import json
from Core.Game import Game
from Core.Mod import Mod
from QtFBN.QFBNWidget import QFBNWidget
from Translate import tr
from ..Setting.BoolSetting import BoolSetting
from ..Setting.IntSetting import IntSetting
from Ui.VersionManager.IconSelector import IconSelector
from Ui.VersionManager.ModItem import ModItem
from Ui.VersionManager.ui_VersionManager import Ui_VersionManager
import Globals as g
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QSize
from Core.Game import Game
from QtFBN.QFBNMessageBox import QFBNMessageBox
from PyQt5.QtGui import QPixmap
import qtawesome as qta


class VersionManager(QFBNWidget, Ui_VersionManager):
    GameDeleted = pyqtSignal()
    IconChanged = pyqtSignal()

    def __init__(self, name, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(qta.icon("msc.versions"))
        self.setWindowTitle(tr("版本管理")+f':{name}')
        self.groupBox.setTitle(tr("基础"))
        self.label_4.setText(tr("Fabric版本"))
        self.label_5.setText(tr("Optifine版本"))
        self.pb_openfoder.setText(tr("打开版本文件夹"))
        self.label_2.setText(tr("版本"))
        self.pb_del.setText(tr("删除"))
        self.pb_reinstall.setText(tr("重新安装"))
        self.label.setText(tr("名称"))
        self.label_3.setText(tr("Forge版本"))
        self.pb_changeicon.setText(tr("更改图标"))
        self.gb_modmanage.setTitle(tr("Mod管理"))
        self.pb_openmodfoder.setText(tr("打开mod文件夹"))
        self.groupBox_3.setTitle(tr("设置"))

        self.version_path = os.path.join(g.cur_gamepath, "versions")
        self.game_path = os.path.join(self.version_path, name)

        self.config = Game(name).get_info()

        if self.config["isolate"]:
            self.mods_path = g.cur_gamepath+"\\mods"
        else:
            pass

        self.name = self.config["name"]
        self.version = self.config["version"]
        self.forge_version = self.config["forge_version"]
        self.fabric_version = self.config["fabric_version"]
        self.optifine_version = self.config["optifine_version"]
        self.icon = self.config["icon"]
        self.isolate = self.config["isolate"]
        self.specific_setting = self.config["specific_setting"]

        if self.specific_setting:
            self.set_specific_setting()

        if self.isolate:
            self.mods_path = self.game_path+"\\mods"
        else:
            self.mods_path = g.cur_gamepath+"\\mods"

        self.isolate_setting = BoolSetting(
            "isolate", tr("版本隔离"), self.isolate, self.save, self)
        self.gridLayout_5.addWidget(self.isolate_setting, 0, 0, 1, 1)

        self.specific_setting_setting = BoolSetting(
            "specific_setting", tr("特定设置"), self.specific_setting, self.save, self)
        self.gridLayout_5.addWidget(self.specific_setting_setting, 0, 1, 1, 1)

        self.le_name.setText(self.name)
        self.l_version.setText(self.version)
        self.l_forgeversion.setText(self.forge_version)
        self.l_fabricversion.setText(self.fabric_version)
        self.l_optifineversion.setText(self.optifine_version)
        self.l_icon.setPixmap(QPixmap(self.icon))

        self.pb_del.clicked.connect(self.del_game)
        self.pb_reinstall.clicked.connect(self.reinstall_game)
        self.pb_openfoder.clicked.connect(lambda: os.startfile(self.game_path))
        self.le_name.textEdited.connect(self.rename_game)
        self.pb_openmodfoder.clicked.connect(
            lambda: os.startfile(self.mods_path))
        self.pb_changeicon.clicked.connect(self.change_icon)

        self.set_mods()

    def set_specific_setting(self):
        self.gamewidth = self.config.get("width", g.width)
        self.gamewidth_setting = IntSetting("width", tr(
            "游戏窗口宽度"), self.gamewidth, self.save, self)
        self.gridLayout_5.addWidget(self.gamewidth_setting, 1, 0, 1, 1)

        self.gameheight = self.config.get("height", g.height)
        self.gameheight_setting = IntSetting("height", tr(
            "游戏窗口高度"), self.gameheight, self.save, self)
        self.gridLayout_5.addWidget(self.gameheight_setting, 1, 1, 1, 1)

        self.maxmem = self.config.get("maxmem", g.maxmem)
        self.maxmem_setting = IntSetting("maxmem", tr(
            "最大内存"), self.maxmem, self.save, self)
        self.gridLayout_5.addWidget(self.maxmem_setting, 2, 0, 1, 1)

        self.minmem = self.config.get("minmem", g.minmem)
        self.minmem_setting = IntSetting("minmem", tr(
            "最小内存"), self.minmem, self.save, self)
        self.gridLayout_5.addWidget(self.minmem_setting, 2, 1, 1, 1)

    def unset_specific_setting(self):
        try:
            self.gridLayout_5.removeWidget(self.gamewidth_setting)
            self.gridLayout_5.removeWidget(self.gameheight_setting)
            self.gridLayout_5.removeWidget(self.maxmem_setting)
            self.gridLayout_5.removeWidget(self.minmem_setting)
            self.gamewidth_setting.hide()
            self.gameheight_setting.hide()
            self.maxmem_setting.hide()
            self.minmem_setting.hide()
        except:
            pass

    def save(self):
        for key in self.config:
            if key in self.__dict__:
                self.config[key] = getattr(self, key)
        if self.specific_setting:
            self.set_specific_setting()
            for key in ("gamewidth", "gameheight", "maxmem", "minmem"):
                if key in self.__dict__:
                    self.config[key] = getattr(self, key)
        else:
            self.unset_specific_setting()

        if self.isolate:
            self.mods_path = self.game_path+"\\mods"
        else:
            self.mods_path = g.cur_gamepath+"\\mods"
        self.set_mods()

        json.dump(self.config, open(
            self.game_path+"/FMCL/config.json", "w"))

    def close(self, called_del=False) -> bool:
        if not called_del:
            self.save()
        return super().close()

    def del_game(self):
        def ok():
            Game(self.name).del_game()
            self.GameDeleted.emit()
            self.close(True)
        msgbox = QFBNMessageBox.info(self, tr("删除"), tr("确定删除")+"?", ok)
        msgbox.show("original")

    def reinstall_game(self):
        g.dmgr.add_task(f"{tr('下载')} {self.name}", Game(
            self.name, self.version, self.forge_version, self.fabric_version, self.optifine_version), "download_version", tuple())

    def rename_game(self):
        new_name = self.le_name.text()
        Game(self.name).rename(new_name)
        self.name = new_name
        self.game_path = os.path.join(self.version_path, self.name)

    def set_mods(self):
        if not (self.forge_version or self.fabric_version):
            self.gb_modmanage.hide()
            return
        while self.gl_modlist.count():
            item = self.gl_modlist.itemAt(0)
            self.gl_modlist.removeItem(item)
            item.widget().deleteLater()
        modlist,enablemod,allmod=Mod(path=self.mods_path).get_mods()
        self.gb_modmanage.setText(f'{tr("Mod管理")}({enablemod}/{allmod})')
        for i, val in enumerate(modlist):
            widget = ModItem(val, self.mods_path)
            widget.ModEnDisAble.connect(self.set_mods)
            widget.ModDeleted.connect(self.set_mods)
            self.gl_modlist.addWidget(widget, i, 0, 1, 1)

    def change_icon(self):
        def ok(icon):
            self.icon = icon
            self.l_icon.setPixmap(QPixmap(self.icon))
            self.save()
            self.IconChanged.emit()

        iconselector = IconSelector(self)
        iconselector.Selected.connect(ok)
        iconselector.show("original")
