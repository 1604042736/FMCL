import qtawesome as qta

from PyQt5.QtCore import QCoreApplication

from .M3U8Downloader import M3U8Downloader

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("M3U8Downloader", "M3U8下载器"),
        "icon": qta.icon("fa5s.file-download"),
    }


def main():
    m3u8downloader = M3U8Downloader()
    m3u8downloader.show()
