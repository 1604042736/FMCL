import logging
import os
import subprocess
import qtawesome as qta
import m3u8

from PyQt5.QtCore import pyqtSlot, QCoreApplication
from PyQt5.QtWidgets import QWidget, QFileDialog
import requests

from Core import Network, Task, Download
from Setting import Setting

from .ui_M3U8Downloader import Ui_M3U8Downloader

_translate = QCoreApplication.translate


class M3U8Downloader(QWidget, Ui_M3U8Downloader):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("fa5s.file-download"))

        self.tasks: list[Task] = []

    @pyqtSlot(bool)
    def on_pb_download_clicked(self, _):
        url = self.le_url.text()
        name = self.le_name.text()
        save_path = self.le_savepath.text()
        self.tasks.append(
            Task(
                self.tr("下载") + f": {name}({url})",
                taskfunc=lambda callback: DownloadTask(
                    url, name, save_path, callback
                ).start(),
            )
        )
        self.tasks[-1].start()

    @pyqtSlot(bool)
    def on_pb_choosepath_clicked(self, _):
        dir = QFileDialog.getExistingDirectory(None, self.tr("选择保存路径"))
        if dir:
            self.le_savepath.setText(dir)


MAX_POOL_SIZE = 10


class DownloadTask:
    # 参考https://blog.csdn.net/wangkunggxx/article/details/134444941
    def __init__(self, url, name, save_path, callback=None):
        self.url = url
        self.name = name
        self.save_path = save_path
        if callback == None:
            callback = {
                "setStatus": lambda _: None,
                "setProgress": lambda _: None,
                "setMax": lambda _: None,
                "getCurTask": lambda: None,
            }
        self.callback = callback
        self.temp_dir = os.path.join(Setting()["system.temp_dir"], self.name)

    def tr(self, text):
        return _translate("DownloadTask", text)

    def start(self):
        logging.info(f"下载m3u8: {self.url=}, {self.name=}, {self.save_path=}")
        self.callback["setStatus"](self.tr("解析M3U8"))
        playlist = self.parse_m3u8(self.url)
        urls_paths = self.get_files_and_paths(playlist)
        m3u8_path = os.path.join(self.temp_dir, "index.m3u8")
        self.create_native_m3u8_file(playlist, m3u8_path)

        self.callback["setStatus"](self.tr("下载ts文件"))
        self.callback["setMax"](len(urls_paths))
        tasks = []
        for count, (url, path) in enumerate(urls_paths):

            def download(url, path, callback):
                session = requests.Session()
                session.timeout = 3
                Download(
                    url,
                    path,
                    callback,
                    network=Network(session, retry_time=2**32, retry_delay=0),
                ).start()

            task_download = Task(
                self.tr("下载") + f": {url}",
                self.callback["getCurTask"](),
                lambda callback, url=url, path=path: download(url, path, callback),
            )
            if count - MAX_POOL_SIZE >= 0:
                task_download.waittasks.append(tasks[count - MAX_POOL_SIZE])
            tasks.append(task_download)
            task_download.start()
            self.callback["setProgress"](count + 1)
        self.callback["setMax"](0)
        Task.waitTasks(tasks, self.callback)

        self.callback["setStatus"](self.tr("合并ts文件"))
        mp4_path = os.path.join(self.save_path, f"{self.name}.mp4")
        args = ["ffmpeg", "-i", m3u8_path, "-c", "copy", mp4_path, "-y"]
        process = subprocess.run(args, capture_output=True)
        logging.info(process.stdout)
        logging.info(process.stderr)

    def parse_m3u8(self, url):
        playlist = m3u8.load(url)
        if not playlist.is_variant:
            return playlist
        playlists = playlist.playlists
        if len(playlists) == 0:
            return None
        return self.parse_m3u8(playlists[0].absolute_uri)

    def get_files_and_paths(self, playlist: m3u8.M3U8):
        urls_paths = []
        for seg in playlist.segments:
            if seg == None:
                break
            urls_paths.append(
                (
                    seg.absolute_uri,
                    os.path.join(self.temp_dir, os.path.basename(seg.absolute_uri)),
                )
            )
        for key in playlist.keys:
            if key == None:
                break
            urls_paths.append(
                (
                    key.absolute_uri,
                    os.path.join(self.temp_dir, os.path.basename(key.absolute_uri)),
                )
            )
        return urls_paths

    def create_native_m3u8_file(self, playlist: m3u8.M3U8, m3u8_path):
        for seg in playlist.segments:
            if seg == None:
                break
            seg.uri = os.path.basename(seg.absolute_uri)
        for key in playlist.keys:
            if key == None:
                break
            key.uri = os.path.basename(key.absolute_uri)
        playlist.dump(m3u8_path)
