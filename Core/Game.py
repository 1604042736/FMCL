import json
import logging
import os
import shutil

import minecraft_launcher_lib as mll
from Globals import Globals
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
from System.Setting import Setting

from .Progress import Progress
from .User import User

_translate = QCoreApplication.translate


class Game:
    @staticmethod
    def get_versions():
        result = []
        for i in mll.utils.get_version_list():
            result.append(i["id"])
        return result

    @staticmethod
    def get_forge(version):
        result = []
        for i in mll.forge.list_forge_versions():
            if version == i.split("-")[0]:
                result.append(i)
        return result

    @staticmethod
    def get_fabric():
        result = []
        for i in mll.fabric.get_all_loader_versions():
            result.append(i["version"])
        return result

    def __init__(self, name: str) -> None:
        self.name = name
        self.directory = Setting().get("game/directories")[0]

        self.DEFAULT_SETTING = {
            "specific": {
                "name": _translate("GameSetting", "特定设置"),
                "value": False
            },
            "isolation": {
                "name": _translate("GameSetting", "版本隔离"),
                "value": False
            },
            "logo": {
                "name": _translate("GameSetting", "游戏图标"),
                "description": _translate("GameSetting", "除非您知道自己在干什么,否则不要手动更改此设置"),
                "value": ""
            }
        }

    def launch(self):
        options = User.get_cur_user()
        options["launcherName"] = "FMCL"
        options["launcherVersion"] = Globals.TAG_NAME
        options["gameDirectory"] = self.directory
        options["customResolution"] = True
        options["resolutionWidth"] = str(Setting().get("game/width"))
        options["resolutionHeight"] = str(Setting().get("game/height"))
        options["executablePath"] = "javaw"
        self.generate_setting()
        if self.setting.get("isolation"):
            options["gameDirectory"] = os.path.abspath(
                os.path.join(self.directory, "versions", self.name))

        command = mll.command.get_minecraft_command(
            self.name, os.path.abspath(self.directory), options)

        str_command = ""
        for i in command:
            if " " in i:
                str_command += '"'+i+'" '
            else:
                str_command += i+' '
        logging.info(str_command)
        os.popen(f"cd {self.directory}&start {str_command}")

    def install_forge(self, forge_version, callback):
        mll.forge.install_forge_version(
            forge_version, self.directory, callback)
        Game(forge_version).rename(self.name)

    def install_fabric(self, version, fabric_version, callback):
        mll.fabric.install_fabric(
            version, self.directory, fabric_version, callback)
        Game(version).rename(self.name)

    def install_mc(self, version, callback):
        mll.install.install_minecraft_version(
            version, self.directory, callback)
        Game(version).rename(self.name)

    def install(self, version, forge_version, fabric_version):
        if forge_version:
            Progress().add(lambda callback: self.install_forge(forge_version, callback))
        elif fabric_version:
            Progress().add(lambda callback: self.install_fabric(version, fabric_version, callback))
        else:
            Progress().add(lambda callback: self.install_mc(version, callback))

    def rename(self, new_name):
        os.rename(f"{self.directory}/versions/{self.name}/{self.name}.jar",
                  f"{self.directory}/versions/{self.name}/{new_name}.jar")
        os.rename(f"{self.directory}/versions/{self.name}/{self.name}.json",
                  f"{self.directory}/versions/{self.name}/{new_name}.json")
        os.rename(f"{self.directory}/versions/{self.name}",
                  f"{self.directory}/versions/{new_name}")

    def get_info(self) -> dict:
        info = {
            "version": "",
            "forge_version": "",
            "fabric_version": ""
        }
        config = json.load(open(os.path.join(
            self.directory, "versions", self.name, f"{self.name}.json"), encoding="utf-8"))

        try:
            i = config["arguments"]["game"].index("--fml.forgeVersion")
            info["forge_version"] = config["arguments"]["game"][i+1]
            i = config["arguments"]["game"].index("--fml.mcVersion")
            info["version"] = config["arguments"]["game"][i+1]
            return info
        except:
            pass

        if "net.minecraftforge:forge:" in config["libraries"][0]["name"]:
            version, forge_version = config["libraries"][0]["name"].rsplit(
                ":")[-1].split("-")
            info["version"] = version
            info["forge_version"] = forge_version
            return info

        for i in config["libraries"]:
            if "net.fabricmc:fabric-loader:" in i["name"]:
                info["fabric_version"] = i["name"].replace(
                    "net.fabricmc:fabric-loader:", "")
                break
        if "clientVersion" in config:
            info["version"] = config["clientVersion"]
        else:
            info["version"] = config["id"]
        return info

    def get_mod(self) -> list:
        self.generate_setting()
        if self.setting.get("isolation"):
            path = os.path.join(self.directory, "versions", self.name, "mods")
        else:
            path = os.path.join(self.directory, "mods")
        if not os.path.exists(path):
            return []
        result = []
        for i in os.listdir(path):
            if ".jar" in i:
                if i.endswith(".disabled"):
                    result.append((0, i.replace(".disabled", "")))
                elif i.endswith(".jar"):
                    result.append((2, i))
        return result

    def open_directory(self):
        os.startfile(os.path.join(self.directory, "versions", self.name))

    def setModEnabled(self, mod: str, state: int):
        path = os.path.join(self.directory, "mods", mod)
        disabled_path = os.path.join(self.directory, "mods", f"{mod}.disbaled")
        if state == 0:
            os.rename(path, disabled_path)
        else:
            os.rename(disabled_path, path)

    def generate_setting(self):
        if not hasattr(self, "setting"):
            info = self.get_info()
            if info["fabric_version"]:
                self.DEFAULT_SETTING["logo"]["value"] = ":/Image/fabric.png"
            elif info["forge_version"]:
                self.DEFAULT_SETTING["logo"]["value"] = ":/Image/forge.png"
            else:
                self.DEFAULT_SETTING["logo"]["value"] = ":/Image/grass.png"

            self.setting = Setting(os.path.join(
                self.directory, "versions", self.name, "FMCL", "setting.json"))
            self.setting.addSetting(self.DEFAULT_SETTING)

    def delete(self):
        shutil.rmtree(os.path.join(self.directory, "versions", self.name))

    def get_pixmap(self):
        self.generate_setting()
        return QPixmap(self.setting.get("logo"))

    def get_icon(self):
        self.generate_setting()
        return QIcon(self.setting.get("logo"))
