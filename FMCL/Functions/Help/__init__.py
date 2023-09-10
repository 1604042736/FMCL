import qtawesome as qta
from PyQt5.QtCore import QCoreApplication

from .Help import Help
from .Page import Page

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("Help", "帮助"),
        "icon": qta.icon("mdi.help")
    }


def main(page: str = None):
    if page:
        page = Page(page)
        page.show()
    else:
        help = Help()
        help.show()
