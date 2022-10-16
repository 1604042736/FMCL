import argparse
import logging
import os
import sys

import qtawesome as qta
from PyQt5.QtCore import QCoreApplication, QTranslator
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QPushButton

import Languages as _
import Resources as _
from Core import Game, Progress, User
from Functions import About, CreateUser, Downloader, GameManager, News, Update
from System import Application, Desktop, Explorer, Setting, Start
from System.Constants import *
from System.TaskManager import TaskManager

_translate = QCoreApplication.translate

single = {
    "Setting": Setting,
    "TaskManager": TaskManager,
    "CreateUser": CreateUser,
    "Downloader": Downloader,
    "News": News,
    "About": About,
    "Update": Update,
    "GameManager": GameManager
}


def getDefaultSetting():
    return {
        "launcher": {
            "name": _translate("FMCLSetting", "启动器"),
            "description": _translate("FMCLSetting", "对启动器的一些属性的设置"),
            "value": {
                "width": {
                    "name": _translate("FMCLSetting", "启动器宽度"),
                    "value": 1000
                },
                "height": {
                    "name": _translate("FMCLSetting", "启动器高度"),
                    "value": 618
                },
                "language": {
                    "name": _translate("FMCLSetting", "语言"),
                    "value": ":/zh_CN.qm"
                }
            }
        },
        "game": {
            "name": _translate("FMCLSetting", "游戏"),
            "description": _translate("FMCLSetting", "与游戏有关的一些设置"),
            "value": {
                "directories": {
                    "name": _translate("FMCLSetting", "游戏目录"),
                    "add": "directory",
                    "min_count": 1,
                    "description": _translate("FMCLSetting", "游戏目录"),
                    "value": [".minecraft"]
                },
                "java_path": {
                    "name": _translate("FMCLSetting", "Java路径"),
                    "value": "javaw"
                },
                "width": {
                    "name": _translate("FMCLSetting", "游戏窗口宽度"),
                    "value": 1000
                },
                "height": {
                    "name": _translate("FMCLSetting", "游戏窗口宽度"),
                    "value": 618
                }
            }
        },
        "users": {
            "name": _translate("FMCLSetting", "用户"),
            "description": _translate("FMCLSetting", "用户设置"),
            "add": lambda: CreateUser().show(),
            "delete": User.delete_user,
            "value": User.get_all_users()
        }
    }


class StdLog:
    __console__ = sys.stdout

    def __init__(self) -> None:
        if not os.path.exists("FMCL"):
            os.makedirs("FMCL")
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


def getPanelButtons():
    pb_user = QPushButton()
    pb_user.setText(_translate("FMCL", "未选择用户"))
    pb_user.setIcon(qta.icon("ph.user-circle"))
    pb_user.resize(W_PANEL, H_PANELBUTTON)
    pb_user.setStyleSheet(S_D_PANELBUTTON)
    pb_user.setIconSize(pb_user.size())
    pb_user.clicked.connect(lambda: Setting().show("users"))
    username = User.get_cur_user()
    if username:
        pb_user.setText(username["username"])

    return [(pb_user,)]


def getVersions():
    result = []
    directories = Setting().get("game/directories")
    if directories:
        directory = directories[0]
        if os.path.exists(directory+"/versions"):
            for i in os.listdir(directory+"/versions"):
                a_launch = QAction()
                a_launch.setText(_translate("FMCL", "启动"))
                a_launch.triggered.connect(lambda _, v=i: Game(v).launch())

                a_manager = QAction()
                a_manager.setText(_translate("FMCL", "管理"))
                a_manager.triggered.connect(
                    lambda _, v=i: GameManager(v).show())
                result.append(
                    (i, Game(i).get_icon(), [a_launch, a_manager]))
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Functional Minecraft Launcher")
    parser.add_argument("--single", choices=single.keys(), help="单独打开一个应用")
    parser.add_argument("--args", nargs="+", default=[],
                        help="传入应用的参数,与 --single 配合使用")
    parser.add_argument("--update", help="更新完成，删除上一个版本文件")
    args = parser.parse_args()

    app = Application(sys.argv)
    app.setApplicationName("FMCL")
    app.setWindowIcon(QIcon(":/Icon/FMCL.ico"))

    sys.stdout = sys.stderr = StdLog()
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] [%(levelname)s]: %(message)s',
                        datefmt='%Y-%m-%d,%H:%M:%S')

    if args.update and os.path.exists(args.update):
        os.remove(args.update)

    setting = Setting()
    setting.addSetting(getDefaultSetting())  # 翻译之前
    translateor = QTranslator()
    translateor.load(setting.get("launcher/language"))
    app.installTranslator(translateor)
    setting.addSetting(getDefaultSetting())  # 翻译过后

    if args.single != None:
        single[args.single](*args.args).show()
    else:
        Start.func_getters.append(
            lambda: [(_translate("Setting", "设置"), qta.icon("ri.settings-5-line"), lambda:Setting().show()),
                     (_translate("CreateUser", "创建用户"), qta.icon("ph.user-circle-plus"),
                      lambda:CreateUser().show()),
                     (_translate("Downloader", "下载器"), qta.icon("ph.download-simple"),
                      lambda:Downloader().show()),
                     (_translate("Progress", "进度"), qta.icon("mdi.progress-download"),
                      lambda:Progress().show()),
                     (_translate("News", "新闻"), qta.icon(
                         "fa.newspaper-o"), lambda:News().show()),
                     (_translate("About", "关于"), qta.icon("mdi.information-outline"),
                      lambda:About().show()),
                     (_translate("Update", "更新"), qta.icon("mdi6.update"), lambda:Update().show())])
        Start.panel_getters.append(getPanelButtons)
        Desktop.item_getters.append(getVersions)

        explorer = Explorer()
        explorer.setWindowTitle("Functional Minecraft Launcher")
        explorer.show()

        Update()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
