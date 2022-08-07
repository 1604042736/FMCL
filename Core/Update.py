import json
import os
import sys
import requests
from Core import CoreBase
from PyQt5.QtCore import pyqtSignal
from Core.Download import download
from PyQt5.QtWidgets import qApp
import Globals as g
import platform


class Update(CoreBase):
    HasNewVersion = pyqtSignal(str)
    NoNewVersion = pyqtSignal()

    system_postfix = {
        "Windows": "exe"
    }

    def __init__(self, tag_name) -> None:
        super().__init__()
        self.tag_name = tag_name

    def get_info(self):
        if "info" not in self.__dict__:
            url = "https://api.github.com/repos/1604042736/FMCL/releases/latest"
            r = requests.get(url)
            self.info = json.loads(r.content)

    def check(self):
        """检查"""
        g.logapi.info("检查更新")
        self.get_info()

        if self.info["tag_name"] != self.tag_name:
            self.HasNewVersion.emit(self.info["tag_name"])
        else:
            self.NoNewVersion.emit()

    def update(self):
        """更新"""
        self.get_info()

        old_name = sys.argv[0]
        system = platform.system()
        name = f'FMCL_{self.info["tag_name"]}.{self.system_postfix.get(system,"pyzw")}'

        url = self.info["assets"][0]["browser_download_url"]  # 默认pyzw的下载地址
        for i in self.info["assets"]:
            if i["name"].endswith('.'+self.system_postfix.get(system, "pyzw")):
                url = i["browser_download_url"]
                break

        download(url, name, self)
        os.popen(f'start "{name}" --updated "{old_name}"')
        qApp.quit()
