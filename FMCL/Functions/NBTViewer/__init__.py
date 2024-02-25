import qtawesome as qta

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QInputDialog


from .NBTViewer import NBTViewer

_translate = QCoreApplication.translate


def functionInfo():
    return {"name": _translate("NBTViewer", "NBT查看器"), "icon": qta.icon("fa.book")}


def main(file_or_dir=None):
    if file_or_dir == None:
        file_or_dir, ok = QInputDialog.getText(
            None,
            _translate("NBTViewer", "NBT查看器"),
            _translate("NBTViewer", "输入路径"),
        )
        if not ok:
            return
    nbtviewer = NBTViewer(file_or_dir)
    nbtviewer.show()
