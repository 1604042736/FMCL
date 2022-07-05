from QtFBN.QFBNWidget import QFBNWidget
from Ui.Downloader.Downloader import Downloader
from Ui.Homepage.ui_Homepage import Ui_Homepage
from PyQt5.QtGui import QResizeEvent
import qtawesome as qta
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget
from Ui.Launcher.Launcher import Launcher
from Ui.Setting.Setting import Setting
from Ui.User.User import User
import Globals as g


class Homepage(QFBNWidget, Ui_Homepage):
    PB_USER_INDEX = -1  # pb_user在panel_buttons中的索引

    default_panel_width = 45
    panel_width = default_panel_width
    panel_button_height = 45

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.panel_buttons = [[self.pb_detail, "top"],
                              [self.pb_launch, "top", "启动"],
                              [self.pb_download, "top", "下载"],
                              [self.pb_setting, "bottom", "设置"],
                              [self.pb_user, "bottom", "未选择用户"]]  # 面板上的按钮
        if g.cur_user:
            self.panel_buttons[self.PB_USER_INDEX][2] = g.cur_user["name"]

        self.launcher = Launcher()
        self.downloader = Downloader()
        self.user = User()
        self.user.CurUserChanged.connect(self.cur_user_changed)
        self.setting = Setting()

        self.pb_launch.setIcon(qta.icon("fa.power-off"))
        self.pb_launch.clicked.connect(lambda: self.set_ui(self.launcher))
        self.pb_launch.mouseDoubleClicked.connect(self.separate_ui)

        self.pb_download.setIcon(qta.icon("ph.download-simple-bold"))
        self.pb_download.clicked.connect(lambda: self.set_ui(self.downloader))
        self.pb_download.mouseDoubleClicked.connect(self.separate_ui)

        self.pb_detail.setIcon(qta.icon("msc.three-bars"))
        self.pb_detail.clicked.connect(self.show_panel_detail)

        self.pb_user.setIcon(qta.icon("ph.user-circle"))
        self.pb_user.clicked.connect(lambda: self.set_ui(self.user))
        self.pb_user.mouseDoubleClicked.connect(self.separate_ui)

        self.pb_setting.setIcon(qta.icon("ri.settings-5-line"))
        self.pb_setting.clicked.connect(lambda: self.set_ui(self.setting))
        self.pb_setting.mouseDoubleClicked.connect(self.separate_ui)

        self.panel_state = "simple"  # 面板状态

    def back_to_widget(self, w):
        if self.w_ui == w:
            self.set_ui(w)
        else:   # 当前w_ui显示的不是w
            w.hide()

    def set_ui(self, widget):
        if self.w_ui.parent() == self:
            self.w_ui.hide()  # 防止原来的干扰
        if widget.win != None:
            widget.win.close()
        self.w_ui = widget
        self.w_ui.setParent(self)
        QWidget.show(self.w_ui)
        self.resizeEvent(None)

    def separate_ui(self):
        self.w_ui.show()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.f_panel.resize(self.panel_width, self.height())
        self.w_ui.move(self.panel_width, 0)
        self.w_ui.resize(self.width()-self.panel_width, self.height())

        top_height = 0
        bottom_height = 0
        for i in self.panel_buttons:
            i[0].setIconSize(
                QSize(self.default_panel_width, self.default_panel_width))
            if i[1] == "top":
                i[0].move(0, top_height)
                i[0].resize(self.panel_width, self.panel_button_height)
                top_height += i[0].height()
            elif i[1] == "bottom":
                bottom_height += i[0].height()
                i[0].resize(self.panel_width, self.panel_button_height)
                i[0].move(0, self.height()-bottom_height)

    def show_panel_detail(self):
        """显示面板细节"""
        if self.panel_state == "simple":
            self.panel_width = self.default_panel_width*3
            for i in self.panel_buttons:
                if len(i) > 2:
                    i[0].setText(i[2])
            self.panel_state = "detail"
        elif self.panel_state == "detail":
            self.panel_width = self.default_panel_width
            for i in self.panel_buttons:
                i[0].setText("")
            self.panel_state = "simple"

        self.resizeEvent(None)

    def cur_user_changed(self):
        if g.cur_user:
            self.panel_buttons[self.PB_USER_INDEX][2] = g.cur_user["name"]
        else:
            self.panel_buttons[self.PB_USER_INDEX][2] = "未选择用户"
