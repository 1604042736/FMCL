import os
import threading
import time
from typing import Callable
import requests
import Globals as g
from Core import CoreBase


class Download(CoreBase):
    def __init__(self, url, path) -> None:
        super().__init__()
        self.url = url
        self.path = path
        self.thread_count = g.max_thread_count  # 启用线程数
        self.download_bytes = {}  # 保存下载的bytes
        self.finished_thread = 0  # 完成的线程
        self.max_try_time = 100  # 最大尝试次数
        self.min_filesize = 1024*1024  # 最小需要多线程下载的文件大小
        try:
            # 创建这个路径
            os.makedirs(os.path.dirname(path))
        except:
            pass

    def download_thread(self, byte_range):
        headers = {
            "Range": f"bytes={byte_range[0]}-{byte_range[1]}"
        }
        try_time = 0
        while try_time != self.max_try_time:
            try:
                r = requests.get(self.url, headers=headers, timeout=5)
                self.download_bytes[byte_range[0]] = r.content
                self.finished_thread += 1
                break
            except:
                g.logapi.info(f"尝试重新下载:{self.url},{byte_range}")
                try_time += 1
                time.sleep(1)

    def start(self):
        """下载"""
        if self.url == '':
            self.Finished.emit()

        g.logapi.info(f'下载"{self.url}"到"{self.path}"')
        headers = {
            "Accept-Encoding": "identity"
        }
        file_size = int(requests.head(
            self.url, headers=headers).headers['Content-Length'])
        g.logapi.info(f"{self.url}大小:{file_size}")

        if file_size < self.min_filesize:  # 小文件不用多线程下载
            self.start_without_thread()
        else:
            self.start_with_thread(file_size)

    def start_with_thread(self, file_size):
        """多线程下载"""
        # 获取各部分长度
        ranges = []
        start_bytes = -1
        for i in range(self.thread_count):
            end_bytes = int(file_size/self.thread_count)*i
            if i == self.thread_count-1:
                end_bytes = file_size
            ranges.append((start_bytes+1, end_bytes))
            start_bytes = end_bytes

        # 开始下载
        thread_list = []
        for i in range(self.thread_count):
            t = threading.Thread(
                target=self.download_thread, args=(ranges[i],))
            t.setDaemon(True)
            t.start()
            thread_list.append(t)

        while self.thread_count != self.finished_thread:
            self.Progress.emit(self.finished_thread, self.thread_count)

        # 合并
        with open(self.path, 'wb')as file:
            for i in ranges:
                file.write(self.download_bytes[i[0]])
        self.Finished.emit()

    def start_without_thread(self):
        """不使用多线程下载"""
        with open(self.path, 'wb')as fileobj:
            try_time = 0
            while try_time != self.max_try_time:
                try:
                    rsp = requests.get(self.url, stream=True, timeout=5)
                    # 再判断一次
                    # 对于某些网站用requests.head获取Content-Length不一定正确
                    if int(rsp.headers["Content-Length"]) >= self.min_filesize:
                        self.start_with_thread(
                            int(rsp.headers["Content-Length"]))
                    offset = 0
                    for chunk in rsp.iter_content(chunk_size=10240):
                        if not chunk:
                            break
                        fileobj.write(chunk)  # 写入文件
                        offset = offset + len(chunk)
                        if "Content-Length" in rsp.headers:
                            self.Progress.emit(offset,
                                               int(rsp.headers['Content-Length']))
                    break
                except Exception:
                    g.logapi.info(f"尝试重新下载:{self.url}")
                    try_time += 1
                    fileobj.seek(0)
                    time.sleep(1)
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


def start_with_count(d: Download, count: list):
    d.start()
    count[0] += 1


def check_with_count(d: Download, count: list):
    d.check()
    count[0] += 1


def download_list(check=False):
    """下载列表(作为装饰器)"""
    def download(func: Callable[[], list[(str, str)]]):
        def wrap(*args):
            downloads: list[tuple[str, str, Download]] = func(*args)
            count = [0, len(downloads)]
            thread_list = []
            for url, path, cls in downloads:
                d = Download(url, path)
                d.Error.connect(lambda a: cls.Error.emit(a))
                if check:
                    t = threading.Thread(
                        target=check_with_count, args=(d, count))
                else:
                    t = threading.Thread(
                        target=start_with_count, args=(d, count))
                t.setDaemon(True)
                t.start()
                thread_list.append(t)
            while count[0] != count[1]:
                downloads[0][2].Progress.emit(count[0], count[1])
                time.sleep(1)  # 频繁发送信号会让界面卡死
        return wrap
    return download
