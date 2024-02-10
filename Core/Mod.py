import logging
import os
import traceback
import toml
import json
from zipfile import ZipFile

from PyQt5.QtGui import QPixmap, QImage



class Mod:
    def __init__(self, path="") -> None:
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

    def __repr__(self) -> str:
        if self.path:
            return f"Mod({self.name})"
        return super().__repr__()
