"""该功能只用来测试"""

import time
import qtawesome as qta

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import ScrollArea, PushButton
from Setting import Setting

from Core import Task, Download


def functionInfo():
    return {"name": "测试", "icon": qta.icon("ri.test-tube-line")}


def defaultSetting():
    return {"test.list": [], "test.dict": {}, "test.auto_refresh": []}


def defaultSettingAttr():
    def getbutton():
        button = PushButton()
        button.clicked.connect(
            lambda: Setting()["test.auto_refresh"].append(time.time())
        )
        return button

    return {"test.auto_refresh": {"side_widgets": [getbutton]}}


def empty(*_):
    pass


def testtask_func1(callback):
    callback.get("setStatus", empty)("Func1")
    n = 100
    callback.get("setMax", empty)(n - 1)
    for i in range(n):
        print(i)
        callback.get("setProgress", empty)(i)
        time.sleep(0.1)


def test_task1():
    """测试任务等待"""
    a = Task("test_task1", taskfunc=testtask_func1)
    a.start()
    b = Task("test_task1_1", taskfunc=testtask_func1)
    b.setParent(a)
    c = Task("test_task1_2", taskfunc=testtask_func1, waittasks=[b])
    c.setParent(a)
    b.start()


def test_task2():
    """测试任务异常"""

    def testtask_func2(callback):
        callback.get("setStatus", empty)("Func2")
        n = 100
        callback.get("setMax", empty)(n - 1)
        for i in range(n):
            print(i)
            callback.get("setProgress", empty)(i)
            if i >= 40:
                raise Exception("Exception from test_task2")
            time.sleep(0.1)

    a = Task("test_task2", taskfunc=testtask_func2)
    b = Task("test_task2_1", parent=a, taskfunc=testtask_func1)
    a.start()


def test_task3():
    """测试单任务"""
    a = Task("test_task3", taskfunc=testtask_func1)
    a.start()


def test_task4():
    """测试在任务中创建任务"""

    def testtask_func3(callback):
        callback.get("setStatus", empty)("Func3")
        n = 10
        callback.get("setMax", empty)(n - 1)
        for i in range(n):
            Task(
                f"test_task4_{i}", callback.get("getCurTask", empty)(), testtask_func1
            ).start()
            print(i)
            callback.get("setProgress", empty)(i)
            time.sleep(0.1)

    a = Task("test_task4", taskfunc=testtask_func3)
    a.start()


def test_download1():
    """测试小文件下载"""
    url = "https://authlib-injector.yushi.moe/artifact/52/authlib-injector-1.2.4.jar"
    task = Task(
        "test_download1",
        taskfunc=lambda callback: Download(
            url, "FMCL/Temp/test_download1.jar", callback=callback
        ).start(),
    )
    task.start()


def test_download2():
    """测试大文件下载"""
    url = "https://issuecdn.baidupcs.com/issue/netdisk/yunguanjia/BaiduNetdisk_7.2.8.9.exe"
    task = Task(
        "test_download2",
        taskfunc=lambda callback: Download(
            url, "FMCL/Temp/test_download2.exe", callback=callback
        ).start(),
    )
    task.start()


class Test(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("测试")
        self.setWindowIcon(qta.icon("ri.test-tube-line"))
        self.setWidgetResizable(True)
        self.resize(1000, 618)
        self.setStyleSheet("QScrollArea{border:none;}")

        self.contentwidget = QWidget()
        self.setWidget(self.contentwidget)

        self.contentwidget.setLayout(QVBoxLayout())

        import FMCL.Functions.Test as tests

        for i in dir(tests):
            if not i.startswith("test_"):
                continue
            button = PushButton()
            button.setText(f"{getattr(tests,i).__doc__}({i})")
            button.clicked.connect(lambda _, i=i: getattr(tests, i)())
            self.contentwidget.layout().addWidget(button)


def main():
    test = Test()
    test.show()
