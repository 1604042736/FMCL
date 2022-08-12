from QtFBN.QFBNWidget import QFBNWidget
from Translate import tr
from Ui.Downloader.ModFileInfo import ModFileInfo
from Ui.Downloader.ui_ModDetail import Ui_ModDetail
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QListWidget, QListWidgetItem
from Core.Mod import Mod
import Globals as g
import qtawesome as qta


class ModDetail(QFBNWidget, Ui_ModDetail):
    _ModFilesOut = pyqtSignal(list)

    def __init__(self, mod_info, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(tr("模组细节")+f":{mod_info['title']}")
        self.setWindowIcon(qta.icon("mdi.details"))

        self.tb_modfiles.removeItem(0)

        self.mod_info = mod_info

        self._ModFilesOut.connect(self.set_modfiles)

        self.set_info()
        self.get_modfiles()

    def set_info(self):
        self.l_title.setText(self.mod_info['title'])
        self.l_describe.setText(self.mod_info['description'])
        self.l_describe.setWordWrap(True)
        self.l_describe.setAlignment(Qt.AlignTop)

    def set_modfiles(self, files):
        def add_item(lw: QListWidget, widget):
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 32))
            lw.addItem(item)
            lw.setItemWidget(item, widget)
        if files:
            from Ui.Downloader.ModInfo import ModInfo
            if files[0]["dependencies"]:
                dependencies = files[0]["dependencies"]
                lw = QListWidget()
                for i in dependencies:
                    add_item(lw, ModInfo(i, True))
                self.tb_modfiles.addItem(lw, tr("前置Mod"))
        self.version_groups = {}
        for i in files:
            if i["game_version"] not in self.version_groups:
                lw = QListWidget()
                self.version_groups[i["game_version"]] = lw
            lw = self.version_groups[i["game_version"]]
            add_item(lw, ModFileInfo(i))
        for key, val in self.version_groups.items():
            self.tb_modfiles.addItem(val, key)

    @g.run_as_thread
    def get_modfiles(self):
        files = Mod(info=self.mod_info).get_mod_files()
        self._ModFilesOut.emit(files)
