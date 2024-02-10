import multitasking

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from Setting import Setting
from Core import ModrinthProjectModel, Download, ModrinthAPI

from .ResItem import ResItem
from .ModrinthResDetail import ModrinthResDetail


class ModrinthResItem(ResItem):
    def __init__(self, res: ModrinthProjectModel) -> None:
        super().__init__(res)
        self.setIcon()

        self.hl_categories.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.hl_otherinfo.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.l_title.setText(res["title"])
        self.l_description.setText(res["description"])
        self.l_description.setToolTip(res["description"])

        api = ModrinthAPI()
        translations = api.get_translations()
        for i in res["categories"]:
            label = QLabel()
            label.setText(translations.get(i, i))
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
        label.setText(self.tr("加载器") + f': {",".join(res["loaders"])}')
        self.hl_otherinfo.addWidget(label)
        label = QLabel()
        label.setText(self.tr("下载量") + f': {res["downloads"]}')
        self.hl_otherinfo.addWidget(label)
        label = QLabel()
        label.setText(self.tr("更新日期") + f': {api.get_time(res["updated"])}')
        self.hl_otherinfo.addWidget(label)
        label = QLabel()
        label.setText(self.tr("来自") + ": Modrinth")
        self.hl_otherinfo.addWidget(label)

    @multitasking.task
    def setIcon(self):
        url = self.res["icon_url"]
        if url == None:
            return
        path = self.res["icon_url"].replace("https:/", Setting()["system.temp_dir"])
        Download(url, path).check()
        self.l_icon.setPixmap(QPixmap(path).scaled(64, 64))

    def event(self, a0: QEvent | None) -> bool:
        if a0.type() == QEvent.Type.MouseButtonRelease:
            ModrinthResDetail(self.res).show()
        return super().event(a0)
