import shutil
import requests
import json
from Core import CoreBase
from Core.Download import download
import Globals as g
import os
from zipfile import *


class Game(CoreBase):
    def get_versions(self) -> list:
        '''获取游戏版本'''
        url = 'http://launchermeta.mojang.com/mc/game/version_manifest.json'
        r = requests.get(url)
        versions = []
        for version in json.loads(r.content)['versions']:
            versions.append(version['id'])
        return versions

    def get_forge(self, version) -> list:
        '''获取forge版本'''
        url = f'https://bmclapi2.bangbang93.com/forge/minecraft/{version}'
        r = requests.get(url)
        forges = []
        for forge in json.loads(r.content):
            forges.append(forge['version'])
        return forges

    def get_fabric(self, version) -> list:
        url = f"https://meta.fabricmc.net/v1/versions/loader/{version}"
        r = requests.get(url)
        fabrics = []
        for fabric in json.loads(r.content):
            fabrics.append(fabric["loader"]["version"])
        return fabrics

    def get_optifine(self, version) -> list:
        '''获取optifine版本'''
        url = f'https://bmclapi2.bangbang93.com/optifine/{version}'
        r = requests.get(url)
        optifines = []
        for optifine in json.loads(r.content):
            optifines.append(
                optifine['mcversion'] + ' ' + optifine['type'] + ' ' + optifine['patch'])
        return optifines

    def get_liteloader(self, version) -> list:
        '''获取liteloader版本'''
        url = f'https://bmclapi2.bangbang93.com/liteloader/list?mcversion={version}'
        r = requests.get(url)
        liteloaders = []
        try:
            liteloaders.append(json.loads(r.content)[
                               'mcversion'] + ' ' + json.loads(r.content)['version'])
        except:
            pass
        return liteloaders

    def __init__(self, name="", version="", forge_version="", fabric_version="", optifine_version="") -> None:
        super().__init__()
        self.name = name
        self.version = version
        self.forge_version = forge_version
        self.fabric_version = fabric_version
        self.optifine_version = optifine_version
        self.class_path = {}
        self.lib_path = os.path.join(g.cur_gamepath, f'libraries')
        self.version_path = os.path.join(g.cur_gamepath, 'versions')
        self.game_path = os.path.join(self.version_path, self.name)

    def download_version(self):
        '''下载版本'''
        if self.forge_version and self.fabric_version:
            self.Error.emit("Forge和Fabric不兼容")
            return

        info = {
            "name": self.name,
            "version": self.version,
            "forge_version": self.forge_version,
            "fabric_version": self.fabric_version,
            "optifine_version": self.optifine_version
        }
        try:
            os.makedirs(f'{self.game_path}/FMCL')
        except:
            pass
        json.dump(info, open(f'{self.game_path}/FMCL/config.json', mode='w'))

        downloads = [[f'https://bmclapi2.bangbang93.com/version/{self.version}/client', self.game_path + f'\\{self.name}.jar'],
                     [f'https://bmclapi2.bangbang93.com/version/{self.version}/json', self.game_path + f'\\{self.name}.json']]
        if self.forge_version:  # 附带forge
            downloads.append(
                [f'https://bmclapi2.bangbang93.com/maven/net/minecraftforge/forge/{self.version}-{self.forge_version}/forge-{self.version}-{self.forge_version}-installer.jar',
                 self.game_path+f'\\installer.jar'])
            downloads.append(
                [f'https://bmclapi2.bangbang93.com/maven/net/minecraftforge/forge/{self.version}-{self.forge_version}/forge-{self.version}-{self.forge_version}-userdev.jar',
                 self.game_path+f'\\userdev.jar'])
        if self.fabric_version:
            downloads.append([f"https://meta.fabricmc.net/v2/versions/loader/{self.version}/{self.fabric_version}/profile/zip",
                              self.game_path+"/profile.zip"])
        if self.optifine_version:
            mcversion, type_, patch = self.optifine_version.split()
            self.optifine_jar = f"{self.game_path}/Optifine-{mcversion}_{type_}_{patch}.jar"
            downloads.append([f"https://bmclapi2.bangbang93.com/optifine/{mcversion}/{type_}/{patch}",
                              self.optifine_jar])
        for task in downloads:
            download(task[0], task[1], self, True)

        if self.forge_version:
            self.install_forge()
        if self.fabric_version:
            self.install_fabric()
        if self.optifine_version:
            self.install_optifine()

        self.Finished.emit()

    def install_forge(self):
        '''安装forge'''
        config = json.load(
            open(os.path.join(self.game_path, f'{self.name}.json')))

        installerpath = self.game_path+f'\\installer.jar'
        # 获取forge的配置
        zip = ZipFile(installerpath)
        zip.extract('version.json', self.game_path)
        zip.extract('install_profile.json', self.game_path)
        forge_config = json.load(
            open(os.path.join(self.game_path, f'version.json')))

        self.install_profile = json.load(
            open(os.path.join(self.game_path, f'install_profile.json')))

        for i in self.install_profile['libraries']:
            self.analysis_library(i, zip)
        for i in forge_config['libraries']:
            self.analysis_library(i, zip)

        # client
        client_binpatch = self.get_client('BINPATCH')
        zip.extract(client_binpatch[1:], self.game_path)
        client_binpatch = os.path.abspath(self.game_path+f'{client_binpatch}')

        for i in self.install_profile['processors']:
            if "sides" in i and "client" not in i["sides"]:
                continue
            self.execute(i, self.game_path +
                         f'\\{self.name}.jar', client_binpatch)

        zip.close()
        # 拼接
        self.splicing(config, forge_config)
        json.dump(config, open(os.path.join(
            self.game_path, f'{self.name}.json'), mode='w'))

    def get_special_client(self, key):
        '''获取特殊的client'''
        val = self.install_profile["data"][key]["client"]
        a = val[1:-1]
        b, c = a.split(':', 1)
        d = b.replace('.', '/')
        e = '/'.join(c.split(':')[:-1])
        f = c.replace(':', '-').replace('@', '.')
        return os.path.abspath(os.path.join(self.lib_path, d+'/'+e+'/'+f))

    def get_client(self, key):
        '''获取install_profile["data"][key]["client"]'''
        val = self.install_profile["data"][key]["client"]
        if val[0] == '[':
            return os.path.abspath(os.path.join(self.lib_path, self.turn_to_path(val)))
        else:
            return val

    def turn_to_path(self, name):
        '''转换成path'''
        a = name[1:-1]
        b, c = a.split(':', 1)
        d = b.replace('.', '/')
        e = c.replace(':', '-').replace('@', '.')
        return d+'/'+e

    def execute(self, processor, minecraft_jar, binpatch):
        '''执行'''
        args = ''

        args += '-cp '

        classpath = []
        for i in processor['classpath']:
            classpath.append(os.path.abspath(self.class_path[i]))
        classpath.append(os.path.abspath(self.class_path[processor["jar"]]))

        args += '"'+';'.join(classpath)+'" '

        mainclass = ''
        jar = processor['jar']
        if 'installertools' in jar:
            mainclass = 'net.minecraftforge.installertools.ConsoleTool'
        elif 'jarsplitter' in jar:
            mainclass = 'net.minecraftforge.jarsplitter.ConsoleTool'
        elif 'md-5' in jar:
            mainclass = ' net.md_5.specialsource.SpecialSource'
        elif 'binarypatcher' in jar:
            mainclass = 'net.minecraftforge.binarypatcher.ConsoleTool'
        args += mainclass

        for i in processor['args']:
            if i[0] == '[':
                i = os.path.abspath(self.class_path[i[1:-1]])
            args += ' '+i

        for key, val in self.install_profile["data"].items():
            if key == "BINPATCH" or key == "MCP_VERSION":
                continue

            if "@" in val["client"] or "/" in val["client"]:
                client = self.get_client(key)
            elif "_SHA" in key:
                continue
            else:
                client = self.get_special_client(key)+".jar"
            args = args.replace("{%s}" % key, client)

        args = args.replace('{BINPATCH}', binpatch)
        args = args.replace("{ROOT}", g.cur_gamepath)
        args = args.replace("{MINECRAFT_JAR}", minecraft_jar)
        args = args.replace("{SIDE}", "client")

        order = f'java {args}'
        os.system(order)

    def splicing(self, a, b):
        '''拼接a和b'''
        if isinstance(a, list) and isinstance(b, list):
            for i in b:
                if i not in a:
                    a.append(i)
            return
        for key, val in b.items():
            if key not in a:  # a原来没有key
                a[key] = val
            elif isinstance(a[key], str):
                a[key] = val
            else:
                self.splicing(a[key], b[key])  # 继续拼接

    def analysis_library(self, lib, forge_zip=None):
        '''解析lib'''
        if "downloads" in lib:
            path = os.path.join(
                self.lib_path, lib['downloads']['artifact']['path'])
            url = lib['downloads']['artifact']['url']
            self.class_path[lib["name"]] = path
            if url:  # 下载
                download(url, path, self, True)
            else:  # 解压
                path = lib['downloads']['artifact']['path']
                jarpath = 'maven/'+path
                newpath = f'{self.lib_path}/{path}'
                try:
                    os.makedirs(os.path.dirname(newpath))
                except:
                    pass
                forge_zip.extract(jarpath, self.lib_path)
                shutil.move(f'{self.lib_path}/{jarpath}', newpath)
        else:
            name = lib["name"]
            path = self.name_to_path(name)
            url = lib["url"]+path
            download(url, f"{g.cur_gamepath}/libraries/{path}", self, True)

    def name_to_path(self, name):
        """将name转换成path"""
        a, b = name.split(":", 1)
        jar_file = b.replace(":", "-")+".jar"
        return a.replace(".", "/")+"/"+b.replace(":", "/")+"/"+jar_file

    def del_game(self):
        '''删除游戏'''
        shutil.rmtree(self.game_path)

    def install_fabric(self):
        """安装Fabric"""
        name = f"fabric-loader-{self.fabric_version}-{self.version}"

        r = requests.get(
            f"https://meta.fabricmc.net/v2/versions/loader/{self.version}/{self.fabric_version}/profile/json")
        for i in json.loads(r.content)["libraries"]:
            self.analysis_library(i)

        zip = ZipFile(self.game_path+"/profile.zip")
        loader_config = json.loads(zip.read(name+"/"+name+".json"))
        loader_config["id"] = f"{self.version}-Fabric {self.fabric_version}"

        config = json.load(
            open(os.path.join(self.game_path, f'{self.name}.json')))

        self.splicing(config, loader_config)
        json.dump(config, open(os.path.join(
            self.game_path, f'{self.name}.json'), mode='w'))

    def install_optifine(self):
        """安装Optifine"""
        zip = ZipFile(self.optifine_jar)
        launchwrapper_of_version = zip.read(
            "launchwrapper-of.txt").decode("utf-8")
        launchwrapper_of_jar = f"launchwrapper-of-{launchwrapper_of_version}.jar"

        # 生成libraries
        zip.extract(launchwrapper_of_jar,
                    f"{self.lib_path}/optifine/launchwrapper-of/{launchwrapper_of_version}")
        zip.close()
        path = f"{self.lib_path}/optifine/OptiFine/{'_'.join(self.optifine_version.split())}"
        try:
            os.makedirs(path)
        except:
            pass
        shutil.move(self.optifine_jar, path)

        # 生成json
        config = json.load(
            open(os.path.join(self.game_path, f'{self.name}.json')))
        mcversion, type_, patch = self.optifine_version.split()
        optifine_config = {
            "id": f"{mcversion}-Optifine_{type_}_{patch}",
            "inheritsFrom": f"{mcversion}",
            "type": "release",
            "libraries": [
                {
                    "name": f"optifine:OptiFine:{mcversion}_{type_}_{patch}"
                },
                {
                    "name": f"optifine:launchwrapper-of:{launchwrapper_of_version}"
                }
            ],
            "mainClass": "net.minecraft.launchwrapper.Launch",
            "arguments": {
                "game": [
                    "--tweakClass",
                    "optifine.OptiFineTweaker"
                ]
            }
        }
        self.splicing(config, optifine_config)
        json.dump(config, open(os.path.join(
            self.game_path, f'{self.name}.json'), mode='w'))

    def complete_info(self):
        """补全信息"""
        config = json.load(
            open(os.path.join(self.game_path, f'{self.name}.json')))
        info = {
            "name": self.name,
            "version": "",
            "forge_version": "",
            "fabric_version": "",
            "optifine_version": ""
        }
        if config["mainClass"] == "net.minecraft.launchwrapper.Launch":  # Optifine
            # optifine:OptiFine:MCVERSION_VERSION
            a = config["libraries"][-2]["name"]
            info["optifine_version"] = a.split(":")[-1].split("_",1)[-1]
        elif "fabricmc" in config["mainClass"]:  # Fabric
            # net.fabricmc:fabric-loader:VERSION
            a = config["libraries"][-1]["name"]
            info["fabric_version"] = a.split(":")[-1]
        elif "cpw.mods" in config["mainClass"]:  # Forge
            a = config["arguments"]["game"].index("--fml.forgeVersion")
            info["forge_version"] = config["arguments"]["game"][a+1]
        else:
            info["version"] = config["id"]

        if "clientVersion" in config:
            info["version"] = config["clientVersion"]
        elif "inheritsFrom" in config:
            info["version"] = config["inheritsFrom"]

        try:
            os.makedirs(f'{self.game_path}/FMCL')
        except:
            pass
        json.dump(info, open(f'{self.game_path}/FMCL/config.json', mode='w'))

    def del_game(self):
        shutil.rmtree(self.game_path)
        if self.name == g.cur_version:
            g.cur_version = ""

    def rename(self, new_name):
        old_name = self.name
        os.rename(self.game_path, os.path.join(self.version_path, new_name))
        if self.name == g.cur_version:
            g.cur_version = new_name
        self.name = new_name
        self.game_path = os.path.join(self.version_path, self.name)
        os.rename(self.game_path+f"/{old_name}.jar",
                  self.game_path+f"/{self.name}.jar")
        os.rename(self.game_path+f"/{old_name}.json",
                  self.game_path+f"/{self.name}.json")
        os.rename(self.game_path+f"/{old_name}-natives",
                  self.game_path+f"/{self.name}-natives")
