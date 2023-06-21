import qtawesome as qta

from .Help import Help
from .Page import Page


def functionInfo():
    return {
        "name": "帮助",
        "icon": qta.icon("mdi.help")
    }


def main(page: str = None):
    if page:
        page = Page(page)
        page.show()
    else:
        help = Help()
        help.show()
