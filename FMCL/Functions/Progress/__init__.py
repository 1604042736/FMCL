from Core.Progress import Progress
import qtawesome as qta


def functionInfo():
    return {
        "name": "进度",
        "icon": qta.icon("mdi.progress-download")
    }


def main():
    Progress().show()
