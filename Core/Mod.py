import os
import json
import requests
from Core import CoreBase
from Core.Download import download
import Globals as g


class Mod(CoreBase):
    def __init__(self, name="", info={}, path="") -> None:
        super().__init__()
        self.name = name
        self.info = info
        self.path = path

    def search_mod(self, index="relevance", limit=100) -> list[dict]:
        '''搜索模组'''
        query = self.name
        g.logapi.info(f"搜索模组:{query}")
        url = f"https://api.modrinth.com/v2/search?query={query}&limit={limit}&index={index}"
        r = requests.get(url)
        result = []
        for i in json.loads(r.content)["hits"]:
            result.append(i)
        return result

    def get_mod_files(self) -> list[dict]:
        '''获取模组文件'''
        project_id = self.info["project_id"]
        url = f"https://api.modrinth.com/v2/project/{project_id}/version"
        r = requests.get(url)
        result = []
        for i in json.loads(r.content):
            result.append({
                "name": i["name"],
                "url": i["files"][0]["url"],
                "filename": i["files"][0]["filename"],
                "game_version": i["game_versions"][0],
                "dependencies": i["dependencies"]
            })
        return result

    def get_mod_info(self):
        """获取Mod信息"""
        project_id = self.info["project_id"]
        url = f"https://api.modrinth.com/v2/project/{project_id}"
        r = requests.get(url)
        result = json.loads(r.content)
        result["project_id"] = result["id"]
        return result

    def download_mod_file(self):
        '''下载模组文件'''
        download(self.info["url"], self.path, self)

    def get_mods(self) -> list:
        """获取文件夹下的mod"""
        try:
            os.makedirs(self.path)
        except:
            pass
        result = []
        allmod = 0
        enablemod = 0
        for i in os.listdir(self.path):
            if self.is_mod(i):
                allmod += 1
                if ".disabled" not in i:
                    enablemod += 1
                result.append(i)
        return result, enablemod, allmod

    def is_mod(self, name) -> bool:
        """判断是否是mod"""
        return ".jar" in name or ".disabled" in name

    def endisable_mod(self) -> tuple:
        """启用或禁用mod"""
        result = "disabled"
        if "disabled" in self.name:
            new_name = ".".join(self.name.split(".")[:-1])
            result = "enabled"
        else:
            new_name = self.name+".disabled"
        os.rename(self.path+"/"+self.name, self.path+"/"+new_name)
        return result, new_name

    def del_mod(self):
        os.remove(self.path+"/"+self.name)
