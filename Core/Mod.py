import logging
import os
import traceback
import toml
import json
from zipfile import ZipFile

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap, QImage

from .Requests import Requests

_translate = QCoreApplication.translate


class Mod:
    project_cache = {}

    def __init__(self, path="") -> None:
        self.downloadsource = "Modrinth"

        self.MODRINTH_SORTMETHOD = {
            _translate("Mod", "按匹配程度排序"): "relevance",
            _translate("Mod", "按下载量排序"): "downloads",
            _translate("Mod", "按关注者数量排序"): "follows",
            _translate("Mod", "按创建时间排序"): "newest",
            _translate("Mod", "按更新时间排序"): "updated",
        }

        self.path = path
        self.set_names()

    def set_names(self):
        """根据self.path设置一些名称"""
        self.dirname = os.path.dirname(self.path)
        self.basename = os.path.basename(self.path)
        if self.basename.endswith(".disabled"):
            self.enabled = False
            self.name = self.basename.replace(".disabled", "")
        else:
            self.enabled = True
            self.name = self.basename

    def set_enabled(self, enabled: bool):
        enabled_path = os.path.join(self.dirname, self.name)
        disabled_path = os.path.join(self.dirname, f"{self.name}.disabled")
        logging.debug(f"{enabled=}, {enabled_path=}, {disabled_path=}")
        if enabled:
            if os.path.exists(disabled_path):  # 防止重复设置
                os.rename(disabled_path, enabled_path)
            self.path = enabled_path
        else:
            if os.path.exists(enabled_path):
                os.rename(enabled_path, disabled_path)
            self.path = disabled_path
        self.set_names()

    def delete(self):
        os.remove(self.path)

    def get_info(self) -> list:
        def adjust(content: str | bytes):
            """调整文件内容来保证能够正常解析"""
            if isinstance(content, bytes):
                content = content.decode(errors="ignore")
            in_str = False  # 判断是否进入文本中的字符串中
            new_content = ""
            for i in content:
                if in_str:
                    if i == "\\":  # 防止把'\'变成两个'\\'
                        new_content += "\\"
                    else:
                        new_content += repr(i)[1:-1]
                else:
                    new_content += i
                if i == '"':
                    in_str = not in_str
            return new_content

        mod_path = self.path

        info = {
            "name": "",
            "description": "",
            "version": "",
            "authors": [],
            "url": "",
            "icon": None,
        }
        # 很多时侯报错是由于多行字符串
        zipfile = ZipFile(mod_path)
        for zipinfo in zipfile.filelist:
            if (
                "icon.png" in zipinfo.filename
                or "logo.png" in zipinfo.filename  # 有这些名称的可能是图标
                or (
                    zipinfo.filename.endswith(".png") and "/" not in zipinfo.filename
                )  # 在根目录下的图片可能是图标
            ):
                info["icon"] = QPixmap.fromImage(
                    QImage.fromData(zipfile.open(zipinfo.filename).read())
                )
            elif "fabric.mod.json" == zipinfo.filename:
                try:
                    config = json.loads(adjust(zipfile.open(zipinfo.filename).read()))
                    info["name"] = config["name"]
                    info["description"] = config.get("description", "")
                    info["version"] = config["version"]
                    for i in config.get("authors", []) + config.get("contributors", []):
                        if isinstance(i, dict):
                            info["authors"].append(i["name"])
                        else:
                            info["authors"].append(i)
                    if "contact" in config and "homepage" in config["contact"]:
                        info["url"] = config["contact"]["homepage"]
                except:
                    logging.error(
                        f"{self.name}: 从{zipinfo.filename}中获取模组信息失败:\n{traceback.format_exc()}"
                    )
            elif "mods.toml" in zipinfo.filename:
                try:
                    config = toml.loads(adjust(zipfile.open(zipinfo.filename).read()))
                    info["name"] = config["mods"][0]["displayName"]
                    info["version"] = config["mods"][0]["version"]
                    info["description"] = config["mods"][0].get("description", "")
                    try:
                        info["authors"] = [config["mods"][0]["authors"]]
                    except KeyError:
                        info["authors"] = [config.get("authors", "")]

                    info["url"] = config["mods"][0].get("displayURL", "")

                    if "${file.jarVersion}" in info["version"]:
                        MANIFESTMF = (
                            zipfile.open("META-INF/MANIFEST.MF")
                            .read()
                            .decode("utf-8")
                            .split("\n")
                        )
                        for i in MANIFESTMF:
                            if "Implementation-Version" in i:
                                info["version"] = info["version"].replace(
                                    "${file.jarVersion}", i.split(":")[-1].strip()
                                )
                                break
                except:
                    logging.error(
                        f"{self.name}: 从{zipinfo.filename}中获取模组信息失败:\n{traceback.format_exc()}"
                    )
            elif ".info" in zipinfo.filename:
                try:
                    config = json.loads(adjust(zipfile.open(zipinfo.filename).read()))
                    if isinstance(config, list):
                        config = config[0]
                    else:
                        config = config["modList"][0]
                    info["name"] = config.get("name", "")
                    info["version"] = config.get("version", "")
                    info["description"] = config.get("description", "")
                    if "authorList" in config:
                        info["authors"] = config["authorList"]
                    elif "authors" in config:
                        info["authors"] = config["authors"]
                    info["url"] = config.get("url", "")
                except:
                    logging.error(
                        f"{self.name}: 从{zipinfo.filename}中获取模组信息失败:\n{traceback.format_exc()}"
                    )
        return info

    def search(self, name, sort="", yield_=False):
        if sort:
            sort = self.get_sortmethod(sort)
        else:
            sort = "relevance"
        if self.downloadsource == "Modrinth":
            if not yield_:
                return [i for i in self.search_modrinth_yield(name, sort)]
            else:
                for i in self.search_modrinth_yield(name, sort):
                    yield i

    def search_modrinth_yield(self, name, sort):
        url = f"https://api.modrinth.com/v2/search?query={name}&index={sort}&limit=100"
        r = Requests.get(url, try_time=-1, timeout=5).json()
        for i in r["hits"]:
            yield self.get_modrinth_modinfo(i["project_id"])

    def get_modrinth_modinfo(self, project_id):
        if project_id in Mod.project_cache:
            return Mod.project_cache[project_id]
        result = {
            "icon_url": "",
            "title": "",
            "description": "",
            "project_id": project_id,
            "files": {},
            "dependencies": [],
        }
        url = f"https://api.modrinth.com/v2/project/{project_id}"
        r = Requests.get(url, try_time=-1, timeout=5).json()
        result["icon_url"] = r["icon_url"]
        result["title"] = r["title"]
        result["description"] = r["description"]

        url = f"https://api.modrinth.com/v2/project/{project_id}/version"
        r = Requests.get(url, try_time=-1, timeout=5).json()
        dependencies_id = []
        for version in r:
            for file in version["files"]:
                for game_version in version["game_versions"]:
                    if game_version not in result["files"]:
                        result["files"][game_version] = {}
                    result["files"][game_version][file["filename"]] = file

            for dependence in version["dependencies"]:
                if (
                    dependence["project_id"]
                    and dependence["project_id"] not in dependencies_id
                ):
                    result["dependencies"].append(
                        self.get_modrinth_modinfo(dependence["project_id"])
                    )
                    dependencies_id.append(dependence["project_id"])
        Mod.project_cache[project_id] = result
        return result

    def get_all_downloadsources(self) -> list[str]:
        return ["Modrinth"]

    def get_all_sortmethod(self) -> list[str]:
        if self.downloadsource == "Modrinth":
            return self.MODRINTH_SORTMETHOD.keys()

    def get_sortmethod(self, sort):
        if self.downloadsource == "Modrinth":
            return self.MODRINTH_SORTMETHOD[sort]

    def set_downloadsource(self, ds):
        self.downloadsource = ds

    def __repr__(self) -> str:
        if self.path:
            return self.name
        return super().__repr__()
