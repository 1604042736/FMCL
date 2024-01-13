import logging
import os
import sys
import traceback

import multitasking
import PyQt5.QtMultimedia as _  # 打包exe需要
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox

from Core import TaskCreator

import Resources as _
from Kernel import Kernel
from Setting import Setting

_translate = QCoreApplication.translate


def except_hook(*args):
    sys.__excepthook__(*args)
    exception = "".join(traceback.format_exception(*args)).strip()
    QMessageBox.critical(None, _translate("Main", "启动器发生了严重错误"), exception)
    logging.critical(exception)
    logging.info(f"{sys.path=}")


def init():
    sys.excepthook = except_hook

    if not os.path.exists("FMCL/Functions"):
        os.makedirs("FMCL/Functions")

    log_formatter = logging.Formatter(
        fmt="[%(asctime)s][%(levelname)s][%(threadName)s]: %(message)s",
        datefmt="%Y-%m-%d,%H:%M:%S",
    )
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(log_formatter)
    fh = logging.FileHandler("FMCL/latest.log", mode="w", encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(log_formatter)
    logger.addHandler(sh)
    logger.addHandler(fh)


def main():
    init()
    try:
        index = sys.argv.index("--update") + 1
        os.remove(sys.argv[index])
    except:
        pass
    app = Kernel(sys.argv)
    TaskCreator()
    logging.info(f"退出代码: {app.exec()}")
    Setting().sync()
    multitasking.killall(None, None)


if __name__ == "__main__":
    main()
