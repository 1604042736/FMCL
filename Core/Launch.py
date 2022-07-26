# -*- coding: utf-8 -*-
import json
import os
import shutil
from zipfile import ZipFile
import platform
import sys
from Core import CoreBase
import Globals as g
from Core.Download import download


class Launch(CoreBase):
    '''
    启动游戏
    参考https://minecraft.fandom.com/zh/wiki/%E6%95%99%E7%A8%8B/%E7%BC%96%E5%86%99%E5%90%AF%E5%8A%A8%E5%99%A8?amp%3Bvariant=zh
    '''
    system_name = platform.system().lower()
    system_version = platform.version()

    maxbit = sys.maxsize
    if maxbit > 2**32:
        arch = 'x64'
    else:
        arch = 'x86'

    native_end = {  # 不同系统下native的后缀
        'windows': '.dll',
        'linux': '.so'
    }

    features = {
        "is_demo_user": False,
        "has_custom_resolution": True
    }

    def __init__(self, name) -> None:
        super().__init__()
        # 尽量使用绝对路径
        self.path = os.path.abspath(os.path.join(os.path.join(
            g.cur_gamepath, 'versions'), name))  # 游戏路径
        self.lib_path = os.path.abspath(os.path.join(
            g.cur_gamepath, 'libraries'))
        self.native_path = os.path.join(self.path, f'{name}-natives')
        self.asset_path = os.path.abspath(
            os.path.join(g.cur_gamepath, 'assets'))
        self.config = json.load(
            open(os.path.join(self.path, f'{name}.json')))  # json文件

        self.name = name
        self.classpath = []  # -cp后的参数
        self.cp_memory = {}  # classpath记忆

        self.total = 0  # 总任务
        self.cur = 0  # 当前任务进度

    def launch(self, javapath='javaw',
               playername='Player',
               width=1000,
               height=618,
               maxmem=1024,
               minmem=256):
        '''启动'''
        self.analysis_libraries()
        self.analysis_assets()

        self.classpath.append(os.path.join(self.path, f'{self.name}.jar'))

        # jvm参数必须放在游戏参数前!!!
        args = f'cd "{os.path.abspath(g.config["cur_gamepath"])}" & start {javapath} '
        args += f'-XX:+UseG1GC '
        args += f'-XX:-UseAdaptiveSizePolicy '
        args += f'-XX:-OmitStackTraceInFastThrow '
        args += f'-Dfml.ignoreInvalidMinecraftCertificates=True -Dfml.ignorePatchDiscrepancies=True -Dlog4j2.formatMsgNoLookups=true '

        if self.system_name == 'windows':  # 专门处理
            args += f'-Dos.name="Windows 10" '
            args += f'-Dos.version=10.0 '

        if "arguments" in self.config:  #有些版本的json文件是没有arguments的,比如1.8.9
            if "-DFabricMcEmu" in self.config['arguments']['jvm'][-1]:
                # 防止出现"-DFabricMcEmu= net.minecraft.client.main.Main "这样的情况
                # 这种情况会导致无法加载Fabric
                self.config["arguments"]["jvm"][-1] = "-DFabricMcEmu=net.minecraft.client.main.Main "

            for i in self.config['arguments']['jvm']:
                if isinstance(i, str):
                    args += i+' '
                elif isinstance(i, dict):
                    if 'rules' in i:
                        if self.check_rule(i['rules']):
                            if isinstance(i['value'], str):
                                args += i['value']+' '

        args += f'-Xmn{minmem}m '
        args += f'-Xmx{maxmem}m '
        args += f'{self.config["mainClass"]} '

        if "arguments" in self.config:
            for i in self.config['arguments']['game']:
                if isinstance(i, str):
                    args += i+' '
                elif isinstance(i, dict):
                    if 'rules' in i:
                        if self.check_rule(i['rules']):
                            if isinstance(i['value'], str):
                                args += i['value']+' '
                            else:
                                args += ' '.join(i['value'])+' '
        else:
            args += self.config["minecraftArguments"]+" "

        args = args.replace('${auth_player_name}', playername)
        args = args.replace('${version_name}', self.config["id"])
        args = args.replace('${game_directory}',
                            f'"{os.path.abspath(g.config["cur_gamepath"])}"')
        args = args.replace('${assets_root}', f'"{self.asset_path}"')
        args = args.replace('${assets_index_name}',
                            self.config["assetIndex"]["id"])
        args = args.replace('${auth_uuid}', '000000000000300C95C489********86')
        args = args.replace('${auth_access_token}',
                            '000000000000300C95C489********86')
        args = args.replace('${user_type}', 'Legacy')
        args = args.replace('${version_type}', 'FMCL')
        args = args.replace('${resolution_width}', str(width))
        args = args.replace('${resolution_height}', str(height))
        args = args.replace('${natives_directory}', f'"{self.native_path}"')
        args = args.replace('${launcher_name}', 'FMCL')
        args = args.replace('${launcher_version}', '1')
        args = args.replace('${classpath}', f'"{";".join(self.classpath)}"')

        os.popen(args)

        self.Finished.emit()

    def analysis_assets(self, sep=False):
        '''解析所有asset'''
        url = self.config['assetIndex']['url']
        name = self.config['assetIndex']['id']+'.json'
        indexes_path = os.path.join(self.asset_path, 'indexes')
        # assets/indexes/{版本名}.json
        indexes_file = os.path.join(indexes_path, name)
        download(url, indexes_file, self, True)
        indexes = json.load(open(indexes_file))
        for _, val in indexes['objects'].items():
            self.analysis_asset(val)

    def analysis_asset(self, val):
        '''解析asset'''
        try:
            objects_path = os.path.join(self.asset_path, 'objects')
            hash = val['hash']
            object_url = f'http://resources.download.minecraft.net/{hash[:2]}/{hash}'
            object_path = os.path.join(objects_path, f'{hash[:2]}/{hash}')
            download(object_url, object_path, self, True)
        except Exception as e:
            print(e)

    def analysis_libraries(self):
        '''解析json文件中的所有library'''
        for _, lib in enumerate(self.config['libraries']):
            self.analysis_library(lib)

    def analysis_library(self, lib):
        '''解析json文件中的library'''
        try:
            if "downloads" in lib:
                # 有classifiers的为natives库
                if 'classifiers' in lib['downloads']:
                    try:
                        native_name = lib['natives'][self.system_name]
                        path = os.path.join(
                            self.lib_path, lib['downloads']['classifiers'][native_name]['path'])
                        url = lib['downloads']['classifiers'][native_name]['url']
                        download(url, path, self, True)
                        if 'rules' in lib and not self.check_rule(lib['rules']):
                            return
                        self.unzip_native(path)
                    except KeyError as e:
                        pass
                else:
                    if 'rules' in lib and not self.check_rule(lib['rules']):
                        return
                    path = os.path.join(
                        self.lib_path, lib['downloads']['artifact']['path'])
                    url = lib['downloads']['artifact']['url']
                    download(url, path, self, True)
                    if "native" in path:  # 属于native的另一种情况
                        self.unzip_native(path)
                    else:
                        self.add_classpath(path)
            else:  # Fabric或Optifine的library
                name = lib["name"]
                path = self.name_to_path(name)
                self.add_classpath(self.lib_path+"/"+path)
        except Exception as e:
            print(e)

    def name_to_path(self, name):
        """将name转换成path"""
        a, b = name.split(":", 1)
        jar_file = b.replace(":", "-")+".jar"
        return a.replace(".", "/")+"/"+b.replace(":", "/")+"/"+jar_file

    def add_classpath(self, path):
        '''添加classpath'''
        path = path.replace('/', '\\')
        file = path.split('\\')[-1]
        # a-b-c.d.e.jar
        # a-b为name
        # c.d.e为version
        t = file.split('-')
        if len(t) > 2:
            name = '-'.join(file.split('-')[:2])
        else:
            name = '-'.join(file.split('-')[:1])
        version = '.'.join(file.split('-')[-1].split('.')[:-1])
        # 选择没有出现过的或者最新的版本
        if name not in self.cp_memory or self.compare_cp_version(version, self.cp_memory[name][0]):
            if name in self.cp_memory:  # 原先有的
                self.classpath.remove(self.cp_memory[name][1])
            self.classpath.append(path)
            self.cp_memory[name] = (version, path)

    def compare_cp_version(self, a, b):
        '''比较classpath的版本'''
        # 拆分开来
        va = map(int, a.split('.'))
        vb = map(int, b.split('.'))
        for i, j in zip(va, vb):
            if i > j:
                return True
        return False

    def unzip_native(self, path):
        '''解压native'''
        zip = ZipFile(path)
        for name in zip.namelist():
            if name.endswith(self.native_end[self.system_name]):
                zip.extract(name, self.native_path)
                path = self.native_path+"/"+name
                try:
                    shutil.move(path, self.native_path)
                except:
                    pass

    def check_rule(self, rules):
        '''检查rule,返回结果'''
        result = False  # 结果

        for rule in rules:
            if 'os' in rule:
                # 只要匹配上了就可以退出
                if 'name' in rule['os'] and rule['os']['name'] == self.system_name:
                    result = self.check_action(rule['action'])
                    break
                elif 'arch' in rule['os'] and rule['os']['arch'] == self.arch:
                    result = self.check_action(rule['action'])
                    break
            elif 'features' in rule:
                # 只要匹配上了就可以退出
                for key, val in rule['features'].items():
                    if self.features[key] != val:
                        result = False
                        break
                else:
                    result = self.check_action(rule['action'])
                    break
            else:  # 只有一个action的rule不能当成最终结果
                result = self.check_action(rule['action'])

        return result

    def check_action(self, action):
        '''检查行动'''
        return action == 'allow'
