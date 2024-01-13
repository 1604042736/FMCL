import logging
import os

from PyQt5.QtCore import QCoreApplication

from Setting import Setting

_translate = QCoreApplication.translate


class Java:
    """与Java有关的操作"""

    @staticmethod
    def auto_find_java() -> list:
        """自动查找Java"""
        java_paths = []
        for _, val in os.environ.items():
            for path in val.split(";"):
                try:
                    if not os.path.exists(path):
                        continue
                    if os.path.isfile(path):
                        continue
                    logging.info(f"在{path}中查找Java")
                    for name in os.listdir(path):
                        full_path = os.path.join(path, name)
                        if not os.path.isfile(full_path):
                            continue
                        if name == "java.exe":
                            java_paths.append(full_path)
                except:
                    pass
        return java_paths

    def __init__(self, setting: Setting) -> None:
        self.setting = setting

    def get_executable_path(self):
        if len(self.setting["game.java_paths"]) == 0:
            raise Exception(_translate("Java", "没有可用的Java"))
        if self.setting["game.auto_choose_java"] == True:
            raise Exception(_translate("Java", "暂不支持自动选择Java"))
        else:
            return self.setting["game.java_paths"][0]
