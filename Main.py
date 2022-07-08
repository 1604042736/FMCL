# pipreqs . --encoding utf-8 --force

import os
from Ui.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import Globals as g
from Ui.DownloadManager.DownloadManager import DownloadManager


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
QGroupBox{
    font-size: 13px;
    font-weight: bold;
    border:4px solid white;
    border-radius:10px;
    background-color:white;
}
QListWidget{
    border:none;
}
QListWidget::Item:hover{
    background-color:rgb(240,240,240);
}
QListWidget::Item:selected{
    background-color:rgb(230,230,230);
}
QPushButton{
    border:1px solid rgb(0,0,0);
}
QPushButton:hover{
    background-color:rgb(200,200,200);
}
QLabel{
    font-size:13px;
}
QTabWidget{
    border:none;
}
QComboBox{
    border:1px solid rgb(0,0,0);
    background-color:rgb(240,240,240)
}
QComboBox QAbstractItemView{
    outline: 0px solid rgb(0,0,0);
    border:none;
    background-color: rgb(255,255,255);
}
QComboBox QAbstractItemView::item:hover{
    color: rgb(240,240,240);
}
QComboBox QAbstractItemView::item:selected{
    color: rgb(230,230,230);
}
QComboBox QAbstractScrollArea QScrollBar:vertical {
    width: 8px;
    background-color: rgb(255,255,255);
}
QComboBox::drop-down{
    border:none;
}
""")
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
