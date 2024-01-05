from PyQt5.QtCore import QCoreApplication

from Kernel import Kernel

from .ui_Developer import Ui_Developer
from .ui_CustomFunction import Ui_CustomFunction
from .ui_CustomHelp import Ui_CustomHelp
from .ui_Translation import Ui_Translation

_translate = QCoreApplication.translate


def helpIndex():
    return {
        "developer": {
            "name": _translate("DeveloperHelp", "开发者"),
            "page": lambda: Kernel.getWidgetFromUi(Ui_Developer),
            "customfunction": {
                "name": _translate("DeveloperHelp", "自定义功能"),
                "page": lambda: Kernel.getWidgetFromUi(Ui_CustomFunction),
            },
            "customhelp": {
                "name": _translate("DeveloperHelp", "自定义帮助"),
                "page": lambda: Kernel.getWidgetFromUi(Ui_CustomHelp),
            },
            "translation": {
                "name": _translate("DeveloperHelp", "翻译"),
                "page": lambda: Kernel.getWidgetFromUi(Ui_Translation),
            },
        }
    }
