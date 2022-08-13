from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog, QInputDialog, QApplication
import qtawesome as qta
import Globals as g
from QtFBN.QFBNMessageBox import QFBNMessageBox
from Translate import tr
from .SettingItem import SettingItem


class ListSetting(SettingItem):
    """类型为列表的设置"""

    def __init__(self, id, name, val, relation_id="", add_type="input", do_after_save=None, target=g, parent=None) -> None:
        super().__init__(id, name, val, do_after_save, target, parent)
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

    def save(self):
        l = self.get_all_text()
        # 将cur放在l的最前面
        cur = self.cb_val.currentText()
        l.remove(cur)
        l.insert(0, cur)

        setattr(self.target, self.id, l)
        if self.relation_id:
            setattr(self.target, self.relation_id, l[0])
        super().save()

    def get_all_text(self) -> list:
        l = []
        for i in range(self.cb_val.count()):
            l.append(self.cb_val.itemText(i))
        return l

    def add(self):
        text = ""
        if self.add_type == "input":
            text, ok = QInputDialog.getText(self, tr("添加"), tr("输入要添加的内容"))
            if not ok:
                text = ""
        elif self.add_type == "file":
            text = QFileDialog.getExistingDirectory(self, tr("选择文件夹"), "./")
        if text != "":
            self.cb_val.addItem(text)
            self.cb_val.setCurrentText(text)

    def delete(self):
        def ok():
            self.cb_val.removeItem(self.cb_val.currentIndex())
        msgbox = QFBNMessageBox.info(self, tr("删除"), tr("确认删除")+"?", ok)
        msgbox.show("original")
