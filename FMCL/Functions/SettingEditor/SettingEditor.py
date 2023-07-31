import qtawesome as qta
from FMCL.Functions.LanguageChooser import LanguageChooser
from Kernel import Kernel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QTreeWidgetItem, QWidget
from Setting import Setting

from .SettingItems import SettingItem
from .ui_SettingEditor import Ui_SettingEditor

_translate = Kernel.translate


class SettingEditor(QWidget, Ui_SettingEditor):
    instances = {}
    new_count = {}

    def __new__(cls, setting: Setting):
        if setting.setting_path not in SettingEditor.instances:
            SettingEditor.instances[setting.setting_path] = super().__new__(
                cls)
            SettingEditor.new_count[setting.setting_path] = 0
        SettingEditor.new_count[setting.setting_path] += 1
        return SettingEditor.instances[setting.setting_path]

    def __init__(self, setting: Setting):
        if SettingEditor.new_count[setting.setting_path] > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.resize(1000, 618)
        self.setWindowIcon(qta.icon("ri.settings-5-line"))
        self.splitter.setSizes([100, 500])

        self.setting = setting
        self.items = {}
        self.item_widget_id = []
        self.setting_items = []

        for id, val in self.setting.items():
            splitids = id.split(".")
            for i, splitid in enumerate(splitids):
                totalid = ".".join(splitids[:i+1])
                lastid = ".".join(splitids[:i])
                if totalid in self.items:
                    continue

                root = self.items.get(("???", lastid)[i-1 >= 0], None)
                item = QTreeWidgetItem()
                text = self.setting.getAttr(totalid, "name")
                text = _translate(text)
                item.setText(0, text)
                self.addTreeItem(root, item)
                self.items[totalid] = item

                widget = QLabel()
                widget.setText(text)
                font = widget.font()
                font.setBold((False, True)[i == 0])
                font.setPixelSize(16-i*2)
                widget.setFont(font)
                self.gl_setting.addWidget(widget)
                self.item_widget_id.append((item, widget, totalid))

            settingcard = self.setting.getAttr(
                id, "settingcard", lambda id=id: SettingItem(id, self.setting))()
            self.gl_setting.addWidget(settingcard)
            self.setting_items.append(settingcard)

    def addTreeItem(self, root: QTreeWidgetItem | None, item: QTreeWidgetItem):
        if root == None:
            self.tw_setting.addTopLevelItem(item)
        else:
            root.addChild(item)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_tw_setting_itemClicked(self, item, _):
        for item_, widget, _ in self.item_widget_id:
            if item_ == item:
                self.sa_setting.verticalScrollBar().setValue(widget.pos().y())
                break

    def turnTo(self, id):
        for _, widget, id_ in self.item_widget_id:
            if id_ == id:
                self.sa_setting.verticalScrollBar().setValue(widget.pos().y())
                break

    def show(self, id="") -> None:
        if id:
            self.turnTo(id)
        return super().show()

    def refresh(self):
        for i in self.setting_items:
            if hasattr(i, "refresh"):
                i.refresh()

    @pyqtSlot(bool)
    def on_pb_refresh_clicked(self):
        self.refresh()
