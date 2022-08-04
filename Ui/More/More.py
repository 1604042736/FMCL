import webbrowser
from Core.Update import Update
from QtFBN.QFBNMessageBox import QFBNMessageBox
from QtFBN.QFBNWidget import QFBNWidget
from Translate import tr
from Ui.More.ui_More import Ui_More
from PyQt5.QtCore import pyqtSlot
import Globals as g
import qtawesome as qta
from PyQt5.QtWidgets import QApplication


class More(QFBNWidget, Ui_More):
    icon_exp = 'qta.icon("ph.squares-four-fill")'

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(tr("更多"))
        self.groupBox.setTitle(tr("关于"))
        self.pb_opensourceurl.setText(tr("打开开源网址"))
        self.groupBox_2.setTitle(tr("鸣谢"))
        self.pb_openbangurl.setText(tr("打开网址"))
        self.label.setText(tr("bangbang93: 提供镜像源"))
        self.pb_openhmclurl.setText(tr("打开网址"))
        self.label_2.setText(tr("huanghongxun: 提供技术帮助(HMCL)"))

        self.setWindowIcon(eval(self.icon_exp))

        self.l_fmclversion.setText(
            self.l_fmclversion.text()+f"[v{g.TAG_NAME}]")

    @pyqtSlot(bool)
    def on_pb_opensourceurl_clicked(self, _):
        webbrowser.open("https://github.com/1604042736/FMCL")

    @pyqtSlot(bool)
    def on_pb_openbangurl_clicked(self, _):
        webbrowser.open("https://bmclapidoc.bangbang93.com")

    @pyqtSlot(bool)
    def on_pb_openhmclurl_clicked(self, _):
        webbrowser.open("https://github.com/huanghongxun/HMCL")

    @pyqtSlot(bool)
    def on_pb_openmczwurl_clicked(self, _):
        webbrowser.open("https://www.minecraftzw.com")

    @pyqtSlot(bool)
    def on_pb_checkupdate_clicked(self, _):
        self.update_ = Update(g.TAG_NAME)
        self.update_.HasNewVersion.connect(self.has_update)
        self.update_.NoNewVersion.connect(self.no_update)
        self.check_update()

    @g.run_as_thread
    def check_update(self):
        self.update_.check()

    def has_update(self, new_version):
        def ok():
            g.dmgr.add_task(f"{tr('安装新版本')} {new_version}",
                            self.update_, "update", tuple())
        msgbox = QFBNMessageBox.info(
            self, f"{tr('有新版本')} {new_version}", tr("确定更新吗")+"?", ok)
        msgbox.show("original")

    def no_update(self):
        msgbox = QFBNMessageBox.info(self, tr('没有新版本'), tr("这是最新版本"))
        msgbox.show("original")
