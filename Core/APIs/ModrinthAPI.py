"""
参考https://docs.modrinth.com/
"""

from datetime import datetime
import json
import logging
import os
from typing import TypedDict, Literal
from zipfile import ZipFile

from PyQt5.QtCore import QCoreApplication

from Core.Network import Network
from Core.Download import Download
from Core.Task import Task
from Core.Installer import Installer

_translate = QCoreApplication.translate

MAX_POOL_SIZE = 10


def empty(*args):
    pass


class ModrinthProjectDonationURL(TypedDict):
    id: str
    platform: str
    url: str


class ModrinthProjectLicense(TypedDict):
    id: str
    name: str
    url: str | None


class ModrinthGalleryImage(TypedDict, total=False):
    url: str  # required
    featured: bool  # required
    title: str | None
    description: str
    created: str  # required ISO-8601
    ordering: int


class ModrinthProjectModel(TypedDict, total=False):
    slug: str  # required
    title: str  # required
    description: str  # required
    categories: list[str]  # required
    client_side: Literal["required", "optional", "unsupported"]  # required
    server_side: Literal["required", "optional", "unsupported"]  # required
    body: str  # required
    status: Literal[
        "approved",
        "archived",
        "rejected",
        "draft",
        "unlisted",
        "processing",
        "withheld",
        "scheduled",
        "private",
        "unknown",
    ]  # required
    requested_status: (
        None | Literal["approved", "archived", "unlisted", "private", "draft"]
    )
    additional_categories: list[str]
    issues_url: str | None
    source_url: str | None
    wiki_url: str | None
    discord_url: str | None
    donation_urls: list[ModrinthProjectDonationURL]
    project_type: Literal["mod", "modpack", "resourcepack", "shader"]  # required
    downloads: int  # required
    icon_url: str | None
    color: int | None
    thread_id: str
    monetization_status: Literal["monetized", "demonetized", "force-demonetized"]
    id: str  # required
    team: str  # required
    published: str  # required ISO-8601
    updated: str  # required ISO-8601
    approved: str | None  # ISO-8601
    queued: str | None  # ISO-8601
    followers: int  # required
    license: list[ModrinthProjectLicense]
    versions: list[str]
    game_versions: list[str]
    loaders: list[str]
    gallery: list[ModrinthGalleryImage]


class ModrinthSearchResultModel(TypedDict, total=False):
    slug: str  # required
    title: str  # required
    description: str  # required
    categories: list[str]
    client_side: Literal["required", "optional", "unsupported"]  # required
    server_side: Literal["required", "optional", "unsupported"]  # required
    project_type: Literal["mod", "modpack", "resourcepack", "shader"]  # required
    downloads: int  # required
    icon_url: str | None
    color: int | None
    thread_id: str
    monetization_status: Literal["monetized", "demonetized", "force-demonetized"]
    project_id: str  # required
    author: str  # required
    display_categories: list[str]
    versions: list[str]  # required
    follows: int  # required
    date_created: str  # required ISO-8601
    date_modified: str  # required ISO-8601
    latest_version: str
    license: str  # required
    gallery: list[str]
    featured_gallery: str | None


class ModrinthVersionDependency(TypedDict, total=False):
    version_id: str | None
    project_id: str | None
    file_name: str | None
    dependency_type: Literal[
        "required", "optional", "incompatible", "embedded"
    ]  # required


class ModrinthVersionFileHashes(TypedDict):
    sha512: str
    sha1: str


class ModrinthVersionFile(TypedDict, total=False):
    hashes: ModrinthVersionFileHashes  # required
    url: str  # required
    filename: str  # required
    primary: bool  # required
    size: int  # required
    file_type: None | Literal["required-resource-pack", "optional-resource-pack"]


class ModrinthVersionModel(TypedDict, total=False):
    name: str  # required
    version_number: str  # required
    changelog: str | None
    dependencies: list[ModrinthVersionDependency]
    game_versions: list[str]  # required
    version_type: Literal["release", "beta", "alpha"]  # required
    loaders: list[str]  # required
    featured: bool  # required
    status: Literal["listed", "archived", "draft", "unlisted", "scheduled", "unknown"]
    requested_status: None | Literal["listed", "archived", "draft", "unlisted"]
    id: str  # required
    project_id: str  # required
    author_id: str  # required
    date_published: str  # required ISO-8601
    downloads: int  # required
    files: list[ModrinthVersionFile]  # required


class ModrinthSearchResponse(TypedDict):
    hits: list[ModrinthSearchResultModel]
    offset: int
    limit: int
    total_hits: int

    error: str
    description: str


class ModrinthModpackFile(TypedDict):
    path: str
    hashes: dict  # sha1 sha512
    downloads: list[str]
    fileSize: int


class ModrinthModpack(TypedDict):
    formatVersion: str
    game: str
    versionId: str
    name: str
    summary: str
    files: list[ModrinthModpackFile]
    dependencies: dict


def memory(func):
    """记忆"""
    cache = {}

    def wrapper(*args, **kwargs):
        _hash = (args, tuple(kwargs.keys()), tuple(kwargs.values()))
        if _hash not in cache:
            cache[_hash] = func(*args, **kwargs)
        return cache[_hash]

    return wrapper


