from Core.Progress import Progress
import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("Progress", "进度"),
        "icon": qta.icon("mdi.progress-download")
    }


def main():
    Progress().show()
