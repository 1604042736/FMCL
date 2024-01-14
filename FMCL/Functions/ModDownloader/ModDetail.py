import webbrowser
import qtawesome as qta
from Events import *

from PyQt5.QtCore import pyqtSlot, QEvent, QSize
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, qApp, QFileDialog
from qfluentwidgets import PushButton, TransparentToolButton

from Core import ApiModInfo, Download, Mod, Task

from .ui_ModDetail import Ui_ModDetail


class ModDetail(QWidget, Ui_ModDetail):
    instances = {}
    new_count = {}

    def __new__(cls, apimodinfo: ApiModInfo):
        if apimodinfo["id"] not in ModDetail.instances:
            ModDetail.instances[apimodinfo["id"]] = super().__new__(cls)
            ModDetail.new_count[apimodinfo["id"]] = 0
        ModDetail.new_count[apimodinfo["id"]] += 1
        return ModDetail.instances[apimodinfo["id"]]

    def __init__(self, apimodinfo: ApiModInfo):
        if ModDetail.new_count[apimodinfo["id"]] > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.puzzle-outline"))
        self.setWindowTitle(f'{self.tr("模组详情")}: {apimodinfo["title"]}')
        self.apimodinfo = apimodinfo

        from .ApiModItem import ApiModItem

        self.modinfo = ApiModItem(apimodinfo)
        self.vl_modinfo.addWidget(self.modinfo)

        for key, name in (
            ("issues_url", self.tr("反馈")),
            ("source_url", self.tr("源码")),
            ("wiki_url", self.tr("Wiki")),
        ):
            if key not in apimodinfo:
                continue
            button = PushButton()
            button.setText(name)
            button.clicked.connect(lambda _, key=key: webbrowser.open(apimodinfo[key]))
            self.hl_urls.addWidget(button)

        self.pb_refresh = TransparentToolButton()
        self.pb_refresh.resize(46, 32)
        self.pb_refresh.setIcon(qta.icon("mdi.refresh"))
        self.pb_refresh.clicked.connect(lambda: self.refresh())

        self.refresh()

    def refresh(self):
        self.game_versions_item = {}
        self.game_versions_dep = {}  # 依赖模组
        self.game_versions_depitem = {}
        self.item_file = []
        self.tw_versions.clear()

        mod = Mod()
        for version in mod.get_mod_versions(self.apimodinfo):
            for game_version in version["game_versions"]:
                item = QTreeWidgetItem()
                item.setText(0, version["name"])
                item.setText(1, ",".join(version["loaders"]))
                item.setText(
                    2,
                    mod.tr_versiontype.get(
                        version["version_type"], version["version_type"]
                    ),
                )
                item.setText(3, str(version["downloads"]))
                item.setText(4, mod.get_time(version["date_published"]))

                for file in version["files"]:
                    file_item = QTreeWidgetItem()
                    file_item.setText(0, file["filename"])
                    item.addChild(file_item)
                    self.item_file.append((file_item, file))

                if game_version not in self.game_versions_item:  # 游戏版本树
                    root = QTreeWidgetItem()
                    root.setText(0, game_version)
                    self.tw_versions.addTopLevelItem(root)
                    self.game_versions_item[game_version] = root

                if game_version not in self.game_versions_dep:
                    self.game_versions_dep[game_version] = []

                for dep in version["dependencies"]:
                    if dep["project_id"] in self.game_versions_dep[game_version]:
                        continue
                    if game_version not in self.game_versions_depitem:  # 前置模组子树
                        root_dep = QTreeWidgetItem()
                        root_dep.setText(0, self.tr("前置模组"))
                        root.addChild(root_dep)
                        self.game_versions_depitem[game_version] = root_dep
                    from .ApiModItem import ApiModItem

                    self.game_versions_dep[game_version].append(dep["project_id"])
                    apimodinfo = mod.get_apimodinfo(self.apimodinfo, dep["project_id"])
                    dep_item = QTreeWidgetItem()
                    dep_item.setText(
                        1,
                        mod.tr_dependencytype.get(
                            dep["dependency_type"], dep["dependency_type"]
                        ),
                    )
                    widget = ApiModItem(apimodinfo)
                    for i in range(self.tw_versions.columnCount()):
                        dep_item.setSizeHint(
                            i, QSize(widget.width(), widget.height() + 10)
                        )
                    root_dep.addChild(dep_item)
                    self.tw_versions.setItemWidget(dep_item, 0, widget)

                root.addChild(item)

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_refresh, "right"))
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_refresh))
            self.pb_refresh.setParent(self)
        return super().event(a0)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_tw_versions_itemClicked(self, item, _):
        for item_, file in self.item_file:
            if item == item_:
                break
        else:
            return
        url = file["url"]
        filename = file["filename"]
        path = QFileDialog.getSaveFileName(self, self.tr("下载"), f"./{filename}")[0]
        if path:
            Task(
                self.tr("下载") + filename,
                taskfunc=lambda callback: Download(url, path, callback).start(),
            ).start()
