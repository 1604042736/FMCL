from .GameDownloader import GameDownloader
import qtawesome as qta


def functionInfo():
    return {
        "name": "游戏下载器",
        "icon": qta.icon("ph.download-simple")
    }


def main():
    gamedownloader = GameDownloader()
    gamedownloader.show()
