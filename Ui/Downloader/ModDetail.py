import webbrowser
from QtFBN.QFBNWidget import QFBNWidget
from Ui.Downloader.ModFileInfo import ModFileInfo
from Ui.Downloader.ui_ModDetail import Ui_ModDetail
from PyQt5.QtCore import Qt, pyqtSlot, QSize, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem
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
        self.l_name.setText(self.mod_info['name'])
        self.l_name.setStyleSheet('font-weight: bold;')
        self.l_describe.setText(self.mod_info['describe'])
        self.l_describe.setWordWrap(True)
        self.l_describe.setAlignment(Qt.AlignTop)

    @pyqtSlot(bool)
    def on_pb_mcmod_clicked(self, _):
        webbrowser.open(self.mod_info['mcmod_url'])

    @pyqtSlot(bool)
    def on_pb_curseforge_clicked(self, _):
        webbrowser.open(self.mod_info['curseforge_url'])

    def set_modfiles(self, files):
        self.lw_modfiles.clear()
        for i in files:
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 64))
            widget = ModFileInfo(i)
            self.lw_modfiles.addItem(item)
            self.lw_modfiles.setItemWidget(item, widget)

    @g.run_as_thread
    def get_modfiles(self):
        files = Mod(info=self.mod_info).get_mod_files()
        self._ModFilesOut.emit(files)
