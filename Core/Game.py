import base64
import json
import logging
import os
import shutil
import tempfile
from copy import deepcopy
from zipfile import ZipFile

import minecraft_launcher_lib as mll
import toml
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import qApp
from Setting import Setting

from Core.Download import Download
from Core.Requests import Requests

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
        self.directory = Setting().get("game.directories")[0]

        self.DEFAULT_SETTING_ATTR = {
            "specific": {
                "name": _translate("Game", "特定设置"),
            },
            "isolation": {
                "name": _translate("Game", "版本隔离"),
            },
            "logo": {
                "name":  _translate("Game", "游戏图标"),
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
        dir, command = self.get_launch_command()
        str_command = ""
        for i in command:
            if " " in i:
                str_command += '"'+i+'" '
            else:
                str_command += i+' '
        args = f"cd {dir}&start {str_command}"
        logging.info(args)
        os.popen(args)

    def get_launch_command(self) -> tuple[str, str]:
        """
        获取启动参数
        返回游戏目录和参数
        """
        self.generate_setting()
        absdir = os.path.abspath(self.directory)
        if self.setting.get("specific"):
            setting = self.setting
        else:
            setting = Setting()

        command = []

        cur_user = deepcopy(User.get_cur_user())
        if cur_user["type"] == "authlibInjector":
            logging.info(f"外置登录: {cur_user['mode']}")
            if cur_user["mode"] == "LittleSkin":
                api = "https://authlib-injector.yushi.moe"
                r = Requests.get(f"{api}/artifact/latest.json").json()

                url = r["download_url"]
                tempdir = os.path.join(tempfile.gettempdir(), "FMCL")
                if not os.path.exists(tempdir):
                    os.makedirs(tempdir)
                filename = url.split("/")[-1]
                path = os.path.join(tempdir, filename)
                logging.info(f"下载{url}到{path}")
                Download(url, path, {"setMax": logging.info,
                         "setProgress": logging.info}).check()
                logging.info("下载完成")

                api = "https://littleskin.cn/api/yggdrasil"
                meta = Requests.get(api).content
                metab64 = base64.b64encode(meta)
                metab64 = str(metab64)[2:-1]
                logging.info(f"元数据Base64编码: {metab64}")
                command.append(
                    f"-javaagent:{path}={api}")
                command.append(
                    f"-Dauthlibinjector.yggdrasil.prefetched={metab64}")

        options = cur_user
        options["launcherName"] = "FMCL"
        options["launcherVersion"] = qApp.applicationVersion()
        options["gameDirectory"] = absdir
        options["customResolution"] = True
        options["resolutionWidth"] = str(setting.get("game.width"))
        options["resolutionHeight"] = str(setting.get("game.height"))
        options["executablePath"] = setting.get("game.java_path")
        options["executablePath"] = setting.get("game.java_path")
        options["jvmArguments"] = [f"-Xmx{setting.get('game.maxmem')}m"]
        self.generate_setting()
        if self.setting.get("isolation"):
            options["gameDirectory"] = os.path.abspath(
                os.path.join(self.directory, "versions", self.name))

        _command = mll.command.get_minecraft_command(
            self.name, absdir, options)
        command.insert(0, _command[0])
        command += _command[1:]
        try:
            i = command.index("--versionType")
            command[i+1] = "FMCL"
        except:
            pass

        return options["gameDirectory"], command

    def install_forge(self, forge_version, callback):
        logging.info(f"下载Forge({forge_version})")
        mll.forge.install_forge_version(
            forge_version, self.directory, callback)
        version, forge = forge_version.split("-")
        Game(f"{version}-forge-{forge}").rename(self.name)

    def install_fabric(self, version, fabric_version, callback):
        logging.info(f"下载Fabric({version},{fabric_version})")
        mll.fabric.install_fabric(
            version, self.directory, fabric_version, callback)
        fabric_minecraft_version = f"fabric-loader-{fabric_version}-{version}"
        Game(fabric_minecraft_version).rename(self.name)

    def install_mc(self, version, callback):
        logging.info(f"下载Minecraft({version})")
        mll.install.install_minecraft_version(
            version, self.directory, callback)
        Game(version).rename(self.name)

    def install(self, version, forge_version, fabric_version):
        logging.info(f"下载({version},{forge_version},{fabric_version})")
        if forge_version:
            Progress().add(_translate("Game", "下载")+self.name,
                           lambda callback: self.install_forge(forge_version, callback))
        elif fabric_version:
            Progress().add(_translate("Game", "下载")+self.name,
                           lambda callback: self.install_fabric(version, fabric_version, callback))
        else:
            Progress().add(_translate("Game", "下载")+self.name,
                           lambda callback: self.install_mc(version, callback))

    def rename(self, new_name):
        if new_name == self.name:
            return
        logging.info(f"重命名: {new_name}")
        old_path = f"{self.directory}/versions/{self.name}"
        new_path = f"{self.directory}/versions/{new_name}"
        if os.path.exists(new_path):  # 如果重命名之后的文件存在就覆盖原来的文件
            # 移动新的文件
            shutil.copy(f"{old_path}/{self.name}.jar", new_path)
            shutil.copy(f"{old_path}/{self.name}.json", new_path)
            # 删除旧的文件
            os.remove(f"{new_path}/{new_name}.jar")
            os.remove(f"{new_path}/{new_name}.json")

            # 重命名
            os.rename(f"{new_path}/{self.name}.jar",
                      f"{new_path}/{new_name}.jar")
            os.rename(f"{new_path}/{self.name}.json",
                      f"{new_path}/{new_name}.json")

            config = json.load(
                open(f"{new_path}/{new_name}.json"))
            config["id"] = new_name
            json.dump(config,
                      open(f"{new_path}/{new_name}.json", mode="w", encoding="utf-8"))
            return
        os.rename(f"{old_path}/{self.name}.jar",
                  f"{old_path}/{new_name}.jar")
        os.rename(f"{old_path}/{self.name}.json",
                  f"{old_path}/{new_name}.json")
        os.rename(old_path, new_path)
        config = json.load(
            open(f"{new_path}/{new_name}.json"))
        config["id"] = new_name
        json.dump(config,
                  open(f"{new_path}/{new_name}.json", mode="w", encoding="utf-8"))

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

    def get_mods(self, keyword="") -> list[tuple[bool, str]]:
        """获取Mod

        Args:
            keyword (str): 查找关键字. Defaults to "".

        Returns:
            list[tuple[bool,str]]: Mod列表, 每个元组的第一个元素代表是否启用, 第二个元素代表Mod名称
        """
        if not self.mod_avaiable():
            return []
        path = self.get_mod_path()
        if not os.path.exists(path):
            return []
        result = []
        for i in os.listdir(path):
            if keyword not in i:
                continue
            if ".jar" in i:
                if i.endswith(".disabled"):
                    result.append((False, i.replace(".disabled", "")))
                elif i.endswith(".jar"):
                    result.append((True, i))
        return result

    def open_directory(self):
        os.startfile(os.path.join(self.directory, "versions", self.name))

    def setModEnabled(self, enabled: bool, names: str | list):
        """
        设置Mod启用/禁用
        names不包含文件最后的.disabled
        """
        if isinstance(names, str):
            names = [names]
        path = self.get_mod_path()
        for name in names:
            enabled_path = os.path.join(path, name)
            disabled_path = os.path.join(path, f"{name}.disabled")
            if enabled:
                if os.path.exists(disabled_path):  # 防止重复设置
                    os.rename(disabled_path, enabled_path)
            else:
                if os.path.exists(enabled_path):
                    os.rename(enabled_path, disabled_path)

    def deleteMods(self, mods: list | str):
        """
        modss包含文件最后的.disabled
        """
        if isinstance(mods, str):
            mods = [mods]
        path = self.get_mod_path()
        for mod in mods:
            p = os.path.join(path, mod)
            if os.path.exists(p):
                os.remove(p)
                logging.info(f"删除{p}")

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

            # 保证当不启用特定设置时与全局设置相同
            if not self.setting.get("specific"):
                globalsetting = Setting()
                for key, val in globalsetting.items():
                    if "game" in key:
                        self.setting[key] = val
                for key, val in globalsetting.attrs.items():
                    if "game" in key:
                        self.setting.attrs[key] = val

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
