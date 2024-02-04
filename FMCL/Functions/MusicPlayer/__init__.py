import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from qfluentwidgets import PushButton
from Setting import Setting

from .MusicPlayer import MusicPlayer

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("MusicPlayer", "音乐播放器"),
        "icon": qta.icon("ei.music"),
    }


def defaultSetting() -> dict:
    setting = Setting()
    if "system.startup_functions" in setting.defaultsetting:
        a = setting.defaultsetting.get("system.startup_functions")
        action = {"commands": ['MusicPlayer Setting()["musicplayer.playatstartup"]']}
        if action not in a:
            a.insert(2, action)
    return {
        "musicplayer.playatstartup": True,
        "musicplayer.musiclist": [],
        "musicplayer.auto_sync_startindex": True,
        "musicplayer.startindex": 0,
        "musicplayer.volume": 100,
    }


def defaultSettingAttr() -> dict:
    button = PushButton()
    button.setText(_translate("MusicPlayer", "前往音乐播放器设置"))
    button.clicked.connect(main)

    return {
        "musicplayer": {"name": _translate("MusicPlayer", "音乐播放器")},
        "musicplayer.playatstartup": {
            "name": _translate("MusicPlayer", "在启动时播放")
        },
        "musicplayer.musiclist": {
            "name": _translate("MusicPlayer", "播放列表"),
            "settingcard": lambda: button,
        },
        "musicplayer.auto_sync_startindex": {
            "name": _translate("MusicPlayer", "从上次停止的地方开始播放"),
        },
        "musicplayer.startindex": {
            "name": _translate("MusicPlayer", "开始播放的音乐索引"),
            "enable_condition": (
                lambda setting: setting.get("musicplayer.auto_sync_startindex") == False
            ),
        },
        "musicplayer.volume": {"name": _translate("MusicPlayer", "音量")},
    }


def main(only_play=None):
    musicplayer = MusicPlayer()
    if only_play == True:
        musicplayer.player.play()
    elif only_play == False:
        pass
    else:
        musicplayer.show()
