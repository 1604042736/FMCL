from QtFBN.QFBNWidget import QFBNWidget
from Ui.Downloader.Minecraft import Minecraft
from Ui.Downloader.ui_Downloader import Ui_Downloader
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget


class Downloader(QFBNWidget, Ui_Downloader):
    panel_height = 45
    panel_button_width = 64
    panel_button_height = panel_height

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.panel_buttons = [self.pb_minecraft]

        self.minecraft = Minecraft()

        self.pb_minecraft.clicked.connect(lambda: self.set_ui(self.minecraft))
        self.pb_minecraft.mouseDoubleClicked.connect(self.separate_ui)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.f_panel.resize(self.width(), self.panel_height)
        self.w_ui.move(0, self.panel_height)
        self.w_ui.resize(self.width(), self.height()-self.panel_height)

        for button in self.panel_buttons:  # 先设置大小
            button.resize(self.panel_button_width, self.panel_button_height)

        buttons_width = sum([i.width() for i in self.panel_buttons])
        button_x = int((self.width()-buttons_width)/2)
        for button in self.panel_buttons:
            button.move(button_x, 0)
            button_x += button.width()

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
