from Kernel import Kernel
from PyQt5.QtCore import QFileInfo
from Setting import Setting

from . import Pages_rc as _

_translate = Kernel.translate


def getIndexes():
    lang = Setting().get("language.type")

    launcher = _translate("启动器")
    costomfunction = _translate("自定义功能")
    costomhelp = _translate("自定义帮助")
    default = {
        launcher: f":/简体中文/launcher/readme.md",
        f"{launcher}.{costomfunction}": f":/简体中文/launcher/customfunction.md",
        f"{launcher}.{costomhelp}": f":/简体中文/launcher/customhelp.md"
    }

    final = {}
    for key, val in default.items():
        new = val.replace("简体中文", lang)
        if QFileInfo(new).exists():
            final[key] = new
        else:
            final[key] = val
    return final
