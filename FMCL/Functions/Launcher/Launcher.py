import logging

import multitasking
import qtawesome as qta
from Core import Game
from Kernel import Kernel
from PyQt5.QtCore import QProcess, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from .ui_Launcher import Ui_Launcher

_translate = Kernel.translate


class Launcher(QWidget, Ui_Launcher):
    __commandGot = pyqtSignal(str, list)

    def __init__(self, game_name: str):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"{_translate('启动游戏')}:{game_name}")
        self.setWindowIcon(qta.icon("mdi.rocket-launch-outline"))
        self.name = game_name
        self.te_output.setReadOnly(True)
        self.__commandGot.connect(self.__start)

    @multitasking.task
    def start(self):
        game = Game(self.name)
        dir, command = game.get_launch_command()
        logging.info(command)
        self.__commandGot.emit(dir, command)

    def __start(self, dir, command):
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.outputStandard)
        self.process.readyReadStandardError.connect(self.errorStandard)
        program, *args = command
        self.process.setWorkingDirectory(dir)
        self.process.start(program, args)

    def outputStandard(self):
        try:
            text = self.process.readAllStandardOutput().data().decode("utf-8")
        except:
            text = self.process.readAllStandardOutput().data().decode("gbk")
        self.output(text)

    def errorStandard(self):
        try:
            text = self.process.readAllStandardError().data().decode("utf-8")
        except:
            text = self.process.readAllStandardError().data().decode("gbk")
        self.output(text)

    def output(self, text: str):
        text = text.rstrip()
        flag = False
        scrollbar = self.te_output.verticalScrollBar()
        if scrollbar.value() == scrollbar.maximum():
            flag = True
        self.te_output.append(text)
        if flag:
            scrollbar.setValue(scrollbar.maximum())

    @pyqtSlot(bool)
    def on_pb_kill_clicked(self, _):
        self.process.kill()
        self.output("游戏结束!")
