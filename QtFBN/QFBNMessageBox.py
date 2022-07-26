from PyQt5.QtWidgets import QWidget, QFrame
from PyQt5.QtGui import QResizeEvent
from QtFBN.ui_Dialog import Ui_Dialog
from PyQt5.QtCore import pyqtSignal


class QFBNMessageBox(QWidget):
    class Dialog(QFrame, Ui_Dialog):
        def __init__(self, parent=None) -> None:
            super().__init__(parent)
            self.setupUi(self)

    Ok = pyqtSignal()

    def __init__(self, parent, title, msg, custom=None):
        super().__init__(parent)
        # 一般情况下parent都是QFBNWindow
        self.setGeometry(0, 30, parent.width(), parent.height()-30)
        setattr(parent, "_msgbox", self)

        if custom:
            self.w_dialog = custom
            self.w_dialog.setParent(self)
        else:
            self.w_dialog = self.Dialog(self)

            self.w_dialog.l_title.setText(title)
            self.w_dialog.l_msg.setText(msg)

        QWidget.show(self.w_dialog)
        self.w_dialog.resize(500, 309)

        self.w_dialog.pb_ok.clicked.connect(lambda: self.Ok.emit())
        self.w_dialog.pb_ok.clicked.connect(self.close)
        self.w_dialog.pb_cancel.clicked.connect(self.close)

        self.raise_()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.w_dialog.move(int((self.width()-self.w_dialog.width())/2),
                           int((self.height()-self.w_dialog.height())/2))
