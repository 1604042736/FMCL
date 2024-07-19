import json
import os
from string import ascii_letters

from PyQt5.Qsci import QsciScintilla

from Setting import Setting
from .JsonEditor import JsonEditor


class SettingJsonEditor(JsonEditor):
    instances = {}
    new_count = {}

    def __new__(cls, setting: Setting):
        return super().__new__(cls, setting.setting_path)
        json_path = setting.setting_path
        if json_path not in SettingJsonEditor.instances:
            SettingJsonEditor.instances[json_path] = super().__new__(cls, json_path)
            SettingJsonEditor.new_count[json_path] = 0
        SettingJsonEditor.new_count[json_path] += 1
        return SettingJsonEditor.instances[json_path]

    def __init__(self, setting: Setting):
        if JsonEditor.new_count[setting.setting_path] > 1:
            return
        super().__init__(setting.setting_path)
        self.setting = setting

    def show(self, id=None):
        super().show()
        if id == None:
            return
        if not os.path.exists(self.json_path):
            return
        try:
            setting_json = json.load(open(self.json_path, encoding="utf-8"))
        except json.JSONDecodeError:
            setting_json = self.setting.modifiedsetting
        if id not in setting_json:
            if id not in self.setting:
                return
            setting_json[id] = self.setting[id]
        self.setText(
            json.dumps(
                setting_json,
                ensure_ascii=False,
                indent=4,
            )
        )
        self.SendScintilla(QsciScintilla.SCI_SETTARGETSTART, 0)
        self.SendScintilla(QsciScintilla.SCI_SETTARGETEND, self.length())
        self.SendScintilla(
            QsciScintilla.SCI_SETSEARCHFLAGS, QsciScintilla.SCFIND_WHOLEWORD
        )
        self.SendScintilla(
            QsciScintilla.SCI_SETWORDCHARS,
            (ascii_letters + ".").encode("utf-8"),
        )
        pos = self.SendScintilla(
            QsciScintilla.SCI_SEARCHINTARGET, len(id), id.encode("utf-8")
        )
        line, index = self.lineIndexFromPosition(pos)
        self.setCursorPosition(line, index)
        self.setSelection(line, index, line, index + len(id))
