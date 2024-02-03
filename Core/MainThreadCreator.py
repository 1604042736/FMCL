import time
import threading

from PyQt5.QtCore import QObject, pyqtSignal


class MainThreadCreator(QObject):
    """负责在主线程中创建对象"""

    __createObject = pyqtSignal(type, tuple, dict, str)

    instance = None
    new_count = 0

    def __new__(cls):
        if MainThreadCreator.instance == None:
            MainThreadCreator.instance = super().__new__(cls)
        MainThreadCreator.new_count += 1
        return MainThreadCreator.instance

    def __init__(self):
        if MainThreadCreator.new_count > 1:
            return
        super().__init__()
        self.created_obj = {}
        self.__createObject.connect(self.createObject)

    def createObject(self, cls, args, kwargs, hash):
        self.created_obj[hash] = cls(*args, **kwargs)

    def newObject(self, cls: type, args, kwargs):
        hash = f"{time.time()}{threading.get_ident()}"
        args = tuple(args)
        self.__createObject.emit(cls, args, kwargs, hash)
        while hash not in self.created_obj:
            time.sleep(0.005)
        return self.created_obj[hash]
