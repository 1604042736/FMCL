"""该功能只用来测试"""


import time


def functionInfo():
    return {"name": "测试"}


def empty(*_):
    pass


def test_task1():
    from Core import Task

    def func1(callback):
        callback.get("setStatus", empty)("Func1")
        n = 2**32
        callback.get("setMax", empty)(n)
        for i in range(n):
            print(i)
            callback.get("setProgress", empty)(i)
            # time.sleep(2)

    def func2(callback):
        callback.get("setStatus", empty)("Func2")
        n = 10000
        callback.get("setMax", empty)(n)
        for i in range(n):
            print(i)
            callback.get("setProgress", empty)(i)
            # time.sleep(2)

    a = Task("Test1", taskfunc=func1)
    a.start()
    b = Task("Test1_1", taskfunc=func2)
    b.setParent(a)
    c = Task("Test1_2", taskfunc=func1, waittasks=[b])
    c.setParent(a)
    b.start()


def test_task2():
    from Core import Task

    def func1(callback):
        callback.get("setStatus", empty)("Func1")
        n = 2**32
        callback.get("setMax", empty)(n)
        for i in range(n):
            print(i)
            callback.get("setProgress", empty)(i)
            if i >= 1000:
                raise Exception("Exception from test_task2")
            # time.sleep(2)

    def func2(callback):
        callback.get("setStatus", empty)("Func2")
        n = 2**32
        callback.get("setMax", empty)(n)
        for i in range(n):
            print(i)
            callback.get("setProgress", empty)(i)
            # time.sleep(2)

    a = Task("Test2", taskfunc=func2)
    b = Task("Test2_1", parent=a, taskfunc=func1)
    a.start()


def test_task3():
    from Core import Task

    def func1(callback):
        callback.get("setStatus", empty)("Func1")
        n = 300
        callback.get("setMax", empty)(n)
        for i in range(n):
            print(i)
            callback.get("setProgress", empty)(i)
            time.sleep(0.01)

    a = Task("Test3", taskfunc=func1)
    a.start()


def test_download1():
    from Core import Download, Task

    url = "https://authlib-injector.yushi.moe/artifact/52/authlib-injector-1.2.4.jar"
    task = Task(
        "test_download1",
        taskfunc=lambda callback: Download(
            url, "FMCL/Temp/test_download1.jar", callback=callback
        ).start(),
    )
    task.start()


def test_download2():
    from Core import Download, Task

    url = "https://issuecdn.baidupcs.com/issue/netdisk/yunguanjia/BaiduNetdisk_7.2.8.9.exe"
    task = Task(
        "test_download2",
        taskfunc=lambda callback: Download(
            url, "FMCL/Temp/test_download2.exe", callback=callback
        ).start(),
    )
    task.start()


def main():
    test_download2()
