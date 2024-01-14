import multitasking

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from Core import ApiModInfo, Mod, Network

from .ModDetail import ModDetail
from .ui_ApiModItem import Ui_ApiModItem


class ApiModItem(QWidget, Ui_ApiModItem):
    def __init__(self, apimodinfo: ApiModInfo) -> None:
        super().__init__()
        self.setupUi(self)
        self.apimodinfo = apimodinfo
        self.setIcon()
        self.hl_categories.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.hl_otherinfo.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.l_title.setText(apimodinfo["title"])
        self.l_description.setText(apimodinfo["description"])
        self.l_description.setToolTip(apimodinfo["description"])

        mod = Mod()
        for i in apimodinfo["categories"]:
            label = QLabel()
            label.setText(mod.tr_categories.get(i, i))
            label.setStyleSheet(
                """
QLabel{
    background-color:rbg(200,200,200);
    border:1px solid black;
}
"""
            )
            self.hl_categories.addWidget(label)

        label = QLabel()
        label.setText(f'{self.tr("加载器")}: {",".join(apimodinfo["loaders"])}')
        self.hl_otherinfo.addWidget(label)
        label = QLabel()
        label.setText(f'{self.tr("下载量")}: {apimodinfo["downloads"]}')
        self.hl_otherinfo.addWidget(label)
        label = QLabel()
        label.setText(f'{self.tr("更新日期")}: {Mod.get_time(apimodinfo["updated"])}')
        self.hl_otherinfo.addWidget(label)
        label = QLabel()
        label.setText(f'{self.tr("来自")}: {apimodinfo["api_name"]}')
        self.hl_otherinfo.addWidget(label)

    @multitasking.task
    def setIcon(self):
        r = Network().get(self.apimodinfo["icon_url"])
        image = QImage.fromData(r.content)
        pixmap = QPixmap.fromImage(image)
        self.l_icon.setPixmap(pixmap.scaled(64, 64))

    def event(self, a0: QEvent | None) -> bool:
        if a0.type() == QEvent.Type.MouseButtonRelease:
            ModDetail(self.apimodinfo).show()
        return super().event(a0)
