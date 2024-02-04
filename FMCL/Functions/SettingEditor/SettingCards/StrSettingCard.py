from .SettingCard import SettingCard

from .ui_StrSettingCard import Ui_StrSettingCard


class StrSettingCard(SettingCard, Ui_StrSettingCard):
    def __init__(self, getter, attrgetter, setter, attrsetter) -> None:
        super().__init__(getter, attrgetter, setter, attrsetter)
        self.setupUi(self)
        self.le_val.setText(self.getter())
        self.le_val.editingFinished.connect(self.on_valueChanged)

        self.setToolTip(self.tr("输入完后按回车键以保存"))

    def refresh(self):
        self.le_val.editingFinished.disconnect(self.on_valueChanged)
        self.le_val.setText(self.getter())
        self.le_val.editingFinished.connect(self.on_valueChanged)
        return super().refresh()

    def value(self):
        return self.le_val.text()