class ModrinthAPI:
    BASE_URL = "https://api.modrinth.com/v2"

    def __init__(self, network=None) -> None:
        self.network = network if network != None else Network()

    @memory
    def search(
        self,
        query: str,
        facets: str = "",
        index: Literal[
            "relevance", "downloads", "follows", "newest", "updated"
        ] = "relevance",
        offset: int = 0,
        limit: int = 100,
    ) -> list[ModrinthSearchResultModel]:
        url = f"{self.BASE_URL}/search?query={query}&index={index}&{offset=}&{limit=}"
        if facets:
            url += f"&facets={facets}"
        r: ModrinthSearchResponse = self.network.get(url).json()
        if "error" in r:
            raise Exception(f'{r["error"]}: {r["description"]}')
        return r["hits"]

    @memory
    def get_project(self, project_id_or_slug: str) -> ModrinthProjectModel:
        url = f"{self.BASE_URL}/project/{project_id_or_slug}"
        r: ModrinthProjectModel = self.network.get(url).json()
        return r

    @memory
    def get_project_versions(
        self,
        project_id_or_slug: str,
        loaders: list[str] = None,
        game_versions: list[str] = None,
        featured: bool = None,
    ) -> list[ModrinthVersionModel]:
        url = f"{self.BASE_URL}/project/{project_id_or_slug}/version"
        args = []
        if loaders != None:
            args.append(str(loaders))
        if game_versions != None:
            args.append(str(game_versions))
        if featured != None:
            args.append(str(featured).lower())
        url += "?" + "&".join(args)
        r: list[ModrinthVersionModel] = self.network.get(url).json()
        return r

    @memory
    def get_version(self, id: str) -> ModrinthVersionModel:
        url = f"{self.BASE_URL}/version/{id}"
        r: ModrinthVersionModel = self.network.get(url).json()
        return r

    def get_translations(self):
        return {
            "release": _translate("ModrinthAPI", "正式版"),
            "beta": _translate("ModrinthAPI", "测试版"),
            "alpha": _translate("ModrinthAPI", "预览版"),
            "required": _translate("ModrinthAPI", "必需"),
            "optional": _translate("ModrinthAPI", "可选"),
            "adventure": _translate("ModrinthAPI", "冒险"),
            "cursed": _translate("ModrinthAPI", "杂项"),
            "decoration": _translate("ModrinthAPI", "装饰"),
            "economy": _translate("ModrinthAPI", "经济"),
            "equipment": _translate("ModrinthAPI", "装备"),
            "food": _translate("ModrinthAPI", "食物"),
            "game-mechanics": _translate("ModrinthAPI", "游戏机制"),
            "library": _translate("ModrinthAPI", "支持库"),
            "magic": _translate("ModrinthAPI", "魔法"),
            "management": _translate("ModrinthAPI", "改良"),
            "minigame": _translate("ModrinthAPI", "迷你游戏"),
            "mobs": _translate("ModrinthAPI", "生物"),
            "optimization": _translate("ModrinthAPI", "优化"),
            "social": _translate("ModrinthAPI", "社交"),
            "storage": _translate("ModrinthAPI", "存储"),
            "technology": _translate("ModrinthAPI", "科技"),
            "transportation": _translate("ModrinthAPI", "运输"),
            "utility": _translate("ModrinthAPI", "实用"),
            "worldgen": _translate("ModrinthAPI", "世界生成"),
            "lightweight": _translate("ModrinthAPI", "轻量"),
            "multiplayer": _translate("ModrinthAPI", "多人游戏"),
            "combat": _translate("ModrinthAPI", "战斗"),
            "challenging": _translate("ModrinthAPI", "挑战"),
            "relevance": _translate("ModrinthAPI", "按匹配程度排序"),
            "downloads": _translate("ModrinthAPI", "按下载量排序"),
            "follows": _translate("ModrinthAPI", "按关注者数量排序"),
            "newest": _translate("ModrinthAPI", "按创建时间排序"),
            "updated": _translate("ModrinthAPI", "按更新时间排序"),
            "mod": _translate("ModrinthAPI", "模组"),
            "modpack": _translate("ModrinthAPI", "整合包"),
            "resourcepack": _translate("ModrinthAPI", "资源包"),
            "shader": _translate("ModrinthAPI", "光影"),
            "release": _translate("ModrinthAPI", "正式版"),
        }

    def get_sortby(self):
        return ["relevance", "downloads", "follows", "newest", "updated"]

    def get_categories(self):
        return [
            "adventure",
            "cursed",
            "decoration",
            "economy",
            "equipment",
            "food",
            "game-mechanics",
            "library",
            "magic",
            "management",
            "minigame",
            "mobs",
            "optimization",
            "social",
            "storage",
            "technology",
            "transportation",
            "utility",
            "worldgen",
        ]

    def get_types(self):
        return ["mod", "modpack", "resourcepack", "shader"]

    def get_time(self, time_iso8601: str):
        """转换ISO8601日期格式"""
        return datetime.strptime(time_iso8601, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
            "%Y-%m-%d"
        )

    def get_primary_file(self, version: ModrinthVersionModel) -> ModrinthVersionFile:
        for file in version["files"]:
            if file["primary"] == True:
                return file
        return version["files"][0]

    def install_modpack(self, filepath, version, callback=None):
        from Core.Version import Version

        Installer().install_mrpack(
            filepath,
            version.directory,
            os.path.join(version.directory, "versions", version.name),
            callback
            | {
                "rename": lambda name: Version(name).rename(version.name)
            },  # 任务会下载原版, 需要重命名
        )
