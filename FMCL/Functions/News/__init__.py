import qtawesome as qta

from .News import News

from PyQt5.QtCore import QCoreApplication
_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("News", "新闻"),
        "icon": qta.icon("fa.newspaper-o")
    }


def main():
    news = News()
    news.show()
