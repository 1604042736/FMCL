from PyQt5.QtCore import pyqtSignal
import os
from PyQt5.QtCore import QObject
import requests


class Download(QObject):
    Finished = pyqtSignal()
    Progress = pyqtSignal(int, int)

    def __init__(self, url, path) -> None:
        super().__init__()
        self.url = url
        self.path = path
        try:
            # 创建这个路径
            os.makedirs(os.path.dirname(path))
        except:
            pass

    def start(self):
        """下载"""
        if self.url == '':
            return
        with open(self.path, 'wb')as fileobj:
            while True:
                try:
                    rsp = requests.get(self.url, stream=True, timeout=5)
                    offset = 0
                    for chunk in rsp.iter_content(chunk_size=1024):
                        if not chunk:
                            break
                        fileobj.write(chunk)  # 写入文件
                        offset = offset + len(chunk)
                        self.Progress.emit(offset,
                                           int(rsp.headers['Content-Length']))
                    break
                except Exception as e:
                    print(e)
                    fileobj.seek(0)
        self.Finished.emit()

    def check(self, redownload=False):
        '''检查文件是否下载'''
        if not redownload and os.path.exists(self.path):
            return
        self.start()


def download(url, path, cls, check=False):
    """下载"""
    d = Download(url, path)
    d.Progress.connect(lambda cur, total: cls.Progress.emit(cur, total))
    if check:
        d.check()
    else:
        d.start()
