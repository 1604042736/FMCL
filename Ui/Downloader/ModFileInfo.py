from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFileDialog
from Core.Mod import Mod
import Globals as g


class ModFileInfo(QWidget):
    def __init__(self, info) -> None:
        super().__init__()
        self.info = info

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self, text=info['name'])
        self.pb_download = QPushButton(self, text='下载')
        self.pb_download.clicked.connect(self.download_mod_file)

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.pb_download)

        self.setLayout(self.hbox)

    def download_mod_file(self):
        path = QFileDialog.getExistingDirectory(self, '选择文件夹', '.')
        if path:
            g.dmgr.add_task("下载Mod", Mod(info=self.info, path=path),
                            "download_mod_file", tuple())
