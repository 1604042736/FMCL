from .ModDownloader import ModDownloader
import qtawesome as qta


def functionInfo():
    return {
        "name": "Mod下载器",
        "icon": qta.icon("mdi.puzzle-outline")
    }


def main():
    moddownloader = ModDownloader()
    moddownloader.show()
