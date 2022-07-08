import json
import os
import requests
from Core import CoreBase
from PyQt5.QtCore import pyqtSignal
from Core.Download import download


class Updata(CoreBase):
    HasNewVersion = pyqtSignal(str)

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
        self.get_info()

        if self.info["tag_name"] != self.tag_name:
            self.HasNewVersion.emit(self.info["tag_name"])

    def updata(self):
        """更新"""
        self.get_info()

        old_name = f"FMCL_{self.tag_name}.pyzw"
        name = f'FMCL_{self.info["tag_name"]}.pyzw'
        url = self.info["assets"][0]["browser_download_url"]
        download(url, name, self)
        os.system(f"start pythonw {name} --updated {old_name}")
        exit()
