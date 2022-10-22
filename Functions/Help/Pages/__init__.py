from PyQt5.QtCore import QCoreApplication, QFileInfo
from System import Setting

from . import Pages_rc as _

_translate = QCoreApplication.translate


def getIndexes():
    lang_file = Setting().get("launcher.language").replace("\\", "/")
    lang = lang_file.split("/")[-1].replace(".qm", "")
    default = {
        _translate("Pages", "启动器"): f":/zh_CN/launcher/README.md"
    }

    final = {}
    for key, val in default.items():
        new = val.replace("zh_CN", lang)
        if QFileInfo(new).exists():
            final[key] = new
        else:
            final[key] = val
    return final