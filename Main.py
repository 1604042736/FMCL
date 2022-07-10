# pipreqs . --encoding utf-8 --force

import os
from Ui.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import Globals as g
from Ui.DownloadManager.DownloadManager import DownloadManager


def main():
    app = QApplication(sys.argv)
    g.set_theme()
    try:
        i = sys.argv.index("--updated")
        old_name = sys.argv[i+1]
        os.remove(old_name)
    except ValueError:
        pass

    g.dmgr = DownloadManager()

    mainwindow = MainWindow()
    mainwindow.show(True)

    app.exec_()
    g.save()
    sys.exit()


if __name__ == "__main__":
    main()
