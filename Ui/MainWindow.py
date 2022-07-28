from Core.Updata import Updata
from QtFBN.QFBNWidget import QFBNWidget
from QtFBN.QFBNWindowManager import QFBNWindowManager
from Ui.Desktop.Desktop import Desktop
from Ui.Homepage.Homepage import Homepage
import Globals as g
from QtFBN.QFBNMessageBox import QFBNMessageBox
from PyQt5.QtWidgets import QApplication, QPushButton
import qtawesome as qta
from Ui.DownloadManager.DownloadManager import DownloadManager
import QtFBN as gg


class MainWindow(QFBNWindowManager):
    def __init__(self) -> None:
        super().__init__()
        self.ignore_widget = [Homepage, DownloadManager, Desktop]
        self.setWindowTitle("Functional Minecraft Launcher")
        self.updata = Updata(g.TAG_NAME)
        self.updata.HasNewVersion.connect(self.has_updata)
        self.homepage = Homepage()
        self.desktop = g.desktop
        self.task_buttons = []

    def ready(self) -> None:
        self.desktop.show()
        self.homepage.show()
        self.setCurrentWidget(self.desktop)
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
        super().on_win_ready()
        self.pb_homepage = QPushButton(self.win.title)
        self.pb_homepage.resize(
            self.win.title_button_width, self.win.title_height)
        self.pb_homepage.setIcon(qta.icon("fa.home"))
        self.pb_homepage.clicked.connect(self.change_page)
        self.pb_homepage.setObjectName("pb_homepage")
        self.win.add_left_widget(self.pb_homepage, 0)

        self.win.remove_left_widget(self.pb_back)

        self.pb_desktop = QPushButton(self.win.title)
        self.pb_desktop.resize(
            self.win.title_button_width, self.win.title_height)
        self.pb_desktop.setIcon(qta.icon("ph.desktop"))
        self.pb_desktop.clicked.connect(
            lambda: self.setCurrentWidget(self.desktop))
        self.pb_desktop.setObjectName("pb_desktop")
        self.win.add_right_widget(self.pb_desktop)

        self.page_map = {
            self.pb_homepage: self.homepage
        }

    def change_page(self):
        if self.currentWidget() == self.page_map[self.sender()]:
            self.setCurrentWidget(self.desktop)
            return
        self.setCurrentWidget(self.page_map[self.sender()])

    def catch_widget(self, widget) -> None:
        if not widget.__class__ in self.ignore_widget:
            for _, val in self.page_map.items():
                if val is widget:
                    break
            else:
                button = QPushButton(self.win.title)
                button.resize(64,
                              self.win.title_height)
                button.clicked.connect(self.change_page)
                button.setText(widget.windowTitle())
                button.setObjectName("task_button")
                button.setIcon(widget.windowIcon())
                button.show()
                self.win.add_left_widget(button, len(self.task_buttons)+1)
                self.page_map[button] = widget
                self.task_buttons.append(button)
        return super().catch_widget(widget)

    def release_widget(self, widget) -> None:
        if not widget.__class__ in self.ignore_widget:
            for key, val in self.page_map.items():
                if val is widget:
                    self.win.remove_left_widget(key)
                    self.task_buttons.remove(key)
                    self.page_map.pop(key)
                    break
        super().release_widget(widget)

    def set_title_widget_state(self):
        super().set_title_widget_state()
        for key, val in self.page_map.items():
            if val == self.currentWidget():
                key.setStyleSheet(f"background-color:{g.BUTTON_HOVER_COLOR};")
            else:
                key.setStyleSheet(f"""
QPushButton{{
    border:none;
}}
QPushButton:hover{{
    background-color:{g.BUTTON_HOVER_COLOR};
}}""")

    def setCurrentWidget(self, w) -> None:
        if self.indexOf(w) == -1:
            self.addWidget(w)
        if isinstance(w, QFBNWidget) and w.win != None:
            w.win.close()
        try:
            if QApplication.activeWindow().target is not gg.manager:
                gg.manager.reshow()
        except:
            pass
        return super().setCurrentWidget(w)
