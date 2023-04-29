from PyQt5.QtCore import QCoreApplication, QFileInfo
from Setting import Setting
from . import Pages_rc as _
from Kernel import Kernel
_translate = Kernel.translate


def getIndexes():
    lang_file = Setting().get("launcher.language").replace("\\", "/")
    lang = lang_file.split("/")[-1].replace(".qm", "")

    launcher = _translate("启动器")
    costomfunction = _translate("自定义功能")
    costomhelp = _translate("自定义帮助")
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
    return final
