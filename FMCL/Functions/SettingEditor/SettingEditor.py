import qtawesome as qta
from Events import *
from PyQt5.QtCore import pyqtSlot, QEvent
from PyQt5.QtWidgets import QLabel, QTreeWidgetItem, QWidget, qApp
from qfluentwidgets import TransparentToolButton, PrimaryPushButton
from Setting import Setting

from .SettingCards import SettingCard
from .ui_SettingEditor import Ui_SettingEditor


class SettingEditor(QWidget, Ui_SettingEditor):
    instances = {}
    new_count = {}

    def __new__(cls, setting: Setting):
        if setting.setting_path not in SettingEditor.instances:
            SettingEditor.instances[setting.setting_path] = super().__new__(cls)
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
        self.setting_cards = {}
        row = 1
        for id, val in self.setting.items():
            splitids = id.split(".")
            for i, splitid in enumerate(splitids):
                totalid = ".".join(splitids[: i + 1])
                lastid = ".".join(splitids[:i])
                if totalid in self.items:
                    continue
                root = self.items.get(("???", lastid)[i - 1 >= 0], None)
                item = QTreeWidgetItem()
                text = self.setting.getAttr(totalid, "name")
                item.setText(0, text)
                self.addTreeItem(root, item)
                self.items[totalid] = item

                widget = QLabel()
                widget.setText(text)
                font = widget.font()
                font.setBold((False, True)[i == 0])
                font.setPixelSize(16 - i * 2)
                widget.setFont(font)
                self.gl_setting.addWidget(widget, row, 1)
                self.item_widget_id.append((item, widget, totalid))

                link = self.setting.getAttr(totalid, "link", None)
                if link:
                    button = PrimaryPushButton()
                    button.setText(link["name"])
                    button.clicked.connect(lambda _, l=link: l["action"]())
                    self.gl_setting.addWidget(button, row, 2)
                row += 1

            if "callback" not in setting.attrs[id]:
                setting.attrs[id]["callback"] = []
            setting.attrs[id]["callback"].append(lambda *_: self.refresh())

            settingcard = self.setting.getAttr(
                id, "settingcard", lambda id=id: SettingCard(id, self.setting)
            )()
            self.gl_setting.addWidget(settingcard, row, 1, 1, 2)
            self.setting_cards[id] = settingcard
            row += 1

        self.pb_refresh = TransparentToolButton()
        self.pb_refresh.resize(46, 32)
        self.pb_refresh.setIcon(qta.icon("mdi.refresh"))
        self.pb_refresh.clicked.connect(lambda: self.refresh())

        self.checkCondition()

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
        super().show()
        if id:
            self.turnTo(id)

    def refresh(self):
        for i in self.setting_cards.values():
            if hasattr(i, "refresh"):
                i.refresh()
        self.checkCondition()

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_refresh, "right"))
            self.refresh()
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_refresh))
            self.pb_refresh.setParent(self)
        return super().event(a0)

    def checkCondition(self):
        enable = {}
        disable = []
        for key, val in self.setting.attrs.items():
            enable[key] = val.get("enable_condition", lambda _: True)(self.setting)
            if not enable[key]:
                disable.append(key)
        for id in disable:  # 将子设置项设为不可用
            for key, val in self.setting.attrs.items():
                if key.find(id) == 0:
                    enable[key] = False
        for _, widget, id in self.item_widget_id:
            widget.setEnabled(enable[id])
            if id in self.setting_cards:
                self.setting_cards[id].setEnabled(enable[id])
