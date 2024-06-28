import os
import logging
import json
from Setting import DEFAULT_SETTING_PATH, DEFAULT_SETTING

from PyQt5.QtCore import QTranslator

from Core.Function import Function
from Core.Help import Help


class Translation:
    """翻译"""

    PATH = ["FMCL/Translations", "FMCL/Default/FMCL/Translations"]

    @staticmethod
    def get_path():
        paths = []
        for path in Translation.PATH:
            if not os.path.exists(path):
                continue
            for i in os.listdir(path):
                paths.append(os.path.join(path, i))
        for path in Function.PATH:
            if not os.path.exists(path):
                continue
            for i in os.listdir(path):
                paths.append(os.path.join(path, i, "Translations"))
        for path in Help.PATH:
            if not os.path.exists(path):
                continue
            for i in os.listdir(path):
                paths.append(os.path.join(path, i, "Translations"))
        return paths

    @staticmethod
    def load(app):
        """加载翻译"""
        logging.info("加载翻译...")
        # 在未加载翻译之前不能使用Setting
        lang = (
            json.load(open(DEFAULT_SETTING_PATH, encoding="utf-8")).get(
                "language.type", DEFAULT_SETTING["language.type"]
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
