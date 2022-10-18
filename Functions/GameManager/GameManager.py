import qtawesome as qta
from Core import Game
from PyQt5.QtCore import QCoreApplication, QEvent, Qt, pyqtSlot
from PyQt5.QtWidgets import QCheckBox, QLabel, QMessageBox, QWidget

from ..LogoChooser import LogoChooser
from .ui_GameManager import Ui_GameManager

_translate = QCoreApplication.translate


class GameManager(QWidget, Ui_GameManager):

    __instances = {}
    __new_count = {}

    def __new__(cls, name: str):
        if name not in cls.__instances:
            cls.__instances[name] = super().__new__(cls)
            cls.__new_count[name] = 0
        cls.__new_count[name] += 1
        return cls.__instances[name]

    def __init__(self, name: str):
        if self.__new_count[name] > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi6.minecraft"))
        self. __info_translate = {
            "version": _translate("GameManager", "版本"),
            "forge_version": _translate("GameManager", "Forge版本"),
            "fabric_version": _translate("GameManager", "Fabric版本")
        }

        self.name = name
        self.game = Game(name)
        self.info = self.game.get_info()
        self.__mods: dict[str, tuple(QCheckBox, QLabel)] = {}

        self.pb_opendirectory.clicked.connect(self.game.open_directory)
        self.gl_mods.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.le_name.setText(name)
        for key, val in self.info.items():
            if val:
                label = QLabel()
                label.setText(f"{self.__info_translate[key]}: {val}")
                self.gl_summary.addWidget(label)

        if not (self.info["forge_version"] or self.info["fabric_version"]):
            self.gb_mods.hide()

        self.le_name.textEdited.connect(self.__rename)
        self.refresh()

    def setLogo(self):
        pixmap = self.game.get_pixmap()
        if not pixmap.isNull():
            self.l_logo.setPixmap(pixmap.scaled(64, 64))

    def refresh(self):
        self.game.DEFAULT_SETTING["isolation"]["callback"] = self.setMods
        self.game.DEFAULT_SETTING["logo"]["callback"] = self.setLogo

        self.game.generate_setting()

        setting_widget = self.game.setting.get_widget()
        # setting_widget.refresh()
        # for i in range(setting_widget.lw_value.count()):
        #    item = setting_widget.lw_value.item(i)
        #    widget = setting_widget.lw_value.itemWidget(item)
        self.gl_setting.addWidget(setting_widget)

        self.setLogo()
        self.setMods()

    def setMods(self):
        if not (self.info["forge_version"] or self.info["fabric_version"]):
            return
        mods = self.game.get_mod()

        for _, val in enumerate(mods):
            if val[1] not in self.__mods:
                checkbox = QCheckBox()
                checkbox.setCheckState(val[0])
                checkbox.stateChanged.connect(
                    lambda _, v=val[1], c=checkbox: self.game.setModEnabled(v, c.checkState()))

                label = QLabel()
                label.setText(val[1])
                # Spacer的存在会使它们两个一行排列
                self.gl_mods.addWidget(checkbox)
                self.gl_mods.addWidget(label)
                self.__mods[val[1]] = (checkbox, label)

        mods_ = [i[1] for i in mods]

        for key in tuple(self.__mods.keys()):  # 移除没有的mod
            if key not in mods_:
                checkbox, label = self.__mods[key]
                self.gl_mods.removeWidget(checkbox)
                self.gl_mods.removeWidget(label)
                checkbox.deleteLater()
                label.deleteLater()
                self.__mods.pop(key)

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            self.refresh()
        return super().event(a0)

    def __rename(self):
        new_name = self.le_name.text()
        self.game.rename(new_name)
        if hasattr(self.game, "setting"):
            self.game.setting.deleteLater()
        self.game = Game(new_name)
        self.refresh()

    @pyqtSlot(bool)
    def on_pb_delete_clicked(self, _):
        reply = QMessageBox.warning(self,
                                    _translate("GameSetting", "删除"),
                                    _translate("GameSetting", "确定删除?"),
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.game.delete()
            self.close()

    @pyqtSlot(bool)
    def on_pb_changelogo_clicked(self, _):
        LogoChooser(self.game.name).show()
