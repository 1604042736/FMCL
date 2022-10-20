import multitasking
import qtawesome as qta
from Core import Download, Mod, Progress
from PyQt5.QtCore import QCoreApplication, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QTreeWidgetItem, QWidget

from .ModFound import ModFound
from .ui_ModDownloader import Ui_ModDownloader

_translate = QCoreApplication.translate


class ModDownloader(QWidget, Ui_ModDownloader):
    __modFound = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.puzzle-outline"))
        self.mod = Mod()
        self.cb_downloadsource.addItems(self.mod.get_all_downloadsources())
        self.cb_sort.addItems(self.mod.get_all_sortmethod())
        self.cb_downloadsource.currentTextChanged.connect(
            self.mod.set_downloadsource)
        self.__modFound.connect(self.addMod)

    @pyqtSlot(bool)
    def on_pb_search_clicked(self, _):
        self.search()

    @multitasking.task
    def search(self):
        self.pb_search.setEnabled(False)
        self.tw_mods.clear()
        self.tw_files.clear()
        name = self.le_name.text()
        sort = self.cb_sort.currentText()
        for i in self.mod.search(name, sort, yield_=True):
            self.__modFound.emit(i)
        self.pb_search.setEnabled(True)

    def setMods(self, mods: list):
        self.tw_mods.clear()
        for mod in mods:
            self.addMod(mod)

    def addMod(self, mod: dict, root=None):
        item = QTreeWidgetItem()
        widget = ModFound(mod)
        item.setSizeHint(0, widget.size())
        if root == None:
            self.tw_mods.addTopLevelItem(item)
        else:
            root.addChild(item)
        self.tw_mods.setItemWidget(item, 0, widget)

        for i in mod["dependencies"]:
            self.addMod(i, item)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_tw_mods_itemClicked(self, item, col):
        widget = self.tw_mods.itemWidget(item, col)
        root = {}
        self.tw_files.clear()
        for version, files in widget.foundmod["files"].items():
            root = QTreeWidgetItem()
            root.setText(0, version)
            self.tw_files.addTopLevelItem(root)
            for filename in files:
                item = QTreeWidgetItem()
                item.setText(0, filename)
                root.addChild(item)

    @pyqtSlot(bool)
    def on_pb_download_clicked(self, _):
        fileitem = self.tw_files.currentItem()
        filename = fileitem.text(0)
        versionitem = fileitem.parent()
        if versionitem == None:
            return
        version = versionitem.text(0)
        widget = self.tw_mods.itemWidget(self.tw_mods.currentItem(), 0)
        url = widget.foundmod["files"][version][filename]["url"]
        path = QFileDialog.getSaveFileName(
            self, _translate("ModDownloader", "下载"), f"./{filename}")[0]
        if path:
            Progress().add(lambda callback: Download(url, path, callback).start())
