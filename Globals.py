import os
import threading
import json
import logging
import sys
from PyQt5.QtWidgets import qApp, QPushButton
import QtFBN as g
import qtawesome as qta


class StdLog:
    __console__ = sys.stdout

    def __init__(self) -> None:
        try:
            os.makedirs("FMCL")
        except:
            pass
        open("./FMCL/latest.log", mode='w', encoding='utf-8').write("")

    def write(self, msg):
        if self.__console__:
            self.__console__.write(msg)
        # 每次重新打开追加可以防止因程序崩溃导致日志无法正常导出
        with open("./FMCL/latest.log", mode='a', encoding='utf-8') as file:
            file.write(msg)

    def flush(self):
        if self.__console__:
            self.__console__.flush()


sys.stdout = sys.stderr = StdLog()

logformat = logging.Formatter(
    '[%(asctime)s] [%(levelname)s]: %(message)s', '%Y-%m-%d,%H:%M:%S')

logapi = logging.getLogger()  # 日志接口
logapi.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logformat)

logapi.addHandler(ch)


TAG_NAME = "1.11.1"  # 当前版本号

dmgr = None  # 下载管理

cur_gamepath = ".minecraft"
cur_version = ""
all_gamepath = [".minecraft"]

# 格式:
# {
#   "name":"...",
#   "type":"offline"|"mojang",
#   "account":"...",
#   "password":"..."
# }
users = []
cur_user = None

java_path = "javaw"
width = 1000
height = 618
maxmem = 1024
minmem = 256
background_image = ""
theme = "rgba(255,255,255,255)"
language = "简体中文"
max_thread_count = 64

try:
    config = json.load(open("FMCL/config.json", encoding="utf-8"))
    cur_gamepath = config.get("cur_gamepath", cur_gamepath)
    all_gamepath = config.get("all_gamepath", all_gamepath)
    cur_version = config.get("cur_version", cur_version)
    users = config.get("users", users)
    if config.get("cur_user_index", -1) != -1:
        cur_user = users[config.get("cur_user_index", -1)]
    java_path = config.get("java_path", java_path)
    width = int(config.get("width", width))
    height = int(config.get("height", height))
    maxmen = int(config.get("maxmem", maxmem))
    minmem = int(config.get("minmem", minmem))
    background_image = config.get("background_image", background_image)
    theme = config.get("theme", theme)
    language = config.get("language", language)
    max_thread_count = int(config.get("max_thread_count", max_thread_count))
except Exception as e:
    print(e)


def run_as_thread(func):
    """让函数在新线程中运行"""
    def wrap(*args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()
    return wrap


def save():
    try:
        os.makedirs("FMCL")
    except:
        pass
    config = {
        "cur_gamepath": cur_gamepath,
        "all_gamepath": all_gamepath,
        "cur_version": cur_version,
        "users": users,
        "java_path": java_path,
        "width": width,
        "height": height,
        "maxmem": maxmem,
        "minmem": minmem,
        "background_image": background_image,
        "theme": theme,
        "language": language,
        "max_thread_count": max_thread_count
    }
    if cur_user in users:
        config["cur_user_index"] = users.index(cur_user)
    else:
        config["cur_user_index"] = -1
    json.dump(config, open("FMCL/config.json", mode="w", encoding="utf-8"))


def set_theme():
    global BUTTON_HOVER_COLOR, TITLE_COLOR
    color = theme.replace("rgba(", "").replace(")", "").split(",")
    color = list(map(int, color))

    TITLE_COLOR = theme
    BUTTON_CHECKED_BORDER_COLOR = f"rgba({255-color[0]},{255-color[1]},{255-color[2]},{color[3]})"
    BUTTON_HOVER_COLOR = f"rgba({int(color[0]/2)},{int(color[1]/2)},{int(color[2]/2)},{int(color[3]/2)})"
    PANEL_COLOR = theme

    APP_QSS = f"""
QFrame#f_title{{
    background-color:{TITLE_COLOR};
}}
QPushButton{{
    border:none;
}}
QPushButton:hover{{
    background-color:{BUTTON_HOVER_COLOR};
}}
QPushButton#pb_close:hover{{
    background-color:rgb(255,0,0);
}}
QFrame#f_panel{{
    background-color:{PANEL_COLOR};
}}
QFrame#f_panel QPushButton{{
    text-align:left;
}}
QFrame#f_panel QPushButton:checked{{
    border-left:2px solid {BUTTON_CHECKED_BORDER_COLOR};
}}
QFrame#f_panel_download{{
    background-color:{PANEL_COLOR};
}}
QFrame#f_panel_download QPushButton:checked{{
    border-bottom:2px solid {BUTTON_CHECKED_BORDER_COLOR};
}}
QPushButton#task_button{{
    text-align:left;
}}
QGroupBox{{
    font-size: 13px;
    font-weight: bold;
    border:4px solid white;
    border-radius:10px;
    background-color:white;
}}
QListWidget{{
    border:none;
}}
QListWidget::Item:hover{{
    background-color:rgb(240,240,240);
}}
QListWidget::Item:selected{{
    background-color:rgb(230,230,230);
}}
QLabel#l_notice{{
    background-color:rgb(0,255,0);
    color:rgb(255,255,255);
}}
QTableWidget{{
    border:none;
}}
QTableWidget#Desktop{{
    background-image:url({background_image});
}}
QScrollArea{{
    border:none;
}}
"""
    qApp.setStyleSheet(APP_QSS)


def on_any_win_ready(win) -> None:
    win.pb_dmgr = QPushButton(win.win.title)
    win.pb_dmgr.resize(win.win.title_button_width,
                       win.win.title_height)
    win.pb_dmgr.setObjectName('pb_dmgr')
    win.pb_dmgr.setIcon(qta.icon('ri.download-2-fill'))
    win.pb_dmgr.clicked.connect(lambda: dmgr.show())
    win.pb_dmgr.hide()
    win.win.add_right_widget(win.pb_dmgr)
    if dmgr.task_num:  # 只有在有任务的时侯才会显示
        win.pb_dmgr.show()

    dmgr.NoTask.connect(lambda: notask(win))
    dmgr.HasTask.connect(lambda: hastask(win))


def notask(win):
    win.pb_dmgr.hide()
    win.win.resize_title_widgets()


def hastask(win):
    win.pb_dmgr.show()
    win.win.resize_title_widgets()


g.on_any_win_ready = on_any_win_ready
