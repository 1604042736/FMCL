import os
import time
import qtawesome as qta
from Core import Version
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QEvent, QObject
from PyQt5.QtWidgets import QLabel, QWidget, QTreeWidgetItem
from qfluentwidgets import MessageBox, TreeWidget

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
        self.name = name
        self.game = Version(name)

        self.l_record.installEventFilter(self)

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

        timerec = self.game.get_timerec()
        count = len(timerec)
        if count != 0:
            total_time = 0
            for key, val in timerec.items():
                total_time += val["end"] - val["start"]
            total_time = int(total_time)
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

    def eventFilter(self, a0: QObject, a1: QEvent):
        if a0 == self.l_record:
            if a1.type() == QEvent.Type.MouseButtonRelease:
                TimeRecodeDetail(self.name).show()
        return super().eventFilter(a0, a1)


class TimeRecodeDetail(TreeWidget):
    __instances = {}
    __new_count = {}

    def __new__(cls, name: str):
        if name not in cls.__instances:
            cls.__instances[name] = super().__new__(cls)
            cls.__new_count[name] = 0
        cls.__new_count[name] += 1
        return cls.__instances[name]

    def __init__(self, name: str):
        if TimeRecodeDetail.__new_count[name] > 1:
            return
        super().__init__()
        self.resize(1000, 618)
        self.setWindowTitle(self.tr("游戏时间记录") + f": {name}")
        self.setWindowIcon(qta.icon("ph.record"))
        self.name = name
        self.game = Version(name)

        self.setColumnCount(4)
        self.setHeaderLabels(
            [
                self.tr("序号"),
                self.tr("开始时间"),
                self.tr("结束时间"),
                self.tr("持续时间"),
            ]
        )

        self.refresh()

    def refresh(self):
        self.clear()

        timerec = self.game.get_timerec()
        for key, val in timerec.items():
            item = QTreeWidgetItem()
            item.setText(0, str(int(key) + 1))
            item.setText(
                1,
                f'{time.strftime("%Y-%m-%d %H:%M:%S",time.localtime( val["start"]))}({val["start"]})',
            )
            item.setText(
                2,
                f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(val["end"]))}({val["end"]})',
            )
            total_time = int(val["end"] - val["start"])
            item.setText(
                3,
                self.tr("{hour_time}时{minute_time}分{second_time}秒").format(
                    hour_time=total_time // 3600,
                    minute_time=total_time % 3600 // 60,
                    second_time=total_time % 3600 % 60,
                ),
            )
            self.addTopLevelItem(item)

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            self.refresh()
        return super().event(a0)
