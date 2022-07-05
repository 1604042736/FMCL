# pipreqs . --encoding utf-8 --force

from Ui.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import Globals as g
from Ui.DownloadManager.DownloadManager import DownloadManager


def main():
    app = QApplication(sys.argv)
    g.dmgr = DownloadManager()

    mainwindow = MainWindow()
    mainwindow.show()

    app.exec_()
    g.save()
    sys.exit()


if __name__ == "__main__":
    main()
