import logging
import os
import threading

from PyQt5.QtCore import QCoreApplication

from Setting import Setting
from Core.Network import Network
from Core.Task import Task
from Core.MainThreadCreator import MainThreadCreator

_translate = QCoreApplication.translate

MAX_POOL_SIZE = 10


class Download:
    def __new__(cls, *args, **kwargs):
        if threading.current_thread().getName() == "MainThread":
            return super().__new__(cls)
        else:
            return MainThreadCreator().newObject(Download, args, kwargs)

    def __init__(
        self, url: str, save_file: str, callback=None, range: tuple = None, network=None
    ) -> None:
        self.max_filesize = 1024 * 1024  # 单个下载任务最大的文件大小
        self.chunk_size = 64 * 1024

        self.url = url
        self.save_file = save_file
        self.range = range

        self.default_callback = {
            "setMax": lambda _: None,
            "setProgress": lambda _: None,
            "setStatus": lambda _: None,
            "getCurTask": lambda: None,
        }
        self.callback = (
            self.default_callback | callback
            if callback != None
            else self.default_callback
        )

        self.network = network if network != None else Network()

    def start(self):
        """开始下载"""
        logging.info(f"开始下载{self.url}到{self.save_file}")
        res = self.network.head(self.url)
        filesize = int(res.headers["Content-Length"])

        headers = {}
        if self.range != None:
            headers = {"Range": f"bytes={self.range[0]}-{self.range[1]}"}

        if filesize <= self.max_filesize or self.range != None:  # 直接下载
            self.callback["setStatus"](
                _translate("Download", "下载 {url} 到 {file}").format(
                    url=self.url, file=self.save_file
                )
            )
            self.callback["setMax"](
                self.range[1] - self.range[0] + 1 if self.range else filesize
            )
            self.callback["setProgress"](0)

            res = self.network.get(self.url, headers=headers, stream=True)
            progress = 0
            if not os.path.exists(os.path.dirname(self.save_file)):
                os.makedirs(os.path.dirname(self.save_file))
            with open(self.save_file, "wb") as f:
                for chunk in res.iter_content(chunk_size=self.chunk_size):
                    if not chunk:
                        continue
                    f.write(chunk)
                    progress += len(chunk)
                    self.callback["setProgress"](progress)
            return

        download_tasks = []
        part = 0
        tempdir = Setting()["system.temp_dir"]
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        basename = os.path.basename(self.save_file)
        basepath = f"{tempdir}/{basename}.parts"

        self.callback["setStatus"](_translate("Download", "拆分文件"))
        self.callback["setMax"](filesize // self.max_filesize + 1)
        self.callback["setProgress"](0)
        for i in range(0, filesize, self.max_filesize):
            s_pos = i
            e_pos = i + self.max_filesize - 1
            if e_pos >= filesize:
                e_pos = filesize - 1

            download_task = Task(
                _translate("Download", "下载第{part}部分").format(part=part),
                self.callback["getCurTask"](),
                lambda callback, part=part, s_pos=s_pos, e_pos=e_pos: Download(
                    self.url,
                    f"{basepath}/{basename}.part{part}",
                    range=(s_pos, e_pos),
                    callback=callback,
                    network=self.network,
                ).start(),
            )
            if len(download_tasks) >= MAX_POOL_SIZE:
                download_task.waittasks.append(
                    download_tasks[len(download_tasks) - MAX_POOL_SIZE]
                )
            download_tasks.append(download_task)
            download_task.start()
            part += 1
            self.callback["setProgress"](part)

        self.callback["setStatus"](_translate("Download", "等待各部分文件下载完成"))
        self.callback["setMax"](0)
        self.callback["setProgress"](0)
        Task.waitTasks(download_tasks, self.callback)

        self.callback["setStatus"](_translate("Download", "合并文件"))
        self.callback["setMax"](part)
        self.callback["setProgress"](0)
        if not os.path.exists(os.path.dirname(self.save_file)):
            os.makedirs(os.path.dirname(self.save_file))
        with open(self.save_file, "wb") as f:
            for i in range(part):
                f.write(open(f"{basepath}/{basename}.part{i}", "rb").read())
                self.callback["setProgress"](i + 1)

    def check(self):
        """如果文件不存在才下载"""
        if os.path.exists(self.save_file):
            return
        self.start()
