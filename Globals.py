import os
import threading
import json

TAG_NAME = "1.0"  # 当前版本号

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
        "homepage_qml": homepage_qml
    }
    if cur_user in users:
        config["cur_user_index"] = users.index(cur_user)
    else:
        config["cur_user_index"] = -1
    json.dump(config, open("FMCL/config.json", mode="w", encoding="utf-8"))
