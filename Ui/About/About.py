import platform
import webbrowser
from Core.Update import Update
from QtFBN.QFBNMessageBox import QFBNMessageBox
from QtFBN.QFBNWidget import QFBNWidget
from Translate import tr
from Ui.About.ui_About import Ui_About
from PyQt5.QtCore import pyqtSlot, PYQT_VERSION_STR
import Globals as g
import qtawesome as qta
from PyQt5.QtWidgets import QMessageBox, QLabel, QSpacerItem, QSizePolicy, QPushButton


class About(QFBNWidget, Ui_About):
    icon_exp = 'qta.icon("mdi.information-outline")'

    DEPENDENCES = [  # from requirements.txt
        ("beautifulsoup4", "4.11.1", "https://www.crummy.com/software/BeautifulSoup/"),
        ("Pillow", "9.2.0", "https://python-pillow.org/"),
        ("pywin32", "303", "https://sourceforge.net/projects/pywin32"),
        ("QtAwesome", "1.1.1", "https://pypi.org/project/QtAwesome/"),
        ("requests", "2.27.1", "http://python-requests.org/"),
        ("win32gui", "221.6", "https://sourceforge.net/projects/pywinauto"),
    ]

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(tr("关于"))
        self.groupBox.setTitle(tr("关于"))
        self.pb_opensourceurl.setText(tr("打开开源网址"))
        self.groupBox_2.setTitle(tr("鸣谢"))
        self.pb_openbangurl.setText(tr("打开网址"))
        self.label.setText(tr("bangbang93: 提供镜像源"))
        self.pb_openhmclurl.setText(tr("打开网址"))
        self.label_2.setText(tr("huanghongxun: 提供技术帮助(HMCL)"))
        self.groupBox_3.setTitle(tr("依赖"))
        self.pb_openpythonurl.setText(tr("打开网址"))
        self.pb_aboutqt.setText(tr("关于Qt"))

        self.setWindowIcon(eval(self.icon_exp))

        self.l_fmclversion.setText(
            f"Functional Minecraft Launcher[v{g.TAG_NAME}]")
        self.l_pythonversion.setText(f"Python[v{platform.python_version()}]")
        self.l_pyqtversion.setText(f"PyQt[v{PYQT_VERSION_STR}]")

        i = 2
        for name, version, url in self.DEPENDENCES:
            label = QLabel(self.groupBox_3, text=f"{name}[v{version}]")
            self.gridLayout_4.addWidget(label, i, 0, 1, 1)
            if url:
                spacerItem = QSpacerItem(
                    40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
                button = QPushButton(text=tr("打开网址"))
                button.clicked.connect(lambda _, url=url: webbrowser.open(url))
                self.gridLayout_4.addItem(spacerItem, i, 1, 1, 1)
                self.gridLayout_4.addWidget(button, i, 2, 1, 1)
            i += 1

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

    @pyqtSlot(bool)
    def on_pb_openpythonurl_clicked(self, _):
        webbrowser.open("https://python.org")

    @pyqtSlot(bool)
    def on_pb_aboutqt_clicked(self, _):
        QMessageBox.aboutQt(self, tr("关于Qt"))

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
