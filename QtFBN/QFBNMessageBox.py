from PyQt5.QtWidgets import QWidget, QFrame, QLabel
from PyQt5.QtGui import QResizeEvent
from QtFBN.QFBNWindow import QFBNWindow
from QtFBN.ui_Dialog import Ui_Dialog
from PyQt5.QtCore import pyqtSignal
from QtFBN.QFBNWindowManager import QFBNWindowManager


class QFBNMessageBox(QWidget):
    class Dialog(QFrame, Ui_Dialog):
        def __init__(self, parent=None) -> None:
            super().__init__(parent)
            self.setupUi(self)

    Ok = pyqtSignal()

    def __init__(self, parent, title, msg, custom: QWidget = None):
        if isinstance(parent, QFBNWindow):
            parent = parent.target
            if isinstance(parent, QFBNWindowManager):
                if parent.currentWidget():
                    parent = parent.currentWidget()
        super().__init__(parent)
        # 一般情况下parent都是QFBNWindow
        self.setGeometry(0, 0, parent.width(), parent.height())
        setattr(parent, "_msgbox", self)

        self.w_dialog = self.Dialog(self)

        if custom:
            self.w_dialog.l_title.setText(custom.windowTitle())
            self.w_dialog.widget = custom
            self.w_dialog.widget.setParent(self.w_dialog)
            self.w_dialog.widget.setGeometry(0, 32, 500, 277)
            self.w_dialog.pb_ok.hide()
            self.w_dialog.pb_cancel.hide()
            QWidget.show(self.w_dialog.widget)
        else:
            self.w_dialog.l_title.setText(title)
            self.w_dialog.widget = QLabel(msg, self.w_dialog)
            self.w_dialog.widget.setGeometry(0, 32, 500, 245)

        QWidget.show(self.w_dialog)
        self.w_dialog.resize(500, 309)

        self.w_dialog.pb_ok.clicked.connect(lambda: self.Ok.emit())
        self.w_dialog.pb_ok.clicked.connect(self.close)
        self.w_dialog.pb_cancel.clicked.connect(self.close)

        if hasattr(self.w_dialog.widget, "pb_ok"):
            self.w_dialog.widget.pb_ok.clicked.connect(lambda: self.Ok.emit())
            self.w_dialog.widget.pb_ok.clicked.connect(self.close)
        if hasattr(self.w_dialog.widget, "pb_cancel"):
            self.w_dialog.widget.pb_cancel.clicked.connect(self.close)

        self.raise_()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.w_dialog.move(int((self.width()-self.w_dialog.width())/2),
                           int((self.height()-self.w_dialog.height())/2))
