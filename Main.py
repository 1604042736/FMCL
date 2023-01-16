import argparse
import logging
import os
import sys
import traceback
from importlib import import_module

import multitasking
import qtawesome as qta
from PyQt5.QtCore import QCoreApplication, QTranslator
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox, QPushButton

import Languages as _
import Resources as _
from Core import Game, Progress, User
from Functions import (About, CreateUser, GameDownloader, GameInfo,
                       GameManager, Help, LanguageChooser, LogoChooser,
                       ModDownloader, ModManager, News, Update)
from System import Application, Desktop, Explorer, Setting, Start
from System.Constants import *
from System.TaskManager import TaskManager

_translate = QCoreApplication.translate

single = {
    "Setting": Setting,
    "TaskManager": TaskManager,
    "CreateUser": CreateUser,
    "GameDownloader": GameDownloader,
    "News": News,
    "About": About,
    "Update": Update,
    "GameManager": GameManager,
    "LanguageChooser": LanguageChooser,
    "LogoChooser": LogoChooser,
    "Help": Help,
    "ModManager": ModManager,
    "GameInfo": GameInfo,
    "ModDownloader": ModDownloader
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


def getSettingAttr():
    return {
        "launcher": {
            "name": _translate("FMCLSetting", "启动器"),
        },
        "launcher.width": {
            "name": _translate("FMCLSetting", "启动器宽度"),
        },
        "launcher.height": {
            "name": _translate("FMCLSetting", "启动器高度"),
        },
        "launcher.language": {
            "name": _translate("FMCLSetting", "语言"),
            "setting_item": lambda: LanguageChooser()
        },
        "game": {
            "name": _translate("FMCLSetting", "游戏"),
        },
        "game.directories": {
            "name": _translate("FMCLSetting", "游戏目录"),
            "method": "directory",
            "atleast": 1
        },
        "game.java_path": {
            "name": _translate("FMCLSetting", "Java路径"),
        },
        "game.width": {
            "name": _translate("FMCLSetting", "游戏窗口宽度"),
        },
        "game.height": {
            "name": _translate("FMCLSetting", "游戏窗口高度"),
        },
        "users": {
            "name": _translate("FMCLSetting", "用户"),
            "method": lambda: CreateUser().show()
        }
    }


DEFAULT_SETTING = {
    "launcher.width": 1000,
    "launcher.height": 618,
    "launcher.language": ":/zh_CN.qm",
    "game.directories": [".minecraft"],
    "game.java_path": "javaw",
    "game.width": 1000,
    "game.height": 618,
    "users": User.get_all_users(),
}


def getPanelButtons():
    pb_user = QPushButton()
    pb_user.setText(_translate("FMCL", "未选择用户"))
    pb_user.setIcon(qta.icon("ph.user-circle"))
    pb_user.resize(W_PANEL, H_PANELBUTTON)
    pb_user.setStyleSheet(S_D_PANELBUTTON())
    pb_user.setIconSize(pb_user.size())
    pb_user.clicked.connect(lambda: Setting().show("users"))
    username = User.get_cur_user()
    if username:
        pb_user.setText(username["username"])

    return [(pb_user,)]


def getVersions():
    result = []
    directories = Setting().get("game.directories")
    if directories:
        directory = directories[0]
        if os.path.exists(directory+"/versions"):
            for i in os.listdir(directory+"/versions"):
                a_launch = QAction()
                a_launch.setText(_translate("Game", "启动"))
                a_launch.setIcon(qta.icon("mdi.rocket-launch-outline"))
                a_launch.triggered.connect(lambda _, v=i: Game(v).launch())

                a_manager = QAction()
                a_manager.setText(_translate("Game", "管理"))
                a_manager.setIcon(qta.icon("mdi6.minecraft"))
                a_manager.triggered.connect(
                    lambda _, v=i: GameManager(v).show())

                result.append((i,
                               Game(i).get_icon(),
                               [a_launch, a_manager]))
    return result


def getExtFunctions():
    result = []
    ext_path = "FMCL/Functions"
    if os.path.exists(ext_path):
        for i in os.listdir(ext_path):
            try:
                module = import_module(f"FMCL.Functions.{i}")
                result.append(module.__dict__["getFunctions"])
            except Exception as e:
                logging.error(f'无法加载功能"{i}": {e}')
    return result


def main():
    sys.stdout = sys.stderr = StdLog()
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] [%(levelname)s]: %(message)s',
                        datefmt='%Y-%m-%d,%H:%M:%S')

    parser = argparse.ArgumentParser(
        description="Functional Minecraft Launcher")
    parser.add_argument("--sep", choices=single.keys(),
                        help="Open a function separately")
    parser.add_argument("--args", nargs="+", default=[],
                        help="The parameter passed in to the function, used with --sep")
    parser.add_argument("--update",
                        help="Update completed, delete the previous version file")
    args = parser.parse_args()

    app = Application(sys.argv)
    app.setApplicationName("FMCL")
    app.setWindowIcon(QIcon(":/Icon/FMCL.ico"))
    app.setApplicationVersion("2.2")

    if args.update and os.path.exists(args.update):
        os.remove(args.update)

    setting = Setting()
    setting.addSetting(DEFAULT_SETTING)
    translateor = QTranslator()
    translateor.load(setting.get("launcher.language"))
    app.installTranslator(translateor)
    setting.addSettingAttr(getSettingAttr())

    if args.sep != None:
        single[args.sep](*args.args).show()
    else:
        Start.func_getters.append(
            lambda: [(_translate("Setting", "设置"), qta.icon("ri.settings-5-line"), lambda:Setting().show()),
                     (_translate("CreateUser", "创建用户"), qta.icon("ph.user-circle-plus"),
                      lambda:CreateUser().show()),
                     (_translate("GameDownloader", "游戏下载器"), qta.icon("ph.download-simple"),
                      lambda:GameDownloader().show()),
                     (_translate("Progress", "进度"), qta.icon("mdi.progress-download"),
                      lambda:Progress().show()),
                     (_translate("News", "新闻"), qta.icon(
                         "fa.newspaper-o"), lambda:News().show()),
                     (_translate("About", "关于"), qta.icon("mdi.information-outline"),
                      lambda:About().show()),
                     (_translate("Update", "更新"), qta.icon(
                         "mdi6.update"), lambda:Update().show()),
                     (_translate("LanguageChooser", "语言选择"), qta.icon(
                         "fa.language"), lambda:LanguageChooser().show()),
                     (_translate("Help", "帮助"), qta.icon(
                         "mdi.help"), lambda:Help().show()),
                     (_translate("ModDownloader", "Mod下载器"), qta.icon("mdi.puzzle-outline"), lambda:ModDownloader().show())])
        Start.func_getters.extend(getExtFunctions())

        Start.panel_getters.append(getPanelButtons)
        Desktop.item_getters.append(getVersions)

        explorer = Explorer()
        explorer.resize(setting.get("launcher.width"),
                        setting.get("launcher.height"))
        explorer.setWindowTitle("Functional Minecraft Launcher")
        explorer.show()

        Update()

    app.exec()
    multitasking.killall(None, None)


def except_hook(*args):
    sys.__excepthook__(*args)
    QMessageBox.critical(None,
                         _translate("FMCL", "启动器发生了严重错误"),
                         "".join(traceback.format_exception(*args)))
    exit()


sys.excepthook = except_hook


if __name__ == "__main__":
    main()
