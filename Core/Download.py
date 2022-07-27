import os
import requests
import Globals as g
from Core import CoreBase


class Download(CoreBase):
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
            self.Finished.emit()
        g.logapi.info(f'下载"{self.url}"到"{self.path}')
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
                        if "Content-Length" in rsp.headers:
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
            self.Finished.emit()
            return
        self.start()


def download(url, path, cls: CoreBase, check=False):
    """下载"""
    d = Download(url, path)
    d.Finished.connect(lambda: cls.Finished.emit())
    d.Progress.connect(lambda cur, total: cls.Progress.emit(cur, total))
    d.Error.connect(lambda a: cls.Error.emit(a))
    if check:
        d.check()
    else:
        d.start()
