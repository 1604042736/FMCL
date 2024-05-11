import os
import logging
import json
from Setting import DEFAULT_SETTING_PATH

from PyQt5.QtCore import QTranslator


class Translation:
    """翻译"""

    @staticmethod
    def get_path():
        default_path = "FMCL/Default/FMCL"
        return (
            (
                (
                    [
                        f"{default_path}/Functions/{i}/Translations"
                        for i in os.listdir(f"{default_path}/Functions")
                    ]
                )
                if os.path.exists(f"{default_path}/Functions")
                else []
            )
            + (
                (
                    [
                        f"FMCL/Functions/{i}/Translations"
                        for i in os.listdir("FMCL/Functions")
                    ]
                )
                if os.path.exists("FMCL/Functions")
                else []
            )
            + (
                [
                    f"{default_path}/Translations/{i}"
                    for i in os.listdir(f"{default_path}/Translations")
                    if os.path.isdir(os.path.join(f"{default_path}/Translations", i))
                ]
                if os.path.exists(f"{default_path}/Translations")
                else []
            )
            + (
                [
                    f"FMCL/Translations/{i}"
                    for i in os.listdir("FMCL/Translations")
                    if os.path.isdir(os.path.join("FMCL/Translations", i))
                ]
                if os.path.exists("FMCL/Translations")
                else []
            )
        )

    @staticmethod
    def load(app):
        """加载翻译"""
        logging.info("加载翻译...")
        # 在未加载翻译之前不能使用Setting
        lang = (
            json.load(open(DEFAULT_SETTING_PATH, encoding="utf-8")).get(
                "language.type", "简体中文"
            )
            + ".qm"
        )
        app.__translators = []  # 防止Translator被销毁
        # QTranslator优先搜索最新安装的文件
        for i in Translation.get_path():
            file = f"{i}/{lang}"
            if not os.path.exists(file):
                continue
            translator = QTranslator()
            if translator.load(file):
                if app.installTranslator(translator):
                    logging.info(f"已加载{file}")
                    app.__translators.append(translator)
                else:
                    logging.error(f"无法加载{file}")

    @staticmethod
    def get_all_languages():
        """获取所有语言"""
        lang = []
        for path in Translation.get_path():
            if not os.path.exists(path):
                continue
            for i in os.listdir(path):
                full_path = os.path.join(path, i)
                if os.path.isdir(full_path):
                    continue
                name, ext = os.path.splitext(i)
                if ext == ".qm":
                    lang.append(name)
        return set(lang)
