# pipreqs . --encoding utf-8 --force
# pyrcc5 Resources.qrc -o __init__.py

import os
from Ui.Desktop.Desktop import Desktop
from Ui.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import Globals as g
from Ui.DownloadManager.DownloadManager import DownloadManager
from PyQt5.QtGui import QIcon
import Resources


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/Image/icon.png"))
    g.set_theme()
    try:
        i = sys.argv.index("--updated")
        old_name = sys.argv[i+1]
        os.remove(old_name)
    except ValueError:
        pass

    g.dmgr = DownloadManager()
    g.desktop = Desktop()

    mainwindow = MainWindow()
    mainwindow.show(True)

    app.exec_()
    g.save()
    sys.exit()


if __name__ == "__main__":
    main()
