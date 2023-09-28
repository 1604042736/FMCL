import time

from PyQt5.QtCore import QThread


class Task(QThread):
    """任务
    一个任务呈树形结构
    """
    # started和finished信号的回调函数
    startedCallback = []
    finishedCallback = []

    def __init__(self, name, taskfunc=None, children: list["Task"] = None, waittasks: list[int] = None) -> None:
        super().__init__()
        self.name = name  # 任务名称
        self.children: list[Task] = children if children else []  # 子任务
        # 需要先等待哪几个兄弟任务完成
        self.waittasks: list[int] = waittasks if waittasks else []
        self.taskfunc = taskfunc  # 执行任务的函数

        for child in self.children:
            child.setParent(self)

        self.status: str = ""  # 状态
        self.progress: int = 0  # 进度
        self.maxprogress: int = 0  # 最大进度

        self.started.connect(lambda: list(callback(self)
                             for callback in Task.startedCallback))
        self.finished.connect(lambda: list(callback(self)
                              for callback in Task.finishedCallback))

    def run(self):
        if self.taskfunc:
            self.taskfunc({
                "setStatus": lambda a: setattr(self, "status", a),
                "setProgress": lambda a: setattr(self, "progress", a),
                "setMax": lambda a: setattr(self, "maxprogress", a)
            })

        self.status = ""
        self.maxprogress = len(self.children)
        self.progress = 0

        tasks_left = len(self.children)  # 剩下的任务
        while tasks_left:
            tasks_left = len(self.children)
            for child in self.children:
                if child.isFinished():
                    tasks_left -= 1
                    continue
                if child.isRunning():
                    continue
                for i in child.waittasks:
                    if not self.children[i].isFinished():
                        break
                else:
                    child.start()
            self.progress = len(self.children)-tasks_left
            time.sleep(0.01)  # 太快会卡死
