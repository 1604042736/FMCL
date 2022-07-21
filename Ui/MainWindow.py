from matplotlib import widgets
from Core.Updata import Updata
from QtFBN.QFBNWindowManager import QFBNWindowManager
from Ui.Homepage.Homepage import Homepage
import Globals as g
from QtFBN.QFBNMessageBox import QFBNMessageBox
from PyQt5.QtWidgets import QApplication, QPushButton
import qtawesome as qta


class MainWindow(QFBNWindowManager):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Functional Minecraft Launcher")
        self.updata = Updata(g.TAG_NAME)
        self.updata.HasNewVersion.connect(self.has_updata)
        self.homepage = Homepage()
        self.task_buttons = []

    def ready(self) -> None:
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

    def on_win_ready(self) -> None:
        self.pb_homepage = QPushButton(self.win.title)
        self.pb_homepage.resize(
            self.win.title_button_width, self.win.title_height)
        self.pb_homepage.setIcon(qta.icon("fa.home"))
        self.pb_homepage.clicked.connect(self.change_page)
        self.pb_homepage.setObjectName("pb_homepage")
        self.pb_homepage.setCheckable(True)
        self.pb_homepage.setAutoExclusive(True)
        self.win.add_left_widget(self.pb_homepage, 0)

        self.page_map = {
            self.pb_homepage: self.homepage
        }
        self.donot_show = {
            self.pb_homepage: False
        }
        return super().on_win_ready()

    def change_page(self):
        widget = self.currentWidget()
        self.removeWidget(widget)
        if not self.donot_show[self.sender()]:
            self.page_map[self.sender()].show()
        for key in self.donot_show:
            if key is not self.sender():
                self.donot_show[key] = False
        self.donot_show[self.sender()] = not self.donot_show[self.sender()]

    def catch_widget(self, widget) -> None:
        if not isinstance(widget, Homepage):
            self.removeWidget(self.currentWidget())
            for _, val in self.page_map.items():
                if val is widget:
                    break
            else:
                button = QPushButton(self.win.title)
                button.resize(self.win.title_button_width,
                              self.win.title_height)
                button.clicked.connect(self.change_page)
                button.setText(widget.windowTitle())
                button.setObjectName(f"task_button{len(self.task_buttons)}")
                button.setCheckable(True)
                button.setAutoExclusive(True)
                button.setIcon(widget.windowIcon())
                button.show()
                self.win.add_left_widget(button, len(self.task_buttons)+1)
                self.page_map[button] = widget
                self.donot_show[button] = True
                self.task_buttons.append(button)
        return super().catch_widget(widget)

    def release_widget(self, widget) -> None:
        if not isinstance(widget, Homepage):
            for key, val in self.page_map.items():
                if val is widget:
                    self.win.remove_left_widget(key)
                    self.task_buttons.remove(key)
                    self.page_map.pop(key)
                    self.donot_show.pop(key)
                    break
        return super().release_widget(widget)
