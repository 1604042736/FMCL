import logging

import qtawesome as qta
from Core import Game
from Kernel import Kernel
from PyQt5.QtCore import QProcess, pyqtSlot
from PyQt5.QtWidgets import QWidget

from .ui_Launcher import Ui_Launcher

_translate = Kernel.translate


class Launcher(QWidget, Ui_Launcher):
    def __init__(self, game_name: str):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"{_translate('启动游戏')}:{game_name}")
        self.setWindowIcon(qta.icon("mdi.rocket-launch-outline"))
        self.name = game_name
        self.te_output.setReadOnly(True)

    def start(self):
        game = Game(self.name)
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.output)
        self.process.readyReadStandardError.connect(self.error)
        dir, command = game.get_launch_command()
        logging.info(command)
        program, *args = command
        self.process.setWorkingDirectory(dir)
        self.process.start(program, args)

    def output(self):
        try:
            text = self.process.readAllStandardOutput().data().decode("utf-8")
        except:
            text = self.process.readAllStandardOutput().data().decode("gbk")
        self.te_output.insertPlainText(text)

    def error(self):
        try:
            text = self.process.readAllStandardError().data().decode("utf-8")
        except:
            text = self.process.readAllStandardError().data().decode("gbk")
        self.te_output.insertPlainText(text)

    @pyqtSlot(bool)
    def on_pb_kill_clicked(self, _):
        self.process.kill()
