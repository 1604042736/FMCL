import logging
import sys
import traceback
import psutil
import os
import time

import qtawesome as qta
from Core import Java, Version, Task
from PyQt5.QtCore import QProcess, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import MessageBox

from Setting import Setting

from .ui_GameLauncher import Ui_GameLauncher

CPU_COUNT = psutil.cpu_count()


class GameLauncher(QWidget, Ui_GameLauncher):
    __launchCommand = pyqtSignal()

    def __init__(self, game_name: str):
        super().__init__()
        self.setupUi(self)
        t = self.tr("游戏日志")
        self.setWindowTitle(f"{t}:{game_name}")
        self.setWindowIcon(qta.icon("mdi.rocket-launch-outline"))
        self.name = game_name
        self.te_output.setReadOnly(True)
        self.__launchCommand.connect(self.__start)

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.outputStandard)
        self.process.readyReadStandardError.connect(self.errorStandard)

        t = self.tr("启动游戏")
        self.game = Version(self.name)
        self.root = Task(
            f"{t}:{game_name}",
            taskfunc=self.prepare,
            exception_handler=[self.showError],
        )
        self.root.start()

    def showError(self, e: Exception):
        MessageBox(self.tr("启动游戏失败"), str(e), self).exec()
        return True

    def prepare(self, callback=None):
        """准备启动游戏"""
        self.game_path, self.commands = self.game.get_launch_command(callback)
        self.timerec_filepath = os.path.join(self.game_path, "FMCL", "TimeRecord.txt")
        self.__launchCommand.emit()

    def __start(self):
        command = self.commands.pop(0)
        logging.info(command)
        program, args = command
        self.process.setWorkingDirectory(self.game_path)
        self.process.start(program, args)
        self.pb_kill.setEnabled(True)

        self.process_info = psutil.Process(self.process.processId())
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showInfo)
        self.timer.start(1000)

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
        self.process.waitForFinished()
        self.commands = []  # 清空
        self.afterKilling()
        logging.info(f"{self.name}被用户终止")
        with open(self.timerec_filepath, "a+") as file:  # 补写结束时间
            file.write(f"1:{int(time.time())}\n")

    def afterKilling(self):
        self.timer.stop()
        self.pb_kill.setEnabled(False)
        if self.commands:
            self.__launchCommand.emit()
        else:
            self.l_info.setText(self.tr("游戏已停止"))

    def showInfo(self):
        if self.process.state() == QProcess.ProcessState.NotRunning:
            self.afterKilling()
            return
        try:  # 游戏可能在执行这部分的时侯停止
            info = [
                f"{self.tr('CPU使用率')}: {round(self.process_info.cpu_percent()/CPU_COUNT,1)}%",
                f"{self.tr('内存使用率')}: {round(self.process_info.memory_percent(),1)}%({round(self.process_info.memory_info().rss/1024/1024,1)}MB)",
            ]
            self.l_info.setText(", ".join(info))
        except:
            logging.error(traceback.format_exc())
