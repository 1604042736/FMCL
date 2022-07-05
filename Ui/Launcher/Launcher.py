from Core.Launch import Launch
from QtFBN.QFBNWidget import QFBNWidget
from Ui.Launcher.ChooseVersion import ChooseVersion
from Ui.Launcher.ui_Launcher import Ui_Launcher
import Globals as g
from Ui.VersionManager.VersionManager import VersionManager
from PyQt5.QtCore import QUrl


class Launcher(QFBNWidget, Ui_Launcher):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.pb_start.clicked.connect(lambda:self.launch_game(g.cur_version))
        self.pb_chooseversion.clicked.connect(self.choose_version)
        self.pb_manageversion.clicked.connect(
            lambda: self.open_version_manager(g.cur_version))

        self.quickWidget.setSource(QUrl(g.homepage_qml))

        if g.cur_version:
            self.pb_start.setText(f'开始游戏:{g.cur_version}')

    def launch_game(self, version):
        g.dmgr.add_task(f"启动{version}", Launch(
            version), "launch", (g.java_path,
                                       g.cur_user["name"],
                                       g.width,
                                       g.height,
                                       g.maxmem,
                                       g.minmem))

    def choose_version(self):
        chooseversion = ChooseVersion()
        chooseversion.VersionChose.connect(self.set_chose_version)
        chooseversion.OpenVersionManager.connect(self.open_version_manager)
        chooseversion.DirectLaunch.connect(self.launch_game)
        chooseversion.show()

    def set_chose_version(self, version):
        g.cur_version = version
        self.pb_start.setText(f'开始游戏:{version}')

    def open_version_manager(self, name):
        if name:
            versionmanager = VersionManager(name)
            versionmanager.GameDeleted.connect(self.refresh_cur_version)
            versionmanager.show()

    def refresh_cur_version(self):
        if g.cur_version:
            self.pb_start.setText(f'开始游戏:{g.cur_version}')
        else:
            self.pb_start.setText(f'开始游戏')
