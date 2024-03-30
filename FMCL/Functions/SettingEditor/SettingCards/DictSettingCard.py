import qtawesome as qta

from PyQt5.QtCore import pyqtSlot, QEvent
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QLabel, QInputDialog, QSpacerItem, QSizePolicy
from qfluentwidgets import TransparentToolButton

from .SettingCard import SettingCard

from .ui_DictSettingCard import Ui_DictSettingCard


class DictSettingCard(SettingCard, Ui_DictSettingCard):
    def __init__(self, getter, attrgetter, setter, attrsetter) -> None:
        super().__init__(getter, attrgetter, setter, attrsetter)
        self.setupUi(self)
        self.pb_add.setIcon(qta.icon("msc.add"))

        if self.attrgetter("element_attrs") == None:
            self.attrsetter("element_attrs", dict())  # 保存元素的属性

        self.button_label_card_attrs = []

        self.gl_elements.setColumnStretch(2, 3)

        self.refresh()

    def refresh(self):
        element_attrs = self.attrgetter("element_attrs")
        for i, (_, l_key, _, attrs) in enumerate(self.button_label_card_attrs):
            element_attrs[l_key.text()] = attrs

        while self.gl_elements.count():
            item = self.gl_elements.takeAt(0)
            if item.widget() != None:
                item.widget().deleteLater()

        self.button_label_card_attrs = []

        for i, (key, val) in enumerate(self.getter().items()):
            pb_delete, l_key, settingcard = self.addItem(key)

            self.gl_elements.addWidget(pb_delete, i * 2, 0)
            self.gl_elements.addWidget(l_key, i * 2, 1)
            self.gl_elements.addItem(
                QSpacerItem(
                    0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
                ),
                i * 2 + 1,
                0,
                1,
                2,
            )
            self.gl_elements.addWidget(settingcard, i * 2, 2, 2, 1)
        return super().refresh()

    def addItem(self, key):
        def setter(key, val):
            self.getter()[key] = val

        def attrsetter(attrs, attr, val):
            attrs[attr] = val

        element_attrs = self.attrgetter("element_attrs")
        if key not in element_attrs:
            element_attrs[key] = {}
        attrs = element_attrs[key]
        _type = self.attrgetter("type")
        if _type != None:
            attrs["type"] = _type  # 优先使用已指定的类型

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

        self.button_label_card_attrs.append((pb_delete, l_key, settingcard, attrs))

        return pb_delete, l_key, settingcard

    def value(self):
        return {i[1].text(): i[2].value() for i in self.button_label_card_attrs}

    def delete(self, settingcard):
        for i, (_, _, card, _) in enumerate(self.button_label_card_attrs):
            if card == settingcard:
                break
        else:
            return

        self.button_label_card_attrs.pop(i)

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

        element_attrs = self.attrgetter("element_attrs")
        if key not in element_attrs:
            element_attrs[key] = {}
        element_attrs[key]["type"] = _type_key

        self.getter()[key] = _type()

        self.addItem(key)

        self.on_valueChanged()
        self.refresh()

    def event(self, a0: QEvent | None) -> bool:
        if a0.type() == QEvent.Type.Paint:
            painter = QPainter(self)
            painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        return super().event(a0)
