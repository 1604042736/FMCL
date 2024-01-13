import logging
import traceback
import psutil

import qtawesome as qta
from Core import Version, Task
from PyQt5.QtCore import QProcess, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import MessageBox

from .ui_GameLauncher import Ui_GameLauncher

CPU_COUNT = psutil.cpu_count()


class GameLauncher(QWidget, Ui_GameLauncher):
    __commandGot = pyqtSignal(str, list)

    def __init__(self, game_name: str):
        super().__init__()
        self.setupUi(self)
        t = self.tr("游戏日志")
        self.setWindowTitle(f"{t}:{game_name}")
        self.setWindowIcon(qta.icon("mdi.rocket-launch-outline"))
        self.name = game_name
        self.te_output.setReadOnly(True)
        self.__commandGot.connect(self.__start)

        t = self.tr("启动游戏")
        self.game = Version(self.name)
        self.root = Task(f"{t}:{game_name}")
        self.check = Task(
            self.tr("检查外置登录"),
            parent=self.root,
            taskfunc=self.game.check_authlibinjector,
            exception_handler=[self.showError],
        )
        self.getcommmand = Task(
            self.tr("获取命令行参数"),
            parent=self.root,
            taskfunc=lambda _: (
                setattr(self, "dir_command", self.game.get_launch_command())
            ),
            waittasks=[self.check],
            exception_handler=[self.showError],
        )
        self.launch = Task(
            self.tr("启动"),
            parent=self.root,
            taskfunc=lambda _: (
                self.show(),
                self.__commandGot.emit(self.dir_command[0], self.dir_command[1]),
            ),
            waittasks=[self.getcommmand],
        )
        self.root.start()

    def showError(self, e: Exception):
        MessageBox(self.tr("启动游戏失败"), str(e), self.window()).exec()
        return True

    def __start(self, dir, command):
        logging.info(command)
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.outputStandard)
        self.process.readyReadStandardError.connect(self.errorStandard)
        program, *args = command
        self.process.setWorkingDirectory(dir)
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
        self.afterKilling()
        logging.info(f"{self.name}被用户终止")

    def afterKilling(self):
        self.timer.stop()
        self.pb_kill.setEnabled(False)
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
