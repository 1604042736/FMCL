import qtawesome as qta

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QInputDialog, QSpacerItem
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

        self.refresh()

    def refresh(self):
        while self.gl_elements.count():
            item = self.gl_elements.takeAt(0)
            if item.widget() != None:
                item.widget().deleteLater()

        self.settingcard_operator = []

        for i, val in enumerate(self.getter()):

            def setter(i, val):
                self.getter()[i] = val

            attrs = {}
            _type = self.attrgetter("type")
            if _type != None:
                attrs["type"] = _type

            def attrsetter(attrs, attr, val):
                attrs[attr] = val

            settingcard = SettingCard(
                lambda i=i: self.getter()[i],
                # 列表中元素类型相同
                lambda attr, default=None, attrs=attrs: attrs.get(attr, default),
                lambda val, i=i: setter(i, val),
                lambda attr, val, attrs=attrs: attrsetter(attrs, attr, val),
            )
            settingcard.valueChanged.connect(lambda _: self.sync())

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

            self.gl_elements.addWidget(w_operator, i, 0)
            self.gl_elements.addWidget(settingcard, i, 1)
            self.settingcard_operator.append((settingcard, w_operator))
        self.gl_elements.addItem(QSpacerItem(0, 0), i, 0)
        return super().refresh()

    def value(self):
        return [settingcard.value() for settingcard, _ in self.settingcard_operator]

    def moveDown(self, settingcard):
        for i, (card, _) in enumerate(self.settingcard_operator):
            if card == settingcard and i < len(self.settingcard_operator) - 1:
                break
        else:
            return  # 下移的是列表的最后一个元素

        self.settingcard_operator[i], self.settingcard_operator[i + 1] = (
            self.settingcard_operator[i + 1],
            self.settingcard_operator[i],
        )

        self.on_valueChanged()
        self.sync()
        self.refresh()

    def moveUp(self, settingcard):
        for i, (card, _) in enumerate(self.settingcard_operator):
            if card == settingcard and i > 0:
                break
        else:
            return

        self.settingcard_operator[i], self.settingcard_operator[i - 1] = (
            self.settingcard_operator[i - 1],
            self.settingcard_operator[i],
        )

        self.on_valueChanged()
        self.refresh()

    def moveTop(self, settingcard):
        for i, (card, _) in enumerate(self.settingcard_operator):
            if card == settingcard and i > 0:
                break
        else:
            return

        self.settingcard_operator[i], self.settingcard_operator[0] = (
            self.settingcard_operator[0],
            self.settingcard_operator[i],
        )

        self.on_valueChanged()
        self.refresh()

    def delete(self, settingcard):
        atleast = self.attrgetter("atleast", 0)
        if len(self.settingcard_operator) <= atleast:
            MessageBox(
                self.tr("无法删除"),
                self.tr("至少要有{atleast}个元素").format(atleast=atleast),
                self.window(),
            ).exec()
            return
        for i, (card, _) in enumerate(self.settingcard_operator):
            if card == settingcard:
                break
        else:
            return

        self.settingcard_operator.pop(i)

        self.on_valueChanged()  # 注意两个语句的先后顺序
        self.refresh()

    def addAfter(self, settingcard):
        for i, (card, _) in enumerate(self.settingcard_operator):
            if card == settingcard:
                break
        else:
            return

        self.getter().insert(i + 1, settingcard.type()())

        self.on_valueChanged()
        self.refresh()

    @pyqtSlot(bool)
    def on_pb_add_clicked(self, _):
        _type_key = ""
        if len(self.settingcard_operator) > 0:
            _type = self.settingcard_operator[0][0].type()
        elif self.attrgetter("type") != None:
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

        self.getter().append(_type())

        if _type_key:
            # 在列表为空的情况下选一个类型最为列表元素的类型
            self.attrsetter("type", _type_key)

        self.refresh()
