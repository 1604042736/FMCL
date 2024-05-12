import os
import qtawesome as qta
from Core import Version
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QEvent
from PyQt5.QtWidgets import QLabel, QWidget
from qfluentwidgets import MessageBox

from .ui_GameInfo import Ui_GameInfo


class GameInfo(QWidget, Ui_GameInfo):
    gameNameChanged = pyqtSignal(str)
    gameDeleted = pyqtSignal()

    def __init__(self, name: str) -> None:
        super().__init__()
        self.setupUi(self)
        t = self.tr("游戏信息")
        self.setWindowTitle(f"{t}:{name}")
        self.setWindowIcon(qta.icon("mdi6.information-outline"))
        self.__info_translate = {
            "version": self.tr("版本"),
            "forge_version": self.tr("Forge版本"),
            "fabric_version": self.tr("Fabric版本"),
        }
        self.game = Version(name)

        self.refresh()

    def refresh(self):
        self.le_name.setText(self.game.name)

        pixmap = self.game.get_pixmap()
        if not pixmap.isNull():
            self.l_logo.setPixmap(pixmap.scaled(64, 64))

        for i in range(self.gl_versions.count() - 1, -1, -1):
            item = self.gl_versions.itemAt(i)
            self.gl_versions.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

        self.info = self.game.get_info()
        for key, val in self.info.items():
            if val:
                label = QLabel()
                label.setText(f"{self.__info_translate[key]}: {val}")
                self.gl_versions.addWidget(label)

        game_path = self.game.get_game_path()
        timerec_path = os.path.join(game_path, "FMCL", "TimeRecord.txt")
        if os.path.exists(timerec_path):
            content = [
                list(map(int, line.strip().split(":")))
                for line in open(timerec_path).readlines()
            ]
            if len(content) != 0:
                total_time = 0
                count = 0
                i = 0
                while i < len(content) - 1:
                    if content[i][0] == 0:
                        count += 1
                    if content[i][0] == 0 and content[i + 1][0] == 1:
                        total_time += content[i + 1][1] - content[i][1]
                        i += 2
                    else:
                        i += 1
                if i < len(content) and content[i][0] == 0:
                    count += 1
                self.l_record.setText(
                    self.tr(
                        "自有记录以来, 一共启动了{count}次游戏, 总时长{hour_time}时{minute_time}分{second_time}秒"
                    ).format(
                        count=count,
                        hour_time=total_time // 3600,
                        minute_time=total_time % 3600 // 60,
                        second_time=total_time % 3600 % 60,
                    )
                )

    @pyqtSlot(bool)
    def on_pb_opendir_clicked(self, _):
        self.game.open_directory()

    @pyqtSlot(bool)
    def on_pb_resourcepack_clicked(self, _):
        os.startfile(self.game.get_resourcepacks_path())

    @pyqtSlot(bool)
    def on_pb_shaderpack_clicked(self, _):
        os.startfile(self.game.get_shaderpacks_path())

    @pyqtSlot(bool)
    def on_pb_delete_clicked(self, _):
        def confirmDelete():
            self.game.delete()
            self.gameDeleted.emit()
            self.close()

        box = MessageBox(self.tr("删除"), self.tr("确定删除?"), self)
        box.yesSignal.connect(confirmDelete)
        box.exec()

    @pyqtSlot()
    def on_le_name_editingFinished(self):
        new_name = self.le_name.text()
        if new_name == self.game.name:
            return
        self.game.rename(new_name)
        if hasattr(self.game, "setting"):
            self.game.setting = None
        self.game = Version(new_name)
        self.refresh()
        self.gameNameChanged.emit(new_name)

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            self.refresh()
        elif a0.type() == QEvent.Type.WindowActivate:
            self.refresh()
        return super().event(a0)
