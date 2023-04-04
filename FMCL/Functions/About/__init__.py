from .About import About
import qtawesome as qta


def functionInfo():
    return {
        "name": "关于",
        "icon": qta.icon("mdi.information-outline")
    }


def main():
    about = About()
    about.show()
