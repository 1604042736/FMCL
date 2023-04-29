from Kernel import Kernel

from .Requests import Requests

_translate = Kernel.translate


class Mod:
    project_cache = {}

    def __init__(self) -> None:
        self.downloadsource = "Modrinth"

        self.MODRINTH_SORTMETHOD = {
            _translate("按匹配程度排序"): "relevance",
            _translate("按下载量排序"): "downloads",
            _translate("按关注者数量排序"): "follows",
            _translate("按创建时间排序"): "newest",
            _translate("按更新时间排序"): "updated",
        }

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
            "dependencies": []
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
                if dependence["project_id"] and dependence["project_id"] not in dependencies_id:
                    result["dependencies"].append(
                        self.get_modrinth_modinfo(dependence["project_id"]))
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
