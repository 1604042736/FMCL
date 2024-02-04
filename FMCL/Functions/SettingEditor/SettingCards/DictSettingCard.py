import qtawesome as qta

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QInputDialog
from qfluentwidgets import TransparentToolButton

from .SettingCard import SettingCard

from .ui_DictSettingCard import Ui_DictSettingCard


class DictSettingCard(SettingCard, Ui_DictSettingCard):
    def __init__(self, getter, attrgetter, setter, attrsetter) -> None:
        super().__init__(getter, attrgetter, setter, attrsetter)
        self.setupUi(self)
        self.pb_add.setIcon(qta.icon("msc.add"))

        if self.attrgetter("element_type") == None:
            self.attrsetter("element_type", dict())

        self.refresh()

    def refresh(self):
        while self.gl_elements.count():
            item = self.gl_elements.takeAt(0)
            if item.widget() != None:
                item.widget().deleteLater()
        self.button_label_card = []
        for i, (key, val) in enumerate(self.getter().items()):
            pb_delete, l_key, settingcard = self.addItem(key)

            self.gl_elements.addWidget(pb_delete, i, 0)
            self.gl_elements.addWidget(l_key, i, 1)
            self.gl_elements.addWidget(settingcard, i, 2)
        return super().refresh()

    def addItem(self, key):
        def setter(key, val):
            self.getter()[key] = val

        def attrsetter(attrs, attr, val):
            attrs[attr] = val

        attrs = {}
        _type = self.attrgetter("element_type").get(key)
        if _type != None:
            attrs["type"] = _type

        settingcard = SettingCard(
            lambda key=key: self.getter()[key],
            lambda attr, default=None, attrs=attrs: attrs.get(attr, default),
            lambda val, key=key: setter(key, val),
            lambda attr, val, attrs=attrs: attrsetter(attrs, attr, val),
        )

        l_key = QLabel()
        l_key.setText(str(key))

        pb_delete = TransparentToolButton()
        pb_delete.setIcon(qta.icon("mdi.delete"))
        pb_delete.clicked.connect(lambda _, card=settingcard: self.delete(card))

        self.button_label_card.append((pb_delete, l_key, settingcard))

        return pb_delete, l_key, settingcard

    def value(self):
        return {i[1].text(): i[2].value() for i in self.button_label_card}

    def delete(self, settingcard):
        for i, (_, _, card) in enumerate(self.button_label_card):
            if card == settingcard:
                break
        else:
            return

        self.button_label_card.pop(i)

        self.on_valueChanged()
        self.refresh()

    @pyqtSlot(bool)
    def on_pb_add_clicked(self, _):
        key, ok = QInputDialog.getText(self, self.tr("添加"), self.tr("输入键"))
        if not ok:
            return
        _type_key, ok = QInputDialog.getItem(
            self,
            self.tr("添加"),
            self.tr("请选择类型"),
            SettingCard.TYPE_MAP.keys(),
            editable=False,
        )
        if not ok:
            return

        _type = SettingCard.TYPE_MAP[_type_key]

        self.getter()[key] = _type()
        element_type = self.attrgetter("element_type")
        element_type[key] = _type_key
        self.attrsetter("element_type", element_type)
        self.addItem(key)

        self.on_valueChanged()
        self.refresh()
