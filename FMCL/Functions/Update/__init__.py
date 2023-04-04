import qtawesome as qta

from .Update import Update


def functionInfo():
    return {
        "name": "更新",
        "icon": qta.icon("mdi6.update")
    }


fisrt_run = True


def main():
    global fisrt_run
    if fisrt_run:
        update = Update()
        fisrt_run = False
    else:
        update = Update()
        update.show()
