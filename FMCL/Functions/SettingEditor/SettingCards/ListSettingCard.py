
from PyQt5.QtWidgets import QFileDialog, QInputDialog
from qfluentwidgets import ComboBox, MessageBox, PushButton

from .SettingCard import SettingCard


class ListSettingCard(SettingCard):
    def __init__(self, id: str, setting) -> None:
        super().__init__(id, setting)
        self.w_value = ComboBox()
        self.w_value.addItems(setting.get(id))
        if len(self.setting.get(self.id)) > 0:
            self.w_value.setCurrentText(setting.get(id)[0])
        self.w_value.currentTextChanged.connect(self.promote_top)
        self.w_value.currentTextChanged.connect(self.sync)

        self.pb_add = PushButton()
        self.pb_add.setText(self.tr("添加"))
        self.pb_add.clicked.connect(self.add)
        self.pb_add.clicked.connect(self.sync)

        self.pb_delete = PushButton()
        self.pb_delete.setText(self.tr("删除"))
        self.pb_delete.clicked.connect(self.delete)
        self.pb_delete.clicked.connect(self.sync)

        self.check_atleast()
        self._layout.addWidget(self.w_value, 0, 0)
        if not setting.getAttr(self.id, "static", False):
            self._layout.addWidget(self.pb_add, 0, 1)
            self._layout.addWidget(self.pb_delete, 0, 2)

    def add(self):
        method = self.setting.getAttr(self.id, "method", "input")
        title = self.tr("添加")
        item = ""
        if method == "input":
            item = QInputDialog.getText(self, title, "")
            item = ("", item[0])[item[1]]
        elif method == "directory":
            item = QFileDialog.getExistingDirectory(self, title)
        elif method == "file":
            item = QFileDialog.getOpenFileName(self, title)
        else:  # 自定义方式
            method()
        if item:
            self.w_value.addItem(item)
            self.setting.set(self.id, self.setting.get(self.id)+[item])
            self.check_atleast()

    def delete(self):
        text = self.w_value.currentText()
        atleast = self.setting.getAttr(self.id, "atleast", 0)
        if self.w_value.count() <= atleast:
            MessageBox(self.tr("删除"),
                       f'{self.tr("至少有")}{atleast}',
                       self.window()).exec()
        else:
            def confirmDelete():
                self.setting.get(self.id).remove(text)
                self.refresh()
            box = MessageBox(self.tr("删除"),
                             self.tr("确定删除?"),
                             self.window())
            box.yesSignal.connect(confirmDelete)
            box.exec()

    def promote_top(self, text):
        if text:
            value = self.setting.get(self.id)
            value.remove(text)
            value.insert(0, text)
        self.check_atleast()

    def check_atleast(self):
        atleast = self.setting.getAttr(self.id, "atleast", 0)
        if self.w_value.count() <= atleast:
            self.pb_delete.setEnabled(False)
        else:
            self.pb_delete.setEnabled(True)

    def refresh(self):
        self.w_value.currentTextChanged.disconnect(self.promote_top)
        self.w_value.clear()
        self.w_value.addItems(self.setting.get(self.id))
        if len(self.setting.get(self.id)) > 0:
            self.w_value.setCurrentText(self.setting.get(self.id)[0])
        self.w_value.currentTextChanged.connect(self.promote_top)
        self.check_atleast()
        return super().refresh()
