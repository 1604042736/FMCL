import logging

import qtawesome as qta
from Core import Game, Task
from PyQt5.QtCore import QProcess, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from .ui_Launcher import Ui_Launcher


class Launcher(QWidget, Ui_Launcher):
    __commandGot = pyqtSignal(str, list)

    def __init__(self, game_name: str):
        super().__init__()
        self.setupUi(self)
        t = self.tr('游戏日志')
        self.setWindowTitle(f"{t}:{game_name}")
        self.setWindowIcon(qta.icon("mdi.rocket-launch-outline"))
        self.name = game_name
        self.te_output.setReadOnly(True)
        self.__commandGot.connect(self.__start)

        t = self.tr('启动游戏')
        self.game = Game(self.name)
        Task(
            f"{t}:{game_name}",
            children=[
                Task(self.tr("检查外置登录"),
                     self.game.check_authlibinjector),
                Task(self.tr("获取命令行参数"),
                     lambda _:setattr(self, "dir_command",
                                      self.game.get_launch_command()),
                     waittasks=[0]),
                Task(self.tr("启动"),
                     lambda _:(self.show(),
                     self.__commandGot.emit(self.dir_command[0], self.dir_command[1])),
                     waittasks=[1])
            ]
        ).start()

    def __start(self, dir, command):
        logging.info(command)
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.outputStandard)
        self.process.readyReadStandardError.connect(self.errorStandard)
        program, *args = command
        self.process.setWorkingDirectory(dir)
        self.process.start(program, args)
        self.pb_kill.setEnabled(True)

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
        self.output(self.tr("游戏结束"))
        logging.info(f"{self.name}被用户终止")
