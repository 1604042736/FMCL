from QtFBN.QFBNDialog import QFBNDialog
from Translate import tr
from Ui.User.ui_NewUser import Ui_NewUser
from PyQt5.QtCore import pyqtSignal


class NewUser(QFBNDialog, Ui_NewUser):
    CreateUser = pyqtSignal(dict)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(tr("新用户"))
        self.pb_ok.setText(tr("确定"))
        self.le_offline_name.setPlaceholderText(tr("请输入用户名"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.offline), tr("离线登录"))
        self.pb_cancel.setText(tr("取消"))

        self.pb_cancel.clicked.connect(self.close)
        self.pb_ok.clicked.connect(self.create_user)

    def create_user(self):
        type = self.tabWidget.currentWidget().objectName()
        if type == "offline":
            name = self.le_offline_name.text()
        self.CreateUser.emit({"name": name, "type": type})
        self.close()
