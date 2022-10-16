from PyQt5.QtCore import QCoreApplication, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox

from .SettingWidget import SettingWidget
from .ui_ListSettingWidget import Ui_ListSettingWidget

_translate = QCoreApplication.translate


class ListSettingWidget(SettingWidget, Ui_ListSettingWidget):
    def __init__(self, id, value):
        if SettingWidget.new_count[id] > 1:
            return
        from ..Setting import Setting
        super().__init__(id, value)
        self.setupUi(self)
        self.setWindowTitle(self.window_title)
        self.setting = Setting().get_setting(id)
        self.refresh()

    def refresh(self):
        self.lw_values.clear()
        self.lw_values.addItems(self.value)
        return super().refresh()

    @pyqtSlot(bool)
    def on_pb_add_clicked(self, _):
        add = self.setting.get("add", "input")
        item = ""
        if add == "input":
            item = QInputDialog.getText(
                self, _translate("ListSettingWidget", "输入"), "")
            if not item[1]:
                item = ""
            else:
                item = item[0]
        elif add == "file":
            item = QFileDialog.getOpenFileName(
                self, _translate("ListSettingWidget", "选择文件"))
        elif add == "directory":
            item = QFileDialog.getExistingDirectory(
                self, _translate("ListSettingWidget", "选择目录"))
        else:
            add()
        if item:
            self.lw_values.addItem(item)
            self.setting["value"].append(item)

    @pyqtSlot(bool)
    def on_pb_delete_clicked(self, _):
        min_count = self.setting.get("min_count", 0)
        if self.lw_values.count() <= min_count:
            QMessageBox.warning(self, _translate(
                "ListSettingWidget", "错误"), f"至少有{min_count}个")
        else:
            item = self.lw_values.currentItem()
            if item:
                self.setting["value"].remove(item.text())
                self.lw_values.takeItem(self.lw_values.row(item))
                delete_callback = self.setting.get("delete", None)
                if delete_callback:
                    delete_callback(item.text())
            else:
                QMessageBox.warning(self, _translate(
                    "ListSettingWidget", "错误"), _translate("ListSettingWidget", "未选中"))

    @pyqtSlot(bool)
    def on_pb_promote_clicked(self, _):
        item = self.lw_values.currentItem()
        if item:
            row = self.lw_values.row(item)
            if row != 0:
                last_item = self.lw_values.item(row-1)
                self.lw_values.takeItem(self.lw_values.row(last_item))
                self.lw_values.insertItem(row, last_item)
                self.setting["value"][row], self.setting["value"][row -
                                                                  1] = self.setting["value"][row-1], self.setting["value"][row]
                self.lw_values.setCurrentItem(item)
        else:
            QMessageBox.warning(self, _translate(
                "ListSettingWidget", "错误"), _translate("ListSettingWidget", "未选中"))

    @pyqtSlot(bool)
    def on_pb_promote_top_clicked(self, _):
        item = self.lw_values.currentItem()
        if item:
            row = self.lw_values.row(item)
            self.lw_values.takeItem(row)
            self.lw_values.insertItem(0, item)
            self.setting["value"].remove(item.text())
            self.setting["value"].insert(0, item.text())
            self.lw_values.setCurrentItem(item)
        else:
            QMessageBox.warning(self, _translate(
                "ListSettingWidget", "错误"), _translate("ListSettingWidget", "未选中"))
