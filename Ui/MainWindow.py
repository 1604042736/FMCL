from Core.Updata import Updata
from QtFBN.QFBNWindowManager import QFBNWindowManager
from Ui.Homepage.Homepage import Homepage
import Globals as g
from QtFBN.QFBNMessageBox import QFBNMessageBox
from PyQt5.QtWidgets import QApplication


class MainWindow(QFBNWindowManager):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Functional Minecraft Launcher")
        self.updata = Updata(g.TAG_NAME)
        self.updata.HasNewVersion.connect(self.has_updata)

    def ready(self) -> None:
        self.homepage = Homepage()
        self.homepage.show()
        self.check_updata()

    @g.run_as_thread
    def check_updata(self):
        self.updata.check()

    def has_updata(self, new_version):
        def ok():
            g.dmgr.add_task(f"安装新版本{new_version}",
                            self.updata, "updata", tuple())
        msgbox = QFBNMessageBox(
            QApplication.activeWindow(), f"有新版本{new_version}", "确定更新吗?")
        msgbox.Ok.connect(ok)
        msgbox.show()
