import json
import os
import sys
import webbrowser

import multitasking
import qtawesome as qta
from Core import Download, Progress, Requests
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, qApp

from .ui_Update import Ui_Update
import time


class Update(QWidget, Ui_Update):
    hadNewVersion = pyqtSignal()
    checkError = pyqtSignal(str)

    if sys.platform == "win32":
        system_postfix = "exe"
    else:
        system_postfix = "pyzw"

    __instance = None
    __new_count = 0

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        cls.__new_count += 1
        return cls.__instance

    def __init__(self):
        if self.__new_count > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi6.update"))
        self.info = {}
        self.has_newversion = False
        self.hadNewVersion.connect(self.prepare)
        self.checkError.connect(self.te_changelog.setText)
        self.tag_name = qApp.applicationVersion()
        self.check()

    @multitasking.task
    def check(self):
        self.pb_handupdate.setEnabled(False)
        self.pb_update.setEnabled(False)
        self.pb_check.setEnabled(False)
        try:
            url = "https://api.github.com/repos/1604042736/FMCL/releases/latest"
            r = Requests.get(url, try_time=-1, cache=False, verify=False)
            self.info = json.loads(r.content)

            if self.info["tag_name"] != self.tag_name:
                self.has_newversion = True
                self.hadNewVersion.emit()

            while self.isHidden() and self.has_newversion:
                self.hadNewVersion.emit()
                time.sleep(1)
        except Exception as e:
            self.checkError.emit(str(e))
        self.pb_check.setEnabled(True)

    def prepare(self):
        self.pb_handupdate.setEnabled(True)
        self.pb_update.setEnabled(True)
        self.setWindowTitle(f"更新:{self.info['tag_name']}")
        self.te_changelog.setText(self.info["body"])
        self.show()

    def update_(self, callback):
        old_name = f"FMCL_{self.tag_name}.{self.system_postfix}"
        name = f"FMCL_{self.info['tag_name']}.{self.system_postfix}"
        url = self.info["assets"][0]["browser_download_url"]  # 默认pyzw的下载地址
        for i in self.info["assets"]:
            if i["name"].endswith('.'+self.system_postfix):
                url = i["browser_download_url"]
                break

        Download(url, name, callback).start()

        os.popen(f'start {name} --update "{old_name}"')
        qApp.quit()

    @pyqtSlot(bool)
    def on_pb_update_clicked(self, _):
        Progress().add(lambda callback: self.update_(callback))

    @pyqtSlot(bool)
    def on_pb_check_clicked(self, _):
        self.has_newversion = False
        self.te_changelog.setText("")
        self.check()

    @pyqtSlot(bool)
    def on_pb_handupdate_clicked(self, _):
        webbrowser.open(self.info["html_url"])
