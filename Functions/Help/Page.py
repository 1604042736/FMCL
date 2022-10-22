from PyQt5.QtCore import QFile, QObject, QUrl, pyqtProperty
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView

from . import Help_rc as _


class Document(QObject):
    def __init__(self, filename: str) -> None:
        super().__init__()
        self.file = QFile(filename)
        self.file.open(QFile.OpenModeFlag.ReadOnly)
        self.m_text = bytes(self.file.readAll()).decode("utf-8")

    @pyqtProperty(str)
    def text(self):
        return self.m_text


class Page(QWebEngineView):
    def __init__(self, filename: str) -> None:
        super().__init__()
        self.setWindowTitle(filename)

        self.webpage = QWebEnginePage(self)
        self.webchannel = QWebChannel()
        self.document = Document(filename)
        self.webchannel.registerObject("content", self.document)
        self.webpage.setWebChannel(self.webchannel)
        self.setPage(self.webpage)
        self.setUrl(QUrl("qrc:/index.html"))
