import multitasking
from Core.User import User
from Kernel import Kernel
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame
from qfluentwidgets import InfoBar, InfoBarPosition, MessageBox

from .ui_UserInfo import Ui_UserInfo


class UserInfo(QFrame, Ui_UserInfo):
    userSelectChanged = pyqtSignal(dict)
    userDeleted = pyqtSignal(dict)
    __headGot = pyqtSignal(QPixmap)

    def __init__(self, userinfo: dict) -> None:
        super().__init__()
        self.setupUi(self)
        self.userinfo = userinfo

        self.l_username.setText(userinfo["username"])
        _type = userinfo["type"]
        if _type == "offline":
            self.l_type.setText(self.tr("离线登录"))
        elif _type == "authlibInjector":
            self.l_type.setText(self.tr("外置登录"))
            self.l_mode.setText(userinfo["mode"])

        multitasking.task(lambda: self.__headGot.emit(
            QPixmap.fromImage(User.get_head(userinfo))))()

        if userinfo == User.get_cur_user():
            self.rb_select.setChecked(True)

        self.__headGot.connect(self.__setHead)

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
        box = MessageBox("",
                         self.tr("确认删除")+"?",
                         self.window())
        box.yesSignal.connect(confirmDeleted)
        box.exec()

    @pyqtSlot(bool)
    def on_pb_refresh_clicked(self, _):
        result = User.refresh(self.userinfo)
        if result != None:
            if result["error"] == "ForbiddenOperationException":
                Kernel.execFunction(
                    "CreateUser", self.userinfo["mode"].lower())
                InfoBar.warning(
                    title=self.tr("请重新登录"),
                    content="",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self.window()
                )
            else:
                InfoBar.error(
                    title=self.tr("刷新失败"),
                    content="",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self.window()
                )
        else:
            InfoBar.success(
                title=self.tr("刷新成功"),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
