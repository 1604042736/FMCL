from Core.Update import Update
from QtFBN.QFBNWidget import QFBNWidget
from QtFBN.QFBNWindowManager import QFBNWindowManager
from Translate import tr
from Ui.Desktop.Desktop import Desktop
from Ui.Homepage.Homepage import Homepage
import Globals as g
from QtFBN.QFBNMessageBox import QFBNMessageBox
from PyQt5.QtWidgets import QApplication, QPushButton, QMenu, QAction
import qtawesome as qta
from Ui.DownloadManager.DownloadManager import DownloadManager
import QtFBN as gg
from PyQt5.QtGui import QResizeEvent, QIcon
from PyQt5.QtCore import QPoint, Qt


class MainWindow(QFBNWindowManager):
    TASKBUTTON_WIDTH = 64
    MOREBUTTON_WIDTH = 30

    def __init__(self) -> None:
        super().__init__()
        self.ignore_widget = [Homepage, DownloadManager, Desktop]
        self.setWindowTitle("Functional Minecraft Launcher")
        self.update_ = Update(g.TAG_NAME)
        self.update_.HasNewVersion.connect(self.has_update)
        self.homepage = Homepage()
        self.desktop = Desktop()
        self.task_buttons = []
        self.page_map = {}

    def ready(self) -> None:
        self.desktop.show()
        self.homepage.show()
        self.setCurrentWidget(self.desktop)
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

    def on_win_ready(self) -> None:
        super().on_win_ready()

        self.win.remove_left_widget(self.pb_back)

        self.pb_desktop = QPushButton(self.win.title)
        self.pb_desktop.resize(
            self.win.title_button_width, self.win.title_height)
        self.pb_desktop.setIcon(qta.icon("ph.desktop"))
        self.pb_desktop.clicked.connect(
            lambda: self.setCurrentWidget(self.desktop))
        self.pb_desktop.setObjectName("pb_desktop")
        self.pb_desktop.setToolTip(tr("显示桌面"))
        self.win.add_right_widget(self.pb_desktop)

        self.add_task_button(self.homepage)

        self.more_button = QPushButton(self.win.title)
        self.more_button.setIcon(qta.icon("ri.more-fill"))
        self.more_button.resize(
            self.MOREBUTTON_WIDTH, self.win.title_height)
        self.more_button.hide()
        self.more_button.clicked.connect(self.show_exceed_menu)

        for key in tuple(self.page_map.keys()):
            try:
                key.objectName()  # 判断key是否被销毁
            except RuntimeError:
                self.add_task_button(self.page_map.pop(key))
        self.set_title_widget_state()

    def add_task_button(self, widget):
        for _, val in self.page_map.items():
            if val is widget:
                return
        if isinstance(widget, Homepage):
            self.pb_homepage = QPushButton(self.win.title)
            self.pb_homepage.resize(
                self.win.title_button_width, self.win.title_height)
            self.pb_homepage.setIcon(QIcon(":/Image/icon.png"))
            self.pb_homepage.clicked.connect(self.change_page)
            self.pb_homepage.setObjectName("pb_homepage")
            self.win.add_left_widget(self.pb_homepage, 0)
            self.page_map[self.pb_homepage] = widget
            return
        button = QPushButton(self.win.title)
        button.resize(self.TASKBUTTON_WIDTH,
                      self.win.title_height)
        button.clicked.connect(self.change_page)
        button.setText(widget.windowTitle())
        button.setObjectName("task_button")
        button.setIcon(widget.windowIcon())
        button.setToolTip(button.text())
        button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        button.customContextMenuRequested.connect(self.show_menu)
        button.show()
        self.win.add_left_widget(button, len(self.task_buttons)+1)
        self.page_map[button] = widget
        self.task_buttons.append(button)

    def show_menu(self):
        """显示标题栏按钮的右键菜单"""
        def new_instance(widget):
            try:
                widget.__class__().show()
            except Exception as e:
                self.notify(tr("错误"), e)
        button = self.sender()
        widget = self.page_map[button]
        menu = QMenu(self.win)

        a_close = QAction(tr("关闭"), self.win)
        a_close.setIcon(qta.icon("mdi6.close"))
        a_close.triggered.connect(widget.close)
        menu.addAction(a_close)

        a_new = QAction(widget.__class__.__name__, self.win)
        a_new.setIcon(widget.windowIcon())
        a_new.triggered.connect(lambda: new_instance(widget))
        menu.addAction(a_new)

        menu.exec_(QPoint(self.win.x()+button.x(),
                   self.win.y()+button.y()+self.win.title_height))

    def show_exceed_menu(self):
        """显示超出部分(以菜单的形式)"""
        menu = QMenu(self.win)
        for i in self.exceed_index:
            action = QAction(self.task_buttons[i].text(), self.win)
            action.triggered.connect(
                lambda _, button=self.task_buttons[i]: self.change_page(sender=button))
            action.setIcon(self.page_map[self.task_buttons[i]].windowIcon())
            menu.addAction(action)
        menu.exec_(QPoint(self.win.x()+self.more_button.x(),
                   self.win.y()+self.more_button.y()+self.win.title_height))

    def change_page(self, _=None, sender=None):
        if not sender:
            sender = self.sender()
        try:
            if self.currentWidget() == self.page_map[sender]:
                self.setCurrentWidget(self.desktop)
                return
            self.setCurrentWidget(self.page_map[sender])
        except KeyError:
            pass

    def catch_widget(self, widget) -> None:
        if not widget.__class__ in self.ignore_widget:
            for _, val in self.page_map.items():
                if val is widget:
                    break
            else:
                self.add_task_button(widget)
        self.adjust_titlewidgets()
        return super().catch_widget(widget)

    def release_widget(self, widget) -> None:
        if not widget.__class__ in self.ignore_widget:
            for key, val in self.page_map.items():
                if val is widget:
                    self.win.remove_left_widget(key)
                    self.task_buttons.remove(key)
                    self.page_map.pop(key)
                    break
        self.adjust_titlewidgets()
        super().release_widget(widget)

    def set_title_widget_state(self):
        super().set_title_widget_state()
        for key in tuple(self.page_map.keys()):
            val = self.page_map[key]
            if val == self.currentWidget():
                key.setStyleSheet(
                    f"background-color:{g.BUTTON_HOVER_COLOR};")
            else:
                key.setStyleSheet(f"""
QPushButton{{
    border:none;
}}
QPushButton:hover{{
    background-color:{g.BUTTON_HOVER_COLOR};
}}""")

    def setCurrentWidget(self, w) -> None:
        # 没有的话就添加
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

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.adjust_titlewidgets()
        return super().resizeEvent(a0)

    def adjust_titlewidgets(self):
        """调整标题栏的(左)控件"""
        left_width = 45
        right_width = self.win.right_width
        wintitle_width = self.win.wintitle_width
        width = self.win.width()
        self.exceed_index = []
        for i, w in enumerate(self.task_buttons):
            try:
                left_width += w.width()
                w.show()
                if left_width >= width-right_width-wintitle_width-self.MOREBUTTON_WIDTH:
                    self.exceed_index.append(i)
                    w.hide()
            except RuntimeError:
                self.task_buttons.remove(w)
        if self.exceed_index:
            self.more_button.show()
            self.win.add_left_widget(self.more_button)
        else:
            try:
                self.win.remove_left_widget(self.more_button)
            except:
                pass
