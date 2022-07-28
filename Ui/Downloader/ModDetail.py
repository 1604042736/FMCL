from QtFBN.QFBNWidget import QFBNWidget
from Ui.Downloader.ModFileInfo import ModFileInfo
from Ui.Downloader.ui_ModDetail import Ui_ModDetail
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout
from Core.Mod import Mod
import Globals as g


class ModDetail(QFBNWidget, Ui_ModDetail):
    _ModFilesOut = pyqtSignal(list)

    def __init__(self, mod_info, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
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
        # TODO 已知bug：文件太多会导致不显示
        if files:
            from Ui.Downloader.ModInfo import ModInfo
            if files[0]["dependencies"]:
                dependencies = files[0]["dependencies"]
                gb = QGroupBox()
                vbox = QVBoxLayout(gb)
                for i in dependencies:
                    vbox.addWidget(ModInfo(i, True))
                self.tb_modfiles.removeItem(0)
                self.tb_modfiles.addItem(gb, "前置Mod")
        self.version_groups = {}
        for i in files:
            if i["game_version"] not in self.version_groups:
                gb = QGroupBox()
                vbox = QVBoxLayout(gb)
                self.version_groups[i["game_version"]] = [gb, vbox]
            gb, vbox = self.version_groups[i["game_version"]]
            vbox.addWidget(ModFileInfo(i))
        for key, val in self.version_groups.items():
            self.tb_modfiles.addItem(val[0], key)

    @g.run_as_thread
    def get_modfiles(self):
        files = Mod(info=self.mod_info).get_mod_files()
        self._ModFilesOut.emit(files)
