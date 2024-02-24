import webbrowser

from PyQt5.QtCore import pyqtSignal, QSize, QCoreApplication
from PyQt5.QtWidgets import qApp, QTreeWidgetItem
from qfluentwidgets import PushButton, StateToolTip

from Core import ModrinthProjectModel, ModrinthVersionModel, ModrinthAPI, Task

from .ResDetail import ResDetail
from .ModrinthVersionItem import ModrinthVersionItem

_translate = QCoreApplication.translate


class GetVersionTask(Task):
    versionGot = pyqtSignal(list)
    instance = None

    def __new__(cls, *args, **kwargs):
        if GetVersionTask.instance != None:
            GetVersionTask.instance.terminate()
        GetVersionTask.instance = super().__new__(cls)
        return GetVersionTask.instance

    def __init__(self, res) -> None:
        super().__init__(
            _translate("GetVersionTask", "获取版本") + ": " + res["title"],
            taskfunc=self.taskfunc,
        )  # 还没初始化, 无法使用self.tr
        self.res = res

    def taskfunc(self, callback):
        self.versionGot.emit(ModrinthAPI().get_project_versions(self.res["id"]))


class GetDependenciesTask(Task):
    dependenciesGot = pyqtSignal(ModrinthVersionItem, QTreeWidgetItem, list)
    instances = {}

    def __new__(cls, res, widget: ModrinthVersionItem, *args):
        _hash = str(res) + str(widget.version)
        if _hash in GetDependenciesTask.instances:
            GetDependenciesTask.instances[_hash].terminate()
        GetDependenciesTask.instances[_hash] = super().__new__(cls)
        return GetDependenciesTask.instances[_hash]

    def __init__(self, res, widget: ModrinthVersionItem, item: QTreeWidgetItem) -> None:
        super().__init__(
            _translate("GetDependenciesTask", "获取依赖")
            + ": "
            + res["title"]
            + " "
            + widget.version["name"],
            taskfunc=self.taskfunc,
        )  # 还没初始化, 无法使用self.tr
        self.res = res
        self.widget = widget
        self.item = item
        self.api = ModrinthAPI()

    def taskfunc(self, callback):
        version = self.widget.version
        projects = []

        n = len(version["dependencies"])
        callback.get("setMax", lambda _: _)(n)
        for i, dependency in enumerate(version["dependencies"]):
            if dependency["project_id"] == None:
                continue
            projects.append(self.api.get_project(dependency["project_id"]))
            callback.get("setProgress", lambda _: _)(i + 1)
        self.dependenciesGot.emit(self.widget, self.item, projects)


class ModrinthResDetail(ResDetail):
    def __init__(self, res: ModrinthProjectModel) -> None:
        if ResDetail.new_count[str(res)] > 1:
            return
        super().__init__(res)
        self.setWindowTitle(self.tr("资源详情") + f': {res["title"]}')
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

        self.refresh()

    def refresh(self):
        getversion_task = GetVersionTask(self.res)
        getversion_task.versionGot.connect(self.setVersions)
        getversion_task.start()
        return super().refresh()

    def setVersions(self, versions: list[ModrinthVersionModel]):
        statetooltip = StateToolTip(self.tr("正在加载版本"), "", self)
        statetooltip.move(statetooltip.getSuitablePos())
        statetooltip.show()

        self.tw_versions.clear()
        # 加载版本之后VersionItem都变了
        # 而之前GetDependenciesTask里保存的VersionItem还没变
        # 为了防止出错要全部终止
        for _, task in GetDependenciesTask.instances.items():
            task.terminate()
        GetDependenciesTask.instances = {}

        n = len(versions)
        for i, version in enumerate(versions):
            item = QTreeWidgetItem()
            widget = ModrinthVersionItem(version, self.res)
            widget.showDependenciesRequest.connect(self.showDependencies)
            item.setSizeHint(0, widget.size())
            self.tw_versions.addTopLevelItem(item)
            self.tw_versions.setItemWidget(item, 0, widget)

            statetooltip.setContent(f"{i+1}/{n}({round((i+1)/n*100,1)}%)")
            qApp.processEvents()

        statetooltip.setContent(self.tr("加载完成"))
        statetooltip.setState(True)

    def showDependencies(self, widget: ModrinthVersionItem):
        for i in range(self.tw_versions.topLevelItemCount()):
            item = self.tw_versions.topLevelItem(i)
            if self.tw_versions.itemWidget(item, 0) == widget:
                break
        else:
            return
        if item.childCount() != 0:  # 说明已经加载过了
            return
        getdependencies_task = GetDependenciesTask(self.res, widget, item)
        getdependencies_task.dependenciesGot.connect(self.setDependencies)
        getdependencies_task.start()

    def setDependencies(
        self,
        widget: ModrinthVersionItem,
        item: QTreeWidgetItem,
        projects: list[ModrinthProjectModel],
    ):
        from .ModrinthResItem import ModrinthResItem

        statetooltip_dep = StateToolTip(
            self.tr("正在加载{name}的依赖").format(name=widget.version["name"]),
            "",
            self,
        )
        statetooltip_dep.move(statetooltip_dep.getSuitablePos())
        statetooltip_dep.show()

        n = len(projects)
        for i, project in enumerate(projects):
            dep_item = QTreeWidgetItem()
            dep_widget = ModrinthResItem(project)
            dep_item.setSizeHint(0, QSize(dep_widget.width(), dep_widget.height() + 10))
            item.addChild(dep_item)
            self.tw_versions.setItemWidget(dep_item, 0, dep_widget)
            statetooltip_dep.setContent(f"{i+1}/{n}({round((i+1)/n*100,1)}%)")
            qApp.processEvents()

        statetooltip_dep.setContent(self.tr("加载完成"))
        statetooltip_dep.setState(True)
