import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from qfluentwidgets import PushButton
from Setting import Setting

from .MusicPlayer import MusicPlayer

_translate = QCoreApplication.translate


def functionInfo():
    return {"name": _translate("MusicPlayer", "音乐播放器"), "icon": qta.icon("ei.music")}


def defaultSetting() -> dict:
    setting = Setting()
    if "system.startup_functions" in setting.defaultsetting:
        a = setting.defaultsetting.get("system.startup_functions")
        if "MusicPlayer" not in a:
            a.insert(2, "MusicPlayer")
    return {
        "musicplayer.playatstartup": True,
        "musicplayer.musiclist": [],
        "musicplayer.auto_sync_startindex": True,
        "musicplayer.startindex": 0,
    }


def defaultSettingAttr() -> dict:
    button = PushButton()
    button.setText(_translate("MusicPlayer", "前往音乐播放器设置"))

    def go():
        global fisrt_run
        fisrt_run = False
        main()

    button.clicked.connect(go)

    return {
        "musicplayer": {"name": _translate("MusicPlayer", "音乐播放器")},
        "musicplayer.playatstartup": {"name": _translate("MusicPlayer", "在启动时播放")},
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
    }


fisrt_run = True  # 用于判断是否是自启动的


def main():
    global fisrt_run
    setting = Setting()
    if "MusicPlayer" not in setting.defaultsetting.get(
        "system.startup_functions", tuple()
    ):
        fisrt_run = False
    if setting.get("musicplayer.playatstartup") == False:
        if fisrt_run != False:  # 是启动项但在启动时不播放
            fisrt_run = False
            return
    musicplayer = MusicPlayer()
    if fisrt_run:
        musicplayer.player.play()
        fisrt_run = False
    else:
        musicplayer.show()
