import base64
import json
import logging
import os

import minecraft_launcher_lib as mll
import qtawesome as qta
from PIL import Image, ImageQt
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QImage
from Setting import Setting

from Core.Download import Download
from Core.Requests import Requests

_translate=QCoreApplication.translate

class User:
    @staticmethod
    def create_offline(username: str):
        """创建离线登录用户"""
        globalsetting = Setting()
        setting = {}
        setting = mll.utils.generate_test_options()
        setting["type"] = "offline"
        setting["username"] = username
        globalsetting["users"].append(setting)
        globalsetting.sync()

    @staticmethod
    def create_microsoft():
        """创建微软用户"""
        # FIXME

    @staticmethod
    def create_littleskin(username: str, password: str):
        """创建LitteSkin账户"""
        logging.info("开始创建LittleSkin用户")
        api = "https://littleskin.cn/api/yggdrasil"

        logging.info("登录")
        data = {
            "username": username,
            "password": password,
            "requestUser": True,
            "agent": {
                "name": "Minecraft",
                "version": 1
            }
        }
        r = Requests.post(f"{api}/authserver/authenticate",
                          json=data,
                          headers={"Content-Type": "application/json"}).json()
        if "errorMessage" in r:
            return r["errorMessage"]
        if not r["selectedProfile"]:
            return _translate("User","没有选择的角色")

        globalsetting = Setting()
        setting = {}
        name = r["selectedProfile"]["name"]
        setting["type"] = "authlibInjector"
        setting["username"] = name
        setting["uuid"] = r["selectedProfile"]["id"]
        setting["clientToken"] = r["clientToken"]
        setting["accessToken"] = r["accessToken"]
        setting["token"] = r["accessToken"]
        setting["mode"] = "LittleSkin"

        prole = Requests.get(
            f'{api}/sessionserver/session/minecraft/profile/{r["selectedProfile"]["id"]}').json()
        setting["profileProperties"] = prole["properties"]

        for i in range(len(globalsetting["users"])):
            user = globalsetting["users"][i]
            if (user["type"] == setting["type"]
                and user["username"] == setting["username"]
                    and user["mode"] == setting["mode"]):  # 如果是重登录只需覆盖
                globalsetting["users"][i] = setting
                break
        else:
            globalsetting["users"].append(setting)
        globalsetting.sync()

    @staticmethod
    def delete(user: dict):
        """删除用户"""
        setting = Setting()
        setting["users"].remove(user)
        if setting["users.selectindex"] >= len(setting["users"]):
            setting["users.selectindex"] -= 1
        setting.sync()

    @staticmethod
    def get_cur_user():
        """获取当前用户"""
        setting = Setting()
        if setting["users"]:
            return setting["users"][setting["users.selectindex"]]
        return None

    @staticmethod
    def refresh(user: dict):
        if user["type"] == "authlibInjector" and user["mode"] == "LittleSkin":
            api = "https://littleskin.cn/api/yggdrasil"
            logging.info("刷新")
            data = {
                "accessToken": user["accessToken"],
                "clientToken": user["clientToken"]
            }
            r = Requests.post(f"{api}/authserver/refresh",
                              json=data,
                              headers={"Content-Type": "application/json"}).json()
            if "error" in r:
                return r
            user["accessToken"] = r["accessToken"]
            user["clientToken"] = r["clientToken"]
            Setting().sync()

    @staticmethod
    def get_head(user: dict):
        """获取头像"""
        if user["type"] == "authlibInjector" and user["mode"] == "LittleSkin":
            for i in user["profileProperties"]:
                if i["name"] == "textures":
                    textures = json.loads(base64.b64decode(i["value"]))
                    break
            else:
                return qta.icon("ph.user-circle")  # 找不到材质
            if "SKIN" in textures["textures"]:
                url = textures["textures"]["SKIN"]["url"]
                name = url.split("/")[-1]
                path = f"FMCL/Skin/{name}.png"
                if not os.path.exists("FMCL/Skin"):
                    os.makedirs("FMCL/Skin")
                logging.info("下载皮肤")
                Download(url, path, {"setMax": logging.info,
                         "setProgress": logging.info}).check()
                img = Image.open(path)
                head = img.crop((8, 8, 16, 16))
                head = ImageQt.ImageQt(head)
                img.close()
                return head
        return QImage(":/Image/defaulthead.png")
