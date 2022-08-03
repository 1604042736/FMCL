from QtFBN.QFBNDialog import QFBNDialog
from QtFBN.ui_QFBNInfoDialog import Ui_QFBNInfoDialog


class QFBNMessageBox(QFBNDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

    @classmethod
    def info(cls, parent, title, msg, ok_connect=None):
        msgbox = cls(parent)
        ui = Ui_QFBNInfoDialog()
        ui.setupUi(msgbox)
        ui.l_msg.setText(msg)
        msgbox.setWindowTitle(title)

        if ok_connect != None:
            ui.pb_ok.clicked.connect(ok_connect)
        ui.pb_ok.clicked.connect(msgbox.close)
        ui.pb_cancel.clicked.connect(msgbox.close)

        return msgbox
