import qtawesome as qta

from PyQt5.QtCore import QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, qApp, QListWidgetItem
from qfluentwidgets import TransparentTogglePushButton, StateToolTip

from Core import ModrinthAPI, Task

from .ModrinthResItem import ModrinthResItem
from .ui_ResourceDownloader import Ui_ResourceDownloader


class ResourceDownloader(QWidget, Ui_ResourceDownloader):
    searchFinsihed = pyqtSignal(list)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.earth"))
        self.splitter.setSizes([100, 500])

        self.modrinthapi = ModrinthAPI()
        self.search_task: Task = None
        self.statetooltip = None

        self.searchFinsihed.connect(self.setResults)

        self.refresh()

    def refresh(self):
        translations = self.modrinthapi.get_translations()

        for i in self.modrinthapi.get_types()[::-1]:
            button = TransparentTogglePushButton()
            button.setObjectName(f"pb_type_{i}")
            button.setText(translations[i])
            button.setCheckable(True)
            button.setAutoExclusive(True)
            self.hl_types.insertWidget(0, button)
        button.setChecked(True)  # 第一个按钮

        for i in self.modrinthapi.get_sortby()[::-1]:
            button = TransparentTogglePushButton()
            button.setObjectName(f"pb_sortby_{i}")
            button.setText(translations[i])
            button.setCheckable(True)
            button.setAutoExclusive(True)
            self.hl_sortby.insertWidget(0, button)
        button.setChecked(True)  # 第一个按钮

        for i in self.modrinthapi.get_categories()[::-1]:
            button = TransparentTogglePushButton()
            button.setObjectName(f"pb_categories_{i}")
            button.setText(translations[i])
            button.setCheckable(True)
            self.hl_categories.insertWidget(0, button)

    @pyqtSlot(bool)
    def on_pb_search_clicked(self, _):
        if self.search_task != None:
            self.search_task.terminate()
        # 注意先后顺序
        if self.statetooltip != None:
            self.statetooltip.close()
            self.statetooltip.setState(True)
        self.statetooltip = StateToolTip(self.tr("正在搜索"), "", self)
        self.statetooltip.move(self.statetooltip.getSuitablePos())
        self.statetooltip.show()

        sources = []
        for i in range(self.hl_source.count()):
            item = self.hl_source.itemAt(i)
            if item.widget() == None:
                continue
            name = item.widget().objectName()
            if name.startswith("pb_source_") and item.widget().isChecked():
                sources.append(name.split("_", maxsplit=2)[-1])

        sortby = ""
        for i in range(self.hl_sortby.count()):
            item = self.hl_sortby.itemAt(i)
            if item.widget() == None:
                continue
            name = item.widget().objectName()
            if name.startswith("pb_sortby_") and item.widget().isChecked():
                sortby = name.split("_", maxsplit=2)[-1]

        categories = []
        for i in range(self.hl_categories.count()):
            item = self.hl_categories.itemAt(i)
            if item.widget() == None:
                continue
            name = item.widget().objectName()
            if name.startswith("pb_categories_") and item.widget().isChecked():
                categories.append(name.split("_", maxsplit=2)[-1])

        project_type = ""
        for i in range(self.hl_types.count()):
            item = self.hl_types.itemAt(i)
            if item.widget() == None:
                continue
            name = item.widget().objectName()
            if name.startswith("pb_type_") and item.widget().isChecked():
                project_type = name.split("_", maxsplit=2)[-1]

        self.search_task = Task(
            self.tr("搜索资源"),
            taskfunc=lambda _: self.search(
                self.le_keyword.text(),
                sources,
                categories,
                sortby,
                project_type,
                self.sb_limit.value(),
                self.sb_page.value(),
            ),
        )
        self.search_task.finished.connect(self.on_searchFinsihed)
        self.search_task.start()

    def search(self, keyword, sources, categories, sortby, project_type, limit, page):
        result = []
        for source in sources:
            if source == "modrinth":
                api = self.modrinthapi
                args = {"query": keyword, "limit": limit, "offset": (page - 1) * limit}
                facets = []
                if categories:
                    for category in categories:
                        facets.append(f'["categories:{category}"]')
                if sortby:
                    args["index"] = sortby
                if project_type:
                    facets.append(f'["project_type:{project_type}"]')
                if facets:
                    args["facets"] = f'[{",".join(facets)}]'
                result.append(api.search(**args))
                contents = []
                for i in result[-1]:
                    contents.append(api.get_project(i["project_id"]))
                result[-1] = {"api": "Modrinth", "contents": contents}
        self.searchFinsihed.emit(result)

    def setResults(self, results):
        self.pb_search.setEnabled(False)  # 防止在添加item时因按下搜索按钮导致出错

        self.lw_result.clear()
        n = len(results)
        for i, result in enumerate(results):
            contents = result["contents"]
            m = len(contents)
            for j, content in enumerate(contents):
                item = QListWidgetItem()
                if result["api"] == "Modrinth":
                    widget = ModrinthResItem(content)
                item.setSizeHint(widget.size())
                self.lw_result.addItem(item)
                self.lw_result.setItemWidget(item, widget)

                self.statetooltip.setContent(
                    f"{i+1}/{n}({round((i+1)/n*100,1)}%)->{j+1}/{m}({round((j+1)/m*100,1)}%)"
                )
                qApp.processEvents()

        self.statetooltip.setContent(self.tr("加载完成"))
        self.statetooltip.setState(True)
        self.statetooltip = None

        self.pb_search.setEnabled(True)

    def on_searchFinsihed(self):
        if self.statetooltip == None:
            return
        if self.search_task.terminated:
            self.statetooltip.setContent(self.tr("加载取消"))
            self.statetooltip.setState(True)
            self.statetooltip = None
