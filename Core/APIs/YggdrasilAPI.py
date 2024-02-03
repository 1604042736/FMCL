"""
参考https://github.com/yushijinhun/authlib-injector/wiki
"""

import base64
import json

from Core.Network import Network

from PyQt5.QtCore import QCoreApplication

_translate = QCoreApplication.translate


class YggdrasilAPI:
    def __init__(self, base_url: str):
        self.headers = {"Content-Type": "application/json; charset=utf-8"}
        self.base_url = base_url
        self.network = Network()

    def login(self, username: str, password: str):
        url = f"{self.base_url}/authserver/authenticate"
        json_data = {
            "username": username,
            "password": password,
            "agent": {"name": "Minecraft", "version": 1},
        }
        r = self.network.post(url, json=json_data, headers=self.headers).json()
        if "error" in r:
            raise Exception(r["errorMessage"])
        return r

    def get_profile(self, uuid):
        url = f"{self.base_url}/sessionserver/session/minecraft/profile/{uuid}"
        r = self.network.get(url, headers=self.headers).json()
        if "error" in r:
            raise Exception(r["errorMessage"])
        return r

    def get_texture(self, profile):
        for pro in profile["properties"]:
            if pro["name"] == "textures":
                return json.loads(base64.b64decode(pro["value"]))
        raise Exception(
            _translate("YggdrasilAPI", "{role_name}角色没有材质").format(
                role_name=profile["name"]
            )
        )

    def refresh(self, userinfo):
        url = f"{self.base_url}/authserver/refresh"
        json_data = {
            "accessToken": userinfo["accessToken"],
            "clientToken": userinfo["clientToken"],
        }
        r = self.network.post(url, json=json_data, headers=self.headers).json()
        if "error" in r:
            raise Exception(r["errorMessage"])
        userinfo["accessToken"] = r["accessToken"]
        userinfo["clientToken"] = r["clientToken"]

    def get_metadata(self):
        r = self.network.get(self.base_url, headers=self.headers).json()
        if "error" in r:
            raise Exception(r["errorMessage"])
        return r
