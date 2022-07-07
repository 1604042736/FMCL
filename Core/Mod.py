import os
from bs4 import BeautifulSoup, element
import re
import requests
from Core import CoreBase
from Core.Download import download


class Mod(CoreBase):
    # https://api.curseforge.com/v1
    def __init__(self, name="", info={}, path="") -> None:
        super().__init__()
        self.name = name
        self.info = info
        self.path = path

    def search_mod(self) -> list[dict]:
        '''搜索模组'''
        url = f'https://search.mcmod.cn/s?key={self.name}'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        search_result_list = soup.find_all('div', class_='result-item')
        _search_result_list = []

        for i in search_result_list:
            info = self.parse_search_result(i)
            if info:
                _search_result_list.append(info)

        return _search_result_list

    def parse_search_result(self, search_result: element.Tag) -> dict:
        '''解析搜索结果'''
        result = {}
        try:
            head = search_result.find('div', class_='head')

            target_blank = head.find_all('a')[-1]
            name = target_blank.text
            mcmode_url = target_blank['href']

            result['name'] = name
            result['mcmod_url'] = mcmode_url

            describe = search_result.find('div', class_='body').text
            result['describe'] = describe

            pattern = r'https://www.curseforge.com/minecraft/mc-mods/.*?</strong>'

            html = requests.get(mcmode_url).text
            result['curseforge_url'] = re.findall(
                pattern, html)[0].replace('</strong>', '')
        except:
            pass

        return result

    def get_mod_files(self) -> list[dict]:
        '''获取模组文件'''
        url = self.info['curseforge_url']+'/files/all'
        files = []
        html = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Referer': 'https://www.curseforge.com/'
        }).text
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.find_all('tr')
        for tr in trs:
            files.append(self.get_mod_file_info(tr))

        return files

    def get_mod_file_info(self, tr: element.Tag) -> dict:
        result = {}

        td = tr.find_all('td')[1]
        a = td.find_all('a')

        result['name'] = a.text
        result['url'] = a['href']

        return result

    def download_mod_file(self):
        '''下载模组文件'''
        url = 'https://www.curseforge.com/'+self.info['url']
        download(url, self.path, self, True)

    def get_mods(self) -> list:
        """获取文件夹下的mod"""
        result = []
        for i in os.listdir(self.path):
            if self.is_mod(i):
                result.append(i)
        return result

    def is_mod(self, name) -> bool:
        """判断是否是mod"""
        return "jar" in name or "disabled" in name

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
