import os
import requests
import time


class Download:
    def __init__(self, url, path, callback=None):
        self.url = url
        self.path = path
        self.callback = callback
        self.max_try_time = 100  # 最大尝试次数
        if callback == None:
            self.callback = {}

    def empty(self, *_):
        pass

    def start(self):
        self.download_without_thread()

    def download_without_thread(self):
        self.callback.get("setStatus", self.empty)(f"Download {self.url}")
        with open(self.path, 'wb')as fileobj:
            try_time = 0
            while try_time != self.max_try_time:
                try:
                    rsp = requests.get(self.url, stream=True, timeout=5)
                    offset = 0
                    self.callback.get("setMax", self.empty)(
                        int(rsp.headers['Content-Length']))
                    for chunk in rsp.iter_content(chunk_size=10240):
                        if not chunk:
                            break
                        fileobj.write(chunk)  # 写入文件
                        offset = offset + len(chunk)
                        self.callback.get("setProgress")(offset)
                    break
                except Exception:
                    try_time += 1
                    fileobj.seek(0)
                    time.sleep(1)

    def check(self):
        if os.path.exists(self.path):
            return
        self.start()
