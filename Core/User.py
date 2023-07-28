import json
import logging
import os

import minecraft_launcher_lib as mll
from Setting import Setting

from Core.Requests import Requests


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
            "requestUser": False,
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
            return "没有选择的角色"
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
            user["accessToken"] = r["accessToken"]
            user["clientToken"] = r["clientToken"]
            Setting().sync()
