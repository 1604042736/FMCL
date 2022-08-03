from QtFBN.QFBNWidget import QFBNWidget
from Translate import tr
from Ui.User.NewUser import NewUser
from Ui.User.UserInfo import UserInfo
from Ui.User.ui_User import Ui_User
import qtawesome as qta
import Globals as g
from PyQt5.QtWidgets import QListWidgetItem, QApplication
from PyQt5.QtCore import QSize, pyqtSignal
from QtFBN.QFBNMessageBox import QFBNMessageBox


class User(QFBNWidget, Ui_User):
    CurUserChanged = pyqtSignal()

    def __init__(self, connection=None, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(tr("用户"))
        self.setWindowIcon(qta.icon("ph.user-circle"))
        if connection:
            self.CurUserChanged.connect(connection)
        self.set_users()

        self.pb_add.setIcon(qta.icon("msc.add"))
        self.pb_add.clicked.connect(self.add_user)

    def add_user(self):
        newuser = NewUser(self)
        newuser.CreateUser.connect(self.create_user)
        newuser.show("original")

    def set_users(self):
        def add_item(i):
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 32))
            widget = UserInfo(i)
            widget.CurUserChanged.connect(self.set_cur_user)
            widget.UserDel.connect(self.del_user)
            self.lw_users.addItem(item)
            self.lw_users.setItemWidget(item, widget)

        self.lw_users.clear()

        if g.cur_user:  # 将当前用户放在列表的第一位
            add_item(g.cur_user)

        for i in g.users:
            if i != g.cur_user:
                add_item(i)

    def set_cur_user(self, info):
        g.cur_user = info
        self.set_users()
        self.CurUserChanged.emit()

    def del_user(self, info):
        def ok():
            g.users.remove(info)
            if g.cur_user == info:
                g.cur_user = None
            self.set_users()
            self.CurUserChanged.emit()
        msgbox = QFBNMessageBox.info(self, tr("删除"), tr("确认删除")+"?", ok)
        msgbox.show("original")

    def create_user(self, info):
        g.users.append(info)
        self.set_users()
        if not g.cur_user:
            g.cur_user = info
        self.CurUserChanged.emit()
