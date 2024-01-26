import requests
from requests.adapters import HTTPAdapter

from PyQt5.QtWidgets import qApp


class Network:
    @staticmethod
    def get_default_headers():
        return {"user-agent": f"1604042736/FMCL/{qApp.applicationVersion()}"}

    def __init__(self, session: requests.Session = None, retry_time: int = 3):
        self.session = session if session != None else requests.session()
        self.session.mount("https://", HTTPAdapter(max_retries=retry_time))
        self.session.mount("http://", HTTPAdapter(max_retries=retry_time))
        self.retry_time = retry_time

    def get(self, url, **kwargs):
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"] = self.get_default_headers() | kwargs["headers"]
        return self.session.get(url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"] = self.get_default_headers() | kwargs["headers"]
        return self.session.post(url, data, json, **kwargs)

    def head(self, url, **kwargs):
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"] = self.get_default_headers() | kwargs["headers"]
        return self.session.head(url, **kwargs)
