import os
import shutil
import python_nbt.nbt as nbt
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap

_translate = QCoreApplication.translate


class Save:
    """对游戏存档的管理"""

    def __init__(self, path):
        self.path = path
        self.icon = QPixmap(os.path.join(path, "icon.png"))
        self.level_file = nbt.read_from_nbt_file(os.path.join(path, "level.dat"))
        self.level_json = self.level_file.json_obj(full_json=False)
        self.levelname = self.level_json["Data"]["LevelName"]
        self.allowcommands = self.level_json["Data"]["allowCommands"]
        self.gametype = {
            0: _translate("Save", "生存模式"),
            1: _translate("Save", "创造模式"),
            2: _translate("Save", "冒险模式"),
            3: _translate("Save", "旁观模式"),
        }[self.level_json["Data"]["GameType"]]
        self.lastplayed = self.level_json["Data"]["LastPlayed"]
        self.version_name = self.level_json["Data"]["Version"]["Name"]
        self.lastplayed /= 1000

    def delete(self):
        shutil.rmtree(self.path)
