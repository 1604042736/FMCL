import logging
import os
from importlib import import_module

from PyQt5.QtCore import QCoreApplication, QFileInfo
from System import Setting

from . import Pages_rc as _

_translate = QCoreApplication.translate


def getIndexes():
    lang_file = Setting().get("launcher.language").replace("\\", "/")
    lang = lang_file.split("/")[-1].replace(".qm", "")

    launcher = _translate("Pages", "启动器")
    costomfunction = _translate("Pages", "自定义功能")
    costomhelp = _translate("Pages", "自定义帮助")
    default = {
        launcher: f":/zh_CN/launcher/readme.md",
        f"{launcher}.{costomfunction}": f":/zh_CN/launcher/customfunction.md",
        f"{launcher}.{costomhelp}": f":/zh_CN/launcher/customhelp.md"
    }

    final = {}
    for key, val in default.items():
        new = val.replace("zh_CN", lang)
        if QFileInfo(new).exists():
            final[key] = new
        else:
            final[key] = val

    if os.path.exists("FMCL/Help"):
        module = import_module("FMCL.Help")
        try:
            final |= module.__dict__["getIndexes"](lang)
        except Exception as e:
            logging.error(f"加载自定义帮助失败: {e}")
    return final
