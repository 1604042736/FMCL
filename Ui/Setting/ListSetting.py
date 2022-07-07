from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog, QInputDialog, QApplication
import qtawesome as qta
import Globals as g
from QtFBN.QFBNMessageBox import QFBNMessageBox


class ListSetting(QWidget):
    """类型为列表的设置"""

    def __init__(self, id, name, val, relation_id="", add_type="input", parent=None) -> None:
        super().__init__(parent)
        self.id = id
        self.name = name
        self.val = val
        self.add_type = add_type  # 添加的时侯的方式
        self.relation_id = relation_id  # 关联的id

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self)
        self.l_name.setText(name)

        self.cb_val = QComboBox(self)
        self.cb_val.currentIndexChanged.connect(self.save)
        self.cb_val.addItems(val)

        self.pb_add = QPushButton(self)
        self.pb_add.setIcon(qta.icon("msc.add"))
        self.pb_add.clicked.connect(self.add)

        self.pb_del = QPushButton(self)
        self.pb_del.setIcon(qta.icon("mdi.delete"))
        self.pb_del.clicked.connect(self.delete)

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.cb_val)
        self.hbox.addWidget(self.pb_add)
        self.hbox.addWidget(self.pb_del)

        self.setLayout(self.hbox)

    def save(self) -> tuple:
        l = self.get_all_text()
        # 将cur放在l的最前面
        cur = self.cb_val.currentText()
        l.remove(cur)
        l.insert(0, cur)

        setattr(g, self.id, l)
        if self.relation_id:
            setattr(g, self.relation_id, l[0])

    def get_all_text(self) -> list:
        l = []
        for i in range(self.cb_val.count()):
            l.append(self.cb_val.itemText(i))
        return l

    def add(self):
        text = ""
        if self.add_type == "input":
            text, ok = QInputDialog.getText(self, "添加", "输入要添加的内容")
            if not ok:
                text = ""
        elif self.add_type == "file":
            text = QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
        if text != "":
            self.cb_val.addItem(text)
            self.cb_val.setCurrentText(text)

    def delete(self):
        def ok():
            self.cb_val.removeItem(self.cb_val.currentIndex())
        msgbox = QFBNMessageBox(QApplication.activeWindow(), "删除", "确认删除?")
        msgbox.Ok.connect(ok)
        msgbox.show()
