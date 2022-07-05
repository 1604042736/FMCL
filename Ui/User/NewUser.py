from QtFBN.QFBNWidget import QFBNWidget
from Ui.User.ui_NewUser import Ui_NewUser
from PyQt5.QtCore import pyqtSignal


class NewUser(QFBNWidget, Ui_NewUser):
    CreateUser = pyqtSignal(dict)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.pb_cancel.clicked.connect(self.close)
        self.pb_ok.clicked.connect(self.create_user)

    def create_user(self):
        type = self.tabWidget.currentWidget().objectName()
        if type == "offline":
            name = self.le_offline_name.text()
        self.CreateUser.emit({"name": name, "type": type})
        self.close()
