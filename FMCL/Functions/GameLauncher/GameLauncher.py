import logging
import os
import traceback
import psutil

import qtawesome as qta
from Core import Version, Task
from PyQt5.QtCore import QProcess, pyqtSignal, pyqtSlot, QTimer, QEvent
from PyQt5.QtWidgets import QWidget, qApp
from qfluentwidgets import MessageBox, TransparentToolButton
from datetime import datetime

from Events import *
from Setting import Setting

from .ui_GameLauncher import Ui_GameLauncher

CPU_COUNT = psutil.cpu_count()


class GameLauncher(QWidget, Ui_GameLauncher):
    __launchCommand = pyqtSignal()

    def __init__(self, game_name: str):
        super().__init__()
        self.setupUi(self)
        t = self.tr("游戏日志")
        self.setWindowTitle(f"[{datetime.now().strftime('%H:%M:%S')}]{t}:{game_name}")
        self.setWindowIcon(qta.icon("mdi.rocket-launch-outline"))

        self.command_name = ""

        self.auto_scroll = True  # 自动滚动日志
        self.name = game_name
        self.te_output.setReadOnly(True)
        self.__launchCommand.connect(self.__start)

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.outputStandard)
        self.process.readyReadStandardError.connect(self.errorStandard)

        qApp.aboutToQuit.connect(self.on_aboutToQuit)

        self.pb_auto_scroll = TransparentToolButton()
        self.pb_auto_scroll.resize(46, 32)
        self.pb_auto_scroll.clicked.connect(
            lambda: self.setAutoScroll(not self.auto_scroll)
        )
        self.setAutoScroll(self.auto_scroll)

        self.use_javawrapper = False  # 使用JavaWrapper.jar

        t = self.tr("启动游戏")
        self.game = Version(self.name)
        self.root = Task(
            f"{t}:{game_name}",
            taskfunc=self.prepare,
            exception_handler=[self.showError],
        )
        self.root.start()

    def setAutoScroll(self, auto_scroll: bool):
        self.auto_scroll = auto_scroll
        if self.auto_scroll:
            self.pb_auto_scroll.setIcon(qta.icon("fa.lock"))
            self.pb_auto_scroll.setToolTip(self.tr("自动滚动"))
        else:
            self.pb_auto_scroll.setIcon(qta.icon("fa.unlock-alt"))
            self.pb_auto_scroll.setToolTip(self.tr("手动滚动"))

    def showError(self, e: Exception):
        MessageBox(self.tr("启动游戏失败"), str(e), self).exec()
        return True

    def prepare(self, callback=None):
        """准备启动游戏"""
        self.game_path, self.commands = self.game.get_launch_command(callback)
        self.__launchCommand.emit()

    def __start(self):
        command = self.commands.pop(0)
        program, args, self.command_name = command
        self.use_javawrapper = False
        if self.command_name == "Main":
            # 假设username的前一个就是mainClass
            main_class_index = args.index("--username") - 1
            javawrapper_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                "JavaWrapper.jar",
            )
            logging.info(f"{javawrapper_path}, {os.path.exists(javawrapper_path)}")
            if os.path.exists(javawrapper_path) and not Setting().get(
                "gamelauncher.never_use_javawrapper", False
            ):
                logging.info("使用javawrapper")
                self.use_javawrapper = True
                args = (
                    args[:main_class_index]
                    + ["-jar", javawrapper_path]
                    + args[main_class_index:]
                )
                timerec = self.game.get_timerec()
                if len(timerec) > 0:
                    self.timerec_index = max(timerec) + 1
                else:
                    self.timerec_index = 0
            else:
                self.timerec_index = self.game.record_new_start_time()
        logging.info(f"运行{self.command_name}: ")
        logging.info(program)
        logging.info(args)

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
        scrollbar = self.te_output.verticalScrollBar()
        self.te_output.append(text.rstrip())
        if self.auto_scroll:
            scrollbar.setValue(scrollbar.maximum())

    @pyqtSlot(bool)
    def on_pb_kill_clicked(self, _):
        self.process.kill()
        self.process.waitForFinished()
        self.commands = []  # 清空
        self.afterKilling()
        logging.info(f"{self.name}被用户终止")

    def afterKilling(self):
        self.timer.stop()
        self.pb_kill.setEnabled(False)
        # 无论用没用JavaWrapper都要写入结束时间
        # 因为进程可能被用户终止或出现其它异常状况
        if self.command_name == "Main":
            self.game.record_end_time(self.timerec_index)
        self.command_name = ""
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

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_auto_scroll, "right"))
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_auto_scroll))
            self.pb_auto_scroll.setParent(self)
        return super().event(a0)

    def on_aboutToQuit(self):
        # 测试时, 父进程退出后子进程有时会退出, 有时不会
        # 所以这里保留一下
        return
        if self.process.state() != QProcess.ProcessState.NotRunning:
            logging.info("等待游戏进程结束")
            self.process.waitForFinished()
            self.afterKilling()
