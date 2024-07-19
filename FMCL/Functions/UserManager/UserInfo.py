import logging
import traceback
import multitasking

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from qfluentwidgets import InfoBar, InfoBarPosition, MessageBox, CardWidget

from Core.User import User

from .ui_UserInfo import Ui_UserInfo


class UserInfo(CardWidget, Ui_UserInfo):
    __headGot = pyqtSignal(QPixmap)
    userSelectChanged = pyqtSignal(dict)
    userDeleted = pyqtSignal(dict)
    userRefreshed = pyqtSignal()

    def __init__(self, userinfo: dict) -> None:
        super().__init__()
        self.setupUi(self)
        self.userinfo = userinfo

        self.l_username.setText(userinfo["username"])
        _type = userinfo["type"]
        if _type == "offline":
            self.l_type.setText(self.tr("离线登录"))
            self.pb_changeprofile.hide()
        elif _type == "authlibInjector":
            self.l_type.setText(self.tr("外置登录"))
            self.l_mode.setText(User.get_servername(userinfo))

        self.__headGot.connect(self.__setHead)

        if userinfo == User.get_cur_user():
            self.rb_select.setChecked(True)

        self.__getHead()

    @multitasking.task
    def __getHead(self):
        head = User.get_head(self.userinfo)
        pixmap = QPixmap.fromImage(head)
        self.__headGot.emit(pixmap)

    def __setHead(self, head):
        head = head.scaled(32, 32)
        self.l_head.setPixmap(head)

    @pyqtSlot(bool)
    def on_rb_select_clicked(self, _):
        if self.rb_select.isChecked():
            self.userSelectChanged.emit(self.userinfo)
        self.rb_select.setChecked(True)

    @pyqtSlot(bool)
    def on_pb_del_clicked(self, _):
        def confirmDeleted():
            User.delete(self.userinfo)
            self.userDeleted.emit(self.userinfo)

        box = MessageBox("", self.tr("确认删除") + "?", self.window())
        box.yesSignal.connect(confirmDeleted)
        box.exec()

    @pyqtSlot(bool)
    def on_pb_refresh_clicked(self, _):
        try:
            User.refresh(self.userinfo)
            InfoBar.success(
                title=self.tr("刷新成功"),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window(),
            )
            self.userRefreshed.emit()
        except:
            logging.error(traceback.format_exc())
            InfoBar.error(
                title=self.tr("刷新失败,请尝试重新登录或看启动器日志"),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window(),
            )
