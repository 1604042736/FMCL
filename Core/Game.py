import json
import logging
import os
import shutil
from zipfile import ZipFile

import minecraft_launcher_lib as mll
import toml
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import qApp
from Setting import Setting

from .Progress import Progress
from .User import User


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
        self.directory = Setting().get("game.directories")[0]

        self.DEFAULT_SETTING_ATTR = {
            "specific": {
                "name": "特定设置",
            },
            "isolation": {
                "name": "版本隔离",
            },
            "logo": {
                "name":  "游戏图标",
            }
        }
        self.DEFAULT_SETTING = {
            "specific": False,
            "isolation": False,
            "logo": ""
        }

        globalsetting = Setting()
        for key, val in globalsetting.items():
            if "game" in key:
                self.DEFAULT_SETTING[key] = val
        for key, val in globalsetting.attrs.items():
            if "game" in key:
                self.DEFAULT_SETTING_ATTR[key] = val

    def launch(self):
        self.generate_setting()
        absdir = os.path.abspath(self.directory)
        if self.setting.get("specific"):
            setting = self.setting
        else:
            setting = Setting()

        options = User.get_cur_user()
        options["launcherName"] = "FMCL"
        options["launcherVersion"] = qApp.applicationVersion()
        options["gameDirectory"] = absdir
        options["customResolution"] = True
        options["resolutionWidth"] = str(setting.get("game.width"))
        options["resolutionHeight"] = str(setting.get("game.height"))
        options["executablePath"] = setting.get("game.java_path")
        self.generate_setting()
        if self.setting.get("isolation"):
            options["gameDirectory"] = os.path.abspath(
                os.path.join(self.directory, "versions", self.name))

        command = mll.command.get_minecraft_command(self.name, absdir, options)

        str_command = ""
        for i in command:
            if " " in i:
                str_command += '"'+i+'" '
            else:
                str_command += i+' '
        args = f"cd {self.directory}&start {str_command}"
        logging.info(args)
        os.popen(args)

    def install_forge(self, forge_version, callback):
        mll.forge.install_forge_version(
            forge_version, self.directory, callback)
        version, forge = forge_version.split("-")
        Game(f"{version}-forge-{forge}").rename(self.name)

    def install_fabric(self, version, fabric_version, callback):
        mll.fabric.install_fabric(
            version, self.directory, fabric_version, callback)
        fabric_minecraft_version = f"fabric-loader-{fabric_version}-{version}"
        Game(fabric_minecraft_version).rename(self.name)

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
        config = json.load(
            open(f"{self.directory}/versions/{self.name}/{self.name}.json"))
        config["id"] = new_name
        json.dump(config,
                  open(f"{self.directory}/versions/{self.name}/{self.name}.json", mode="w", encoding="utf-8"))
        os.rename(f"{self.directory}/versions/{self.name}/{self.name}.jar",
                  f"{self.directory}/versions/{self.name}/{new_name}.jar")
        os.rename(f"{self.directory}/versions/{self.name}/{self.name}.json",
                  f"{self.directory}/versions/{self.name}/{new_name}.json")
        os.rename(f"{self.directory}/versions/{self.name}",
                  f"{self.directory}/versions/{new_name}")

    def get_info(self) -> dict:
        if hasattr(self, "info"):
            return self.info
        self.info = info = {
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
        elif "inheritsFrom" in config:
            info["version"] = config["inheritsFrom"]
        else:
            info["version"] = config["id"]
        return info

    def get_mod_path(self):
        self.generate_setting()
        if self.setting.get("isolation"):
            path = os.path.join(self.directory, "versions", self.name, "mods")
        else:
            path = os.path.join(self.directory, "mods")
        return path

    def mod_avaiable(self):
        self.get_info()
        return self.info["forge_version"] or self.info["fabric_version"]

    def get_mods(self) -> list:
        if not self.mod_avaiable():
            return []
        path = self.get_mod_path()
        if not os.path.exists(path):
            return []
        result = []
        for i in os.listdir(path):
            if ".jar" in i:
                if i.endswith(".disabled"):
                    result.append((False, i.replace(".disabled", "")))
                elif i.endswith(".jar"):
                    result.append((True, i))
        return result

    def open_directory(self):
        os.startfile(os.path.join(self.directory, "versions", self.name))

    def setModEnabled(self, enabled: bool, name: str):
        path = self.get_mod_path()
        enabled_path = os.path.join(path, name)
        disabled_path = os.path.join(path, f"{name}.disbaled")
        if enabled:
            os.rename(disabled_path, enabled_path)
        else:
            os.rename(enabled_path, disabled_path)

    def generate_setting(self):
        if not hasattr(self, "setting"):
            info = self.get_info()
            if info["fabric_version"]:
                self.DEFAULT_SETTING["logo"] = ":/Image/fabric.png"
            elif info["forge_version"]:
                self.DEFAULT_SETTING["logo"] = ":/Image/forge.png"
            else:
                self.DEFAULT_SETTING["logo"] = ":/Image/grass.png"

            self.setting = Setting(os.path.join(
                self.directory, "versions", self.name, "FMCL", "setting.json"))
            self.setting.add(self.DEFAULT_SETTING)
            self.setting.addAttr(self.DEFAULT_SETTING_ATTR)

    def delete(self):
        shutil.rmtree(os.path.join(self.directory, "versions", self.name))

    def get_pixmap(self):
        self.generate_setting()
        return QPixmap(self.setting.get("logo"))

    def get_icon(self):
        self.generate_setting()
        return QIcon(self.setting.get("logo"))

    def get_mod_info(self, mod_name: str, enabled=True) -> list:
        path = self.get_mod_path()
        if not enabled:
            mod_name = mod_name+".disabled"
        mod_path = os.path.join(path, mod_name)

        info = {
            "name": "",
            "description": "",
            "version": "",
            "authors": []
        }

        zipfile = ZipFile(mod_path)
        for zipinfo in zipfile.filelist:
            if "fabric.mod.json" == zipinfo.filename:
                config = json.loads(zipfile.open("fabric.mod.json").read())
                info["name"] = config["name"]
                info["description"] = config.get("description", "")
                info["version"] = config["version"]
                for i in config.get("authors", [])+config.get("contributors", []):
                    if isinstance(i, dict):
                        info["authors"].append(i["name"])
                    else:
                        info["authors"].append(i)
                break
            elif "mods.toml" in zipinfo.filename:
                config = toml.loads(zipfile.open(
                    zipinfo.filename).read().decode("utf-8"))
                info["name"] = config["mods"][0]["displayName"]
                info["version"] = config["mods"][0]["version"]
                info["description"] = config["mods"][0].get("description", "")
                try:
                    info["authors"] = [config["mods"][0]["authors"]]
                except KeyError:
                    info["authors"] = [config.get("authors", "")]

                if "${file.jarVersion}" in info["version"]:
                    MANIFESTMF = zipfile.open(
                        "META-INF/MANIFEST.MF").read().decode("utf-8").split("\n")
                    for i in MANIFESTMF:
                        if "Implementation-Version" in i:
                            info["version"] = info["version"].replace(
                                "${file.jarVersion}", i.split(":")[-1].strip())
                            break
                break
        return info
