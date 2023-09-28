import qtawesome as qta
from PyQt5.QtCore import QFile, QObject, pyqtProperty
from qfluentwidgets import TextEdit


class Document(QObject):
    def __init__(self, filename: str) -> None:
        super().__init__()
        self.file = QFile(filename)
        self.file.open(QFile.OpenModeFlag.ReadOnly)
        self.m_text = bytes(self.file.readAll()).decode("utf-8")
        self.file.close()

    @pyqtProperty(str)
    def text(self):
        return self.m_text


class Page(TextEdit):
    instances = {}
    new_count = {}

    def __new__(cls, filename):
        if filename not in Page.instances:
            Page.instances[filename] = super().__new__(cls)
            Page.new_count[filename] = 0
        Page.new_count[filename] += 1
        return Page.instances[filename]

    def __init__(self, filename: str) -> None:
        if Page.new_count[filename] > 1:
            return
        super().__init__()
        self.setWindowTitle(filename)
        self.setWindowIcon(qta.icon("ri.pages-line"))
        self.setReadOnly(True)
        self.file = QFile(filename)
        self.file.open(QFile.OpenModeFlag.ReadOnly)
        self.m_text = bytes(self.file.readAll()).decode("utf-8")
        self.setMarkdown(self.m_text)
        self.file.close()
