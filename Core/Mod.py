from datetime import datetime
import logging
import os
import traceback
from typing import TypedDict
import toml
import json
from zipfile import ZipFile

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap, QImage

from Core.Network import Network

_translate = QCoreApplication.translate


class ApiModInfo(TypedDict):
    """Api模组信息"""

    api_name: str  # API名称

    client_side: str  # 对客户端要求
    server_side: str  # 对服务端要求
    game_versions: list[str]  # 游戏版本
    id: str
    title: str
    description: str
    updated: str  # 更新日期
    downloads: int  # 下载量
    categories: list[str]  # 分类
    loaders: list[str]  # 加载器
    icon_url: str  # 图标网址
    issues_url: str  # 反馈网址
    source_url: str  # 源码网址
    wiki_url: str  # Wiki网址


class Dependency(TypedDict):
    """依赖"""

    project_id: str
    dependency_type: str


class FileInfo(TypedDict):
    """模组文件信息"""

    url: str
    filename: str


class VersionInfo(TypedDict):
    """模组版本信息"""

    game_versions: str  # 游戏版本
    loaders: str  # 加载器
    id: str
    name: str
    version_number: str
    date_published: str  # 发布日期
    downloads: str  # 下载量
    version_type: str  # 版本类型
    files: list[FileInfo]  # 文件
    dependencies: list[Dependency]  # 依赖


class Mod:
    project_cache = {}

    @staticmethod
    def get_time(utc_time):
        update_time = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        return update_time.strftime("%Y-%m-%d")

    def __init__(self, path="") -> None:
        self.downloadsource = "Modrinth"

        self.MODRINTH_SORTMETHOD = {
            _translate("Mod", "按匹配程度排序"): "relevance",
            _translate("Mod", "按下载量排序"): "downloads",
            _translate("Mod", "按关注者数量排序"): "follows",
            _translate("Mod", "按创建时间排序"): "newest",
            _translate("Mod", "按更新时间排序"): "updated",
        }

        self.tr_categories = {
            "adventure": _translate("Mod", "冒险"),
            "cursed": _translate("Mod", "杂项"),
            "decoration": _translate("Mod", "装饰"),
            "economy": _translate("Mod", "经济"),
            "equipment": _translate("Mod", "装备"),
            "food": _translate("Mod", "食物"),
            "game-mechanics": _translate("Mod", "游戏机制"),
            "library": _translate("Mod", "支持库"),
            "magic": _translate("Mod", "魔法"),
            "management": _translate("Mod", "改良"),
            "minigame": _translate("Mod", "迷你游戏"),
            "mobs": _translate("Mod", "生物"),
            "optimization": _translate("Mod", "优化"),
            "social": _translate("Mod", "社交"),
            "storage": _translate("Mod", "存储"),
            "technology": _translate("Mod", "科技"),
            "transportation": _translate("Mod", "运输"),
            "utility": _translate("Mod", "实用"),
            "worldgen": _translate("Mod", "世界生成"),
        }

        self.tr_versiontype = {
            "release": _translate("Mod", "正式版"),
            "beta": _translate("Mod", "测试版"),
        }

        self.tr_dependencytype = {
            "required": _translate("Mod", "必需"),
            "optional": _translate("Mod", "可选"),
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
                return [i for i in self.search_modrinth_iter(name, sort)]
            else:
                for i in self.search_modrinth_iter(name, sort):
                    yield i

    def search_modrinth_iter(self, name, sort):
        url = f"https://api.modrinth.com/v2/search?query={name}&index={sort}&limit=100"
        r = Network().get(url).json()
        for i in r["hits"]:
            yield self.get_modrinth_modinfo(i["project_id"])

    def get_modrinth_modinfo(self, project_id) -> ApiModInfo:
        if project_id in Mod.project_cache:
            return Mod.project_cache[project_id]

        url = f"https://api.modrinth.com/v2/project/{project_id}"
        r: ApiModInfo = Network().get(url).json()
        r["api_name"] = "Modrinth"
        Mod.project_cache[project_id] = r
        return r

    def get_apimodinfo(self, apimodinfo: ApiModInfo, project_id) -> ApiModInfo:
        if apimodinfo["api_name"] == "Modrinth":
            return self.get_modrinth_modinfo(project_id)

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

    def get_mod_versions(self, apimodinfo: ApiModInfo) -> list[VersionInfo]:
        """获得模组的版本"""
        if apimodinfo["api_name"] == "Modrinth":
            return self.get_modrinth_modversions(apimodinfo)
        return []

    def get_modrinth_modversions(self, apimodinfo: ApiModInfo) -> list[VersionInfo]:
        url = f"https://api.modrinth.com/v2/project/{apimodinfo['id']}/version"
        r: list[VersionInfo] = Network().get(url).json()
        return r

    def __repr__(self) -> str:
        if self.path:
            return f"Mod({self.name})"
        return super().__repr__()
