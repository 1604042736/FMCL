import logging
import threading
import time
from typing import Callable
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QCoreApplication

_translate = QCoreApplication.translate

SLEEP_TIME = 0.005  # 循环等待时间(秒)


class TaskExceptionPass(QObject):
    """负责传递Task的异常(在主线程中)"""

    def __init__(self, task: "Task") -> None:
        super().__init__()
        self.task = task
        task.occurException.connect(self.handleException)

    def handleException(self, e: Exception, exception_handler: list):
        if isinstance(self.task.parent(), Task):  # 一级一级上报
            self.task.parent().occurException.emit(
                e, self.task.parent().exception_handler + exception_handler
            )
        else:
            self.task.terminate()
            flag = False
            for handler in exception_handler:
                if handler(e):
                    flag = True
            if not flag:  # 如果错误处理过了就不raise
                raise e  # 在主线程里raise


class TaskCreator(QObject):
    """负责在主线程中创建Task"""

    __createTask = pyqtSignal(tuple, dict, str)

    instance = None
    new_count = 0

    def __new__(cls):
        if TaskCreator.instance == None:
            TaskCreator.instance = super().__new__(cls)
        TaskCreator.new_count += 1
        return TaskCreator.instance

    def __init__(self):
        if TaskCreator.new_count > 1:
            return
        super().__init__()
        self.created_tasks: dict[str, Task] = {}
        self.__createTask.connect(self.createTask)

    def createTask(self, args, kwargs, hash):
        self.created_tasks[hash] = Task(*args, **kwargs)

    def newTask(self, args, kwargs) -> "Task":
        hash = f"{time.time()}{threading.get_ident()}"
        args = tuple(args)
        self.__createTask.emit(args, kwargs, hash)
        while hash not in self.created_tasks:
            time.sleep(SLEEP_TIME)
        return self.created_tasks[hash]


class Task(QThread):
    occurException = pyqtSignal(Exception, list)
    # started和finished信号的回调函数
    startedCallback = []
    finishedCallback = []

    @staticmethod
    def waitTasks(tasks, callback):
        while True:
            for task in tasks:
                if not task.isFinished():
                    callback.get("setStatus", lambda _: None)(
                        f'{_translate("Task","等待")} {task.name}'
                    )
                    break
            else:
                break
            time.sleep(SLEEP_TIME)

    def __new__(cls, *args, **kwargs):
        if threading.current_thread().getName() == "MainThread":
            return super().__new__(cls)
        else:
            return TaskCreator().newTask(args, kwargs)

    def __init__(
        self,
        name: str = "",
        parent: QObject | None = None,
        taskfunc=None,
        waittasks: list["Task"] = None,
        exception_handler: list[Callable[[Exception], bool]] = None,
    ) -> None:
        if threading.current_thread().getName() != "MainThread":  # 子线程的Task已在主线程中初始化过
            return
        super().__init__(parent)
        self.taskfunc = taskfunc  # 要运行的函数
        self.waittasks: list[Task] = waittasks if waittasks != None else []  # 等待的任务
        self.name: str = name  # 名称
        self.status: str = ""  # 状态
        self.progress: int = 0  # 进度
        self.maxprogress: int = 0  # 最大进度
        self.terminated: bool = False  # 是否被终止

        self.exceptionpass = TaskExceptionPass(self)
        self.exception_handler = (
            exception_handler if exception_handler != None else []
        )  # 异常处理

        self.callback = {
            "setStatus": lambda a: setattr(self, "status", a),
            "setProgress": lambda a: setattr(self, "progress", a),
            "setMax": lambda a: setattr(self, "maxprogress", a),
            "getCurTask": lambda: self,
        }

        self.started.connect(
            lambda: list(callback(self) for callback in Task.startedCallback)
        )
        self.finished.connect(
            lambda: list(callback(self) for callback in Task.finishedCallback)
        )

    def run(self) -> None:
        self.waitTasks(self.waittasks, self.callback)

        self.status = self.tr("启动子任务")
        for task in self.children():
            if isinstance(task, Task):
                task.start()

        self.status = ""
        if self.taskfunc:
            try:
                self.taskfunc(self.callback)
            except Exception as e:
                logging.warning(f"产生错误:{e}")
                self.occurException.emit(e, self.exception_handler)  # 交给主线程来raise

        self.status = self.tr("等待子任务执行完成")
        while True:
            for task in self.children():  # children会变所以不能用Task.waitTasks
                if isinstance(task, Task) and not task.isFinished():
                    break
            else:
                break
            time.sleep(SLEEP_TIME)

    def terminate(self) -> None:
        self.terminated = True
        for task in self.children():
            if isinstance(task, Task):
                task.terminate()
        return super().terminate()

    def __repr__(self):
        return f'Task("{self.name}")'
