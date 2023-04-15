import logging
import os
import sys
import traceback
import webbrowser as _  # 打包exe需要

import multitasking
import PyQt5.QtWebEngineWidgets as _  # 打包exe需要
from PyQt5.QtWidgets import QMessageBox

import Core as _  # 打包exe需要
import Resources as _
from Kernel import Kernel
from Setting import Setting


def except_hook(*args):
    sys.__excepthook__(*args)
    exception = "".join([str(sys.path), "\n"] +
                        traceback.format_exception(*args))
    QMessageBox.critical(None,
                         "启动器发生了严重错误",
                         exception)
    logging.critical(exception)
    exit()


def init():
    sys.excepthook = except_hook

    if not os.path.exists("FMCL/Functions"):
        os.makedirs("FMCL/Functions")

    log_formatter = logging.Formatter(fmt='[%(asctime)s] [%(levelname)s]: %(message)s',
                                      datefmt='%Y-%m-%d,%H:%M:%S')
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
        index = sys.argv.index("--update")+1
        os.remove(sys.argv[index])
    except:
        pass
    app = Kernel()
    logging.info(f"退出代码: {app.exec()}")
    Setting().sync()
    multitasking.killall(None, None)


if __name__ == "__main__":
    main()
