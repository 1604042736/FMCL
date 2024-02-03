import logging
import traceback
import webbrowser
import multitasking

from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtWidgets import qApp, QTreeWidgetItem
from qfluentwidgets import PushButton, StateToolTip

from Core import ModrinthProjectModel, ModrinthVersionModel, ModrinthAPI

from .ResDetail import ResDetail
from .ModrinthVersionItem import ModrinthVersionItem


class ModrinthResDetail(ResDetail):
    __versionsGot = pyqtSignal(list)
    __dependenciesGot = pyqtSignal(QTreeWidgetItem, list)

    def __init__(self, res: ModrinthProjectModel) -> None:
        if ResDetail.new_count[str(res)] > 1:
            return
        super().__init__(res)
        self.setWindowTitle(f'{self.tr("资源详情")}: {res["title"]}')
        self.api = ModrinthAPI()

        from .ModrinthResItem import ModrinthResItem

        self.vl_resinfo.addWidget(ModrinthResItem(res))

        button = PushButton()
        button.setText(self.tr("复制名称"))
        button.clicked.connect(lambda: qApp.clipboard().setText(res["title"]))
        self.hl_operates.addWidget(button)

        button = PushButton()
        button.setText(self.tr("转到Modrinth"))
        button.clicked.connect(
            lambda: webbrowser.open(
                "https://modrinth.com/" + res["project_type"] + "/" + res["slug"]
            )
        )
        self.hl_operates.addWidget(button)

        for key, name in (
            ("issues_url", self.tr("反馈")),
            ("source_url", self.tr("源码")),
            ("wiki_url", self.tr("Wiki")),
            ("discord_url", self.tr("Discord")),
        ):
            if key not in res:
                continue
            button = PushButton()
            button.setText(name)
            button.clicked.connect(lambda _, key=key: webbrowser.open(res[key]))
            self.hl_operates.addWidget(button)

        self.statetooltip = None
        self.__versionsGot.connect(self.setVersions)

        self.statetooltip_dep = None
        self.__dependenciesGot.connect(self.setDependencies)

        self.refresh()

    def refresh(self):
        if self.statetooltip != None:
            self.statetooltip.close()
            self.statetooltip.setState(True)
        self.statetooltip = StateToolTip(self.tr("正在获取版本"), "", self)
        self.statetooltip.move(self.statetooltip.getSuitablePos())
        self.statetooltip.show()

        self.tw_versions.clear()
        self.__getVersions()
        return super().refresh()

    @multitasking.task
    def __getVersions(self):
        self.__versionsGot.emit(self.api.get_project_versions(self.res["id"]))

    def setVersions(self, versions: list[ModrinthVersionModel]):
        n = len(versions)
        for i, version in enumerate(versions):
            item = QTreeWidgetItem()
            widget = ModrinthVersionItem(version, self.res)
            widget.showDependenciesRequest.connect(self.showDependencies)
            item.setSizeHint(0, widget.size())
            self.tw_versions.addTopLevelItem(item)
            self.tw_versions.setItemWidget(item, 0, widget)

            self.statetooltip.setContent(f"{i+1}/{n}({round((i+1)/n*100,1)}%)")
            qApp.processEvents()

        self.statetooltip.setContent(self.tr("获取完成"))
        self.statetooltip.setState(True)
        self.statetooltip = None

    def showDependencies(self, widget: ModrinthVersionItem):
        for i in range(self.tw_versions.topLevelItemCount()):
            item = self.tw_versions.topLevelItem(i)
            if self.tw_versions.itemWidget(item, 0) == widget:
                break
        else:
            return
        if item.childCount() != 0:  # 说明已经加载过了
            return
        version = widget.version
        self.statetooltip_dep = StateToolTip(
            self.tr("正在加载{name}的依赖").format(name=version["name"]), "", self
        )
        self.statetooltip_dep.move(self.statetooltip_dep.getSuitablePos())
        self.statetooltip_dep.show()

        self.getDependencies(widget, item)

    @multitasking.task
    def getDependencies(self, widget: ModrinthVersionItem, item: QTreeWidgetItem):
        version = widget.version
        projects = []
        for i, dependency in enumerate(version["dependencies"]):
            if dependency["project_id"] == None:
                continue
            projects.append(self.api.get_project(dependency["project_id"]))
        try:
            self.__dependenciesGot.emit(item, projects)
        except:
            logging.error(traceback.format_exc())
            self.statetooltip_dep.setContent(self.tr("加载失败, 请尝试重新加载"))
            self.statetooltip_dep.setState(True)  # 实际上并不会消失
            self.statetooltip_dep = None

    def setDependencies(
        self,
        item: QTreeWidgetItem,
        projects: list[ModrinthProjectModel],
    ):
        from .ModrinthResItem import ModrinthResItem

        n = len(projects)
        for i, project in enumerate(projects):
            dep_item = QTreeWidgetItem()
            dep_widget = ModrinthResItem(project)
            dep_item.setSizeHint(0, QSize(dep_widget.width(), dep_widget.height() + 10))
            item.addChild(dep_item)
            self.tw_versions.setItemWidget(dep_item, 0, dep_widget)
            self.statetooltip_dep.setContent(f"{i+1}/{n}({round((i+1)/n*100,1)}%)")
            qApp.processEvents()

        self.statetooltip_dep.setContent(self.tr("加载完成"))
        self.statetooltip_dep.setState(True)
        self.statetooltip_dep = None
