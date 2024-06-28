import json
import math
import os
import qtawesome as qta

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import qApp
from PyQt5.QtGui import QColor
from PyQt5.Qsci import QsciScintilla, QsciLexerJSON

from qfluentwidgets import TransparentToolButton

from Events import *


class JsonEditor(QsciScintilla):
    instances = {}
    new_count = {}

    def __new__(cls, json_path: str):
        if json_path not in JsonEditor.instances:
            JsonEditor.instances[json_path] = super().__new__(cls)
            JsonEditor.new_count[json_path] = 0
        JsonEditor.new_count[json_path] += 1
        return JsonEditor.instances[json_path]

    def __init__(self, json_path: str):
        if JsonEditor.new_count[json_path] > 1:
            return
        super().__init__()
        self.setWindowTitle(json_path)
        self.setWindowIcon(qta.icon("mdi.code-json"))

        self.setLexer(QsciLexerJSON())
        self.setIndentationGuides(True)  # 缩进提示
        self.setCaretLineVisible(True)  # 高亮当前行
        self.setIndentationsUseTabs(False)  # tab用空格代替
        self.setIndentationWidth(4)
        self.setTabWidth(4)  # 每个tab 4个空格
        self.setUtf8(True)
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.indicatorDefine(QsciScintilla.IndicatorStyle.SquiggleLowIndicator, 0)
        self.setIndicatorForegroundColor(QColor("red"), 0)
        self.setWrapMode(QsciScintilla.WrapMode.WrapCharacter)  # 环绕模式

        self.json_path = json_path

        self.pb_save = TransparentToolButton()
        self.pb_save.resize(46, 32)
        self.pb_save.setIcon(qta.icon("fa.save"))
        self.pb_save.clicked.connect(self.save)

        self.last_error = None
        self.textChanged.connect(self.check)

        self.setMouseTracking(True)

        self.load()

    def load(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, encoding="utf-8") as file:
                self.setText(file.read())

    def check(self):
        """
        检查json文本是否符合语法
        符合返回True, 否则返回False
        """
        code = self.text()
        self.setMarginWidth(0, "0" * (math.ceil(math.log10(len(code.split("\n")))) + 1))
        try:
            json.loads(code)
            if self.last_error != None:
                self.SendScintilla(QsciScintilla.SCI_INDICATORCLEARRANGE, 0, len(code))
            return True
        except json.JSONDecodeError as e:
            self.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, e.pos, 1)
            self.last_error = e
            return False

    def save(self):
        if self.check():
            open(self.json_path, mode="w", encoding="utf-8").write(self.text())

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_save, "right"))
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_save))
            self.pb_save.setParent(self)
        return super().event(a0)
