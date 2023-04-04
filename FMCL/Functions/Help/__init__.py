from .Help import Help
import qtawesome as qta


def functionInfo():
    return {
        "name": "帮助",
        "icon": qta.icon("mdi.help")
    }


def main():
    help = Help()
    help.show()
