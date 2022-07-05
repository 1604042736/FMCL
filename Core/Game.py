from http import client
import shutil
import requests
import json
from Core.Download import download
from Core.Launch import Launch
import Globals as g
import os
from zipfile import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject


class Game(QObject):
    Finished = pyqtSignal()
    Progress = pyqtSignal(int, int)

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

    def __init__(self, name="", version="", forge_version="") -> None:
        super().__init__()
        self.name = name
        self.version = version
        self.forge_version = forge_version
        self.class_path = {}

    def download_version(self):
        '''下载版本'''

        version_path = os.path.join(g.cur_gamepath, 'versions')
        game_path = os.path.join(version_path, self.name)
        downloads = [[f'https://bmclapi2.bangbang93.com/version/{self.version}/client', game_path + f'\\{self.name}.jar'],
                     [f'https://bmclapi2.bangbang93.com/version/{self.version}/json', game_path + f'\\{self.name}.json']]
        if self.forge_version:  # 附带forge
            downloads.append(
                [f'https://bmclapi2.bangbang93.com/maven/net/minecraftforge/forge/{self.version}-{self.forge_version}/forge-{self.version}-{self.forge_version}-installer.jar', game_path+f'\\installer.jar'])
            downloads.append(
                [f'https://bmclapi2.bangbang93.com/maven/net/minecraftforge/forge/{self.version}-{self.forge_version}/forge-{self.version}-{self.forge_version}-userdev.jar', game_path+f'\\userdev.jar'])

        for task in downloads:
            download(task[0], task[1], self, True)

        if self.forge_version:
            self.install_forge()

        config = {  # 游戏配置信息
            "name": self.name,
            "version": self.version,
            "forge_version": self.forge_version
        }
        json.dump(config, open(f'{game_path}/FMCL/config.json', mode='w'))

        self.Finished.emit()

    def install_forge(self):
        '''安装forge'''
        version_path = os.path.join(g.cur_gamepath, 'versions')
        game_path = os.path.join(version_path, self.name)
        config = json.load(open(os.path.join(game_path, f'{self.name}.json')))

        installerpath = game_path+f'\\installer.jar'
        # 获取forge的配置
        zip = ZipFile(installerpath)
        zip.extract('version.json', game_path)
        zip.extract('install_profile.json', game_path)
        self.lib_path = os.path.join(g.cur_gamepath, f'libraries')
        forge_config = json.load(
            open(os.path.join(game_path, f'version.json')))

        self.install_profile = json.load(
            open(os.path.join(game_path, f'install_profile.json')))

        for i in self.install_profile['libraries']:
            self.analysis_library(zip, i)
        for i in forge_config['libraries']:
            self.analysis_library(zip, i)

        # client
        client_binpatch = self.get_client('BINPATCH')
        zip.extract(client_binpatch[1:], game_path)
        client_binpatch = os.path.abspath(game_path+f'{client_binpatch}')

        for i in self.install_profile['processors']:
            if "sides" in i and "client" not in i["sides"]:
                continue
            self.execute(i, game_path + f'\\{self.name}.jar', client_binpatch)

        zip.close()
        # 拼接
        self.splicing(config, forge_config)
        json.dump(config, open(os.path.join(
            game_path, f'{self.name}.json'), mode='w'))

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

    def analysis_library(self, forge_zip, lib):
        '''解析lib'''
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

    def del_game(self):
        '''删除游戏'''
        version_path = os.path.join(g.cur_gamepath, 'versions')
        game_path = os.path.join(version_path, self.name)
        shutil.rmtree(game_path)
