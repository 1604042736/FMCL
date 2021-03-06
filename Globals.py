import os
import threading
import json
from PyQt5.QtWidgets import qApp

TAG_NAME = "1.2.2"  # 当前版本号

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
homepage_qml = ""
theme = "rgba(255,255,255,255)"

try:
    config = json.load(open("FMCL/config.json", encoding="utf-8"))
    cur_gamepath = config["cur_gamepath"]
    all_gamepath = config["all_gamepath"]
    cur_version = config["cur_version"]
    users = config["users"]
    if config["cur_user_index"] != -1:
        cur_user = users[config["cur_user_index"]]
    java_path = config["java_path"]
    width = int(config["width"])
    height = int(config["height"])
    maxmen = int(config["maxmem"])
    minmem = int(config["minmem"])
    homepage_qml = config["homepage_qml"]
    theme = config["theme"]
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
        "homepage_qml": homepage_qml,
        "theme": theme
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
QFrame#f_panel_download{{
    background-color:{PANEL_COLOR};
}}
QFrame#f_panel_download QPushButton:checked{{
    border-bottom:2px solid {BUTTON_CHECKED_BORDER_COLOR};
}}
QFrame#Dialog{{
    border:1px solid rgb(0,0,0);
}}
QFrame#Dialog QPushButton{{
    border-bottom:1px solid rgb(0,0,0);
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
    font-size:13px;
}}
QTableWidget{{
    border:none;
}}
"""
    qApp.setStyleSheet(APP_QSS)
