# pipreqs . --encoding utf-8 --force
# pyrcc5 Resources.qrc -o __init__.py

import os
from Ui.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import Globals as g
from Ui.DownloadManager.DownloadManager import DownloadManager
from PyQt5.QtGui import QIcon
import Resources
from importlib import import_module


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

    g.dmgr = DownloadManager()  # 因为有些Ui要用到,所以要放到前面

    if '--only' in sys.argv:
        i = sys.argv.index('--only')
        name = sys.argv[i+1]
        g.logapi.info(f"单独打开:{name}")
        module = import_module(f"Ui.{name}")
        args = []
        for j in range(i+2, len(sys.argv)):
            if sys.argv[j].startswith("--"):
                break
            args.append(sys.argv[j])
        widget = getattr(module, name.split('.')[-1])(*args)
        widget.show()
    else:
        mainwindow = MainWindow()
        mainwindow.show(True)

    app.exec_()
    g.save()
    sys.exit()


if __name__ == "__main__":
    main()
