import logging
import os

import minecraft_launcher_lib as mll
import qtawesome as qta
from PIL import Image, ImageQt
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QInputDialog
from Setting import Setting

from Core.Download import Download
from Core.APIs.YggdrasilAPI import YggdrasilAPI

_translate = QCoreApplication.translate


class User:
    @staticmethod
    def create_offline(username: str, uuid: str = ""):
        """创建离线登录用户"""
        setting = {}
        setting = mll.utils.generate_test_options()
        setting["type"] = "offline"
        setting["username"] = username
        if uuid:
            setting["uuid"] = uuid
        User.add_user(setting)

    @staticmethod
    def create_microsoft():
        """创建微软用户"""
        # FIXME

    @staticmethod
    def create_yggdrasil(base_url: str, username: str, password: str):
        """创建Yggdrasil账户"""
        logging.info(f"开始创建{base_url}用户")
        api = YggdrasilAPI(base_url)

        logging.info("登录")
        userinfo: dict = api.login(username, password)

        availableProfiles = userinfo.pop("availableProfiles")
        if len(availableProfiles) == 0:
            raise Exception(_translate("User", "请先创建角色"))
        if len(availableProfiles) == 1:
            selectedProfile = availableProfiles[0]
        else:
            name, ok = QInputDialog.getItem(
                None,
                _translate("User", "创建用户"),
                _translate("User", "选择角色"),
                [i["name"] for i in availableProfiles],
                editable=False,
            )
            if not ok:
                return
            for i in availableProfiles:
                if i["name"] == name:
                    selectedProfile = i
                    break

        setting = {}
        setting["type"] = "authlibInjector"
        setting["username"] = selectedProfile["name"]
        setting["uuid"] = selectedProfile["id"]
        setting["clientToken"] = userinfo["clientToken"]
        setting["accessToken"] = userinfo["accessToken"]
        setting["token"] = userinfo["accessToken"]
        setting["serverbaseurl"] = base_url

        setting["profile"] = api.get_profile(selectedProfile["id"])

        User.add_user(setting)

    @staticmethod
    def add_user(user: dict):
        globalsetting = Setting()
        for _user in globalsetting["users"]:
            if (
                _user.get("serverbaseurl") == user.get("serverbaseurl")
                and _user["uuid"] == user["uuid"]
                and _user["type"] == user["type"]
                and _user["username"] == user["username"]
            ):
                _user |= user  # 覆盖
                Setting().sync()
                break
        else:
            globalsetting["users"].append(user)

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
        if user["type"] == "authlibInjector":
            api = YggdrasilAPI(user["serverbaseurl"])
            api.refresh(user)
            user["profile"] = api.get_profile(user["profile"]["id"])
            Setting().sync()

    @staticmethod
    def get_head(user: dict):
        """获取头像"""
        if user["type"] == "authlibInjector":
            api = YggdrasilAPI(user["serverbaseurl"])
            try:
                textures = api.get_texture(user["profile"])
            except:
                return qta.icon("ph.user-circle")  # 找不到材质
            if "SKIN" in textures["textures"]:
                url = textures["textures"]["SKIN"]["url"]
                name = url.split("/")[-1]
                temp_dir = Setting()["system.temp_dir"]
                path = f"{temp_dir}/Skin/{name}.png"
                if not os.path.exists(f"{temp_dir}/Skin"):
                    os.makedirs(f"{temp_dir}/Skin")
                logging.info("下载皮肤")
                Download(
                    url,
                    path,
                    {
                        "setMax": logging.info,
                        "setProgress": logging.info,
                        "setStatus": logging.info,
                    },
                ).check()
                img = Image.open(path)
                head = img.crop((8, 8, 16, 16))
                head = ImageQt.ImageQt(head)
                img.close()
                return head
        return QImage(":/Image/defaulthead.png")

    @staticmethod
    def get_servername(user: dict):
        """获取认证服务器名称"""
        if user["type"] != "authlibInjector":
            return ""
        for server in Setting()["users.authlibinjector_servers"]:
            if server["url"] == user["serverbaseurl"]:
                return server["meta"]["serverName"]
        return YggdrasilAPI(server["serverbaseurl"]).get_metadata()["meta"][
            "serverName"
        ]
