from .SettingCard import SettingCard

from .ui_BoolSettingCard import Ui_BoolSettingCard


class BoolSettingCard(SettingCard, Ui_BoolSettingCard):
    def __init__(self, getter, attrgetter, setter,attrsetter) -> None:
        super().__init__(getter, attrgetter, setter,attrsetter)
        self.setupUi(self)

        self.cb_val.setCheckState((0, 2)[self.getter()])
        self.cb_val.stateChanged.connect(self.on_valueChanged)

    def refresh(self):
        self.cb_val.stateChanged.disconnect(self.on_valueChanged)
        self.cb_val.setCheckState((0, 2)[self.getter()])
        self.cb_val.stateChanged.connect(self.on_valueChanged)
        return super().refresh()

    def value(self):
        return (False, True, True)[self.cb_val.checkState()]
