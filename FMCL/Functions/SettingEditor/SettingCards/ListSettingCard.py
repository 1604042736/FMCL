import qtawesome as qta

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QInputDialog, QSpacerItem, QSizePolicy
from qfluentwidgets import MessageBox

from .SettingCard import SettingCard

from .ui_ListSettingCard import Ui_ListSettingCard
from .ui_ListSettingCardOperator import Ui_ListSettingCardOperator


class ListSettingCardOperator(QWidget, Ui_ListSettingCardOperator):
    addRequest = pyqtSignal(SettingCard)
    moveUpRequest = pyqtSignal(SettingCard)
    moveDownRequest = pyqtSignal(SettingCard)
    moveTopRequest = pyqtSignal(SettingCard)
    deleteRequest = pyqtSignal(SettingCard)

    def __init__(self, settingcard: SettingCard) -> None:
        super().__init__()
        self.setupUi(self)
        self.settingcard = settingcard

        self.pb_add.setIcon(qta.icon("msc.add"))
        self.pb_delete.setIcon(qta.icon("mdi.delete"))
        self.pb_movedown.setIcon(qta.icon("fa5s.arrow-down"))
        self.pb_moveup.setIcon(qta.icon("fa5s.arrow-up"))
        self.pb_movetop.setIcon(qta.icon("mdi.arrow-collapse-up"))

    @pyqtSlot(bool)
    def on_pb_add_clicked(self, _):
        self.addRequest.emit(self.settingcard)

    @pyqtSlot(bool)
    def on_pb_moveup_clicked(self, _):
        self.moveUpRequest.emit(self.settingcard)

    @pyqtSlot(bool)
    def on_pb_movedown_clicked(self, _):
        self.moveDownRequest.emit(self.settingcard)

    @pyqtSlot(bool)
    def on_pb_movetop_clicked(self, _):
        self.moveTopRequest.emit(self.settingcard)

    @pyqtSlot(bool)
    def on_pb_delete_clicked(self, _):
        self.deleteRequest.emit(self.settingcard)


class ListSettingCard(SettingCard, Ui_ListSettingCard):
    def __init__(self, getter, attrgetter, setter, attrsetter) -> None:
        super().__init__(getter, attrgetter, setter, attrsetter)
        self.setupUi(self)
        self.pb_add.setIcon(qta.icon("msc.add"))

        self.gl_elements.setAlignment(Qt.AlignmentFlag.AlignTop)

        if self.attrgetter("element_attrs") == None:
            self.attrsetter("element_attrs", dict())  # 保存元素的属性

        self.card_operator_attrs = []

        self.refresh()

    def refresh(self):
        element_attrs = self.attrgetter("element_attrs")
        for i, (_, _, attrs) in enumerate(self.card_operator_attrs):
            element_attrs[i] = attrs

        while self.gl_elements.count():
            item = self.gl_elements.takeAt(0)
            if item.widget() != None:
                item.widget().deleteLater()

        self.card_operator_attrs = []

        for i, val in enumerate(self.getter()):

            def setter(i, val):
                self.getter()[i] = val

            if i not in element_attrs:
                element_attrs[i] = {}
            attrs = element_attrs[i]
            _type = self.attrgetter("type")
            if _type != None:
                attrs["type"] = _type  # 优先使用已指定的类型

            def attrsetter(attrs, attr, val):
                attrs[attr] = val

            settingcard = SettingCard(
                lambda i=i: self.getter()[i],
                lambda attr, default=None, attrs=attrs: attrs.get(attr, default),
                lambda val, i=i: setter(i, val),
                lambda attr, val, attrs=attrs: attrsetter(attrs, attr, val),
            )
            settingcard.valueChanged.connect(lambda _: self.on_valueChanged())

            w_operator = ListSettingCardOperator(settingcard)
            w_operator.addRequest.connect(self.addAfter)
            w_operator.moveUpRequest.connect(self.moveUp)
            w_operator.moveDownRequest.connect(self.moveDown)
            w_operator.moveTopRequest.connect(self.moveTop)
            w_operator.deleteRequest.connect(self.delete)

            if self.attrgetter("static", False) == True:
                settingcard.setEnabled(False)
                w_operator.pb_add.setEnabled(False)
                w_operator.pb_delete.setEnabled(False)

            # 一个元素在布局里占2行
            self.gl_elements.addWidget(w_operator, i * 2, 0)
            self.gl_elements.addItem(
                QSpacerItem(
                    0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
                ),
                i * 2 + 1,
                0,
            )
            self.gl_elements.addWidget(settingcard, i * 2, 1, 2, 1)
            self.card_operator_attrs.append((settingcard, w_operator, attrs))
        return super().refresh()

    def value(self):
        return [settingcard.value() for settingcard, _, _ in self.card_operator_attrs]

    def moveDown(self, settingcard):
        for i, (card, _, _) in enumerate(self.card_operator_attrs):
            if card == settingcard and i < len(self.card_operator_attrs) - 1:
                break
        else:
            return  # 下移的是列表的最后一个元素

        self.card_operator_attrs[i], self.card_operator_attrs[i + 1] = (
            self.card_operator_attrs[i + 1],
            self.card_operator_attrs[i],
        )
        self.on_valueChanged()
        self.sync()
        self.refresh()

    def moveUp(self, settingcard):
        for i, (card, _, _) in enumerate(self.card_operator_attrs):
            if card == settingcard and i > 0:
                break
        else:
            return

        self.card_operator_attrs[i], self.card_operator_attrs[i - 1] = (
            self.card_operator_attrs[i - 1],
            self.card_operator_attrs[i],
        )

        self.on_valueChanged()
        self.refresh()

    def moveTop(self, settingcard):
        for i, (card, _, _) in enumerate(self.card_operator_attrs):
            if card == settingcard and i > 0:
                break
        else:
            return

        t = self.card_operator_attrs.pop(i)
        self.card_operator_attrs.insert(0, t)

        self.on_valueChanged()
        self.refresh()

    def delete(self, settingcard):
        atleast = self.attrgetter("atleast", 0)
        if len(self.card_operator_attrs) <= atleast:
            MessageBox(
                self.tr("无法删除"),
                self.tr("至少要有{atleast}个元素").format(atleast=atleast),
                self.window(),
            ).exec()
            return
        for i, (card, _, _) in enumerate(self.card_operator_attrs):
            if card == settingcard:
                break
        else:
            return

        self.card_operator_attrs.pop(i)

        self.on_valueChanged()  # 注意两个语句的先后顺序
        self.refresh()

    def addAfter(self, settingcard):
        for i, (card, _, _) in enumerate(self.card_operator_attrs):
            if card == settingcard:
                break
        else:
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
        element_attrs[i + 1]["type"] = _type_key
        self.getter().insert(i + 1, _type())

        self.on_valueChanged()
        self.refresh()

    @pyqtSlot(bool)
    def on_pb_add_clicked(self, _):
        _type_key = ""
        if self.attrgetter("type") != None:
            _type = SettingCard.TYPE_MAP[self.attrgetter("type")]
        else:
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
        if _type_key:
            if len(self.getter()) not in element_attrs:
                element_attrs[len(self.getter()) ] = {}
            element_attrs[len(self.getter())]["type"] = _type_key

        self.getter().append(_type())

        self.refresh()
