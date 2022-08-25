import os
import Ui.AllHelp.CustomTranslate as CustomTranslate
import Ui.AllHelp.JoinTranslate as JoinTranslate
import Ui.AllHelp.JoinWriteHelp as JoinWriteHelp
import Ui.AllHelp.CustomHelp as CustomHelp
import Ui.AllHelp.CustomFunction as CustomFunction

allhelp = [JoinWriteHelp, CustomHelp,
           JoinTranslate, CustomTranslate, CustomFunction]

try:
    for i in os.listdir("FMCL/Help"):
        if i != "__init__.py" and i.endswith(".py"):
            allhelp.append(f"FMCL.Help.{os.path.splitext(i)[0]}")
    if not os.path.exists("FMCL/__init__.py"):
        with open("FMCL/__init__.py", "w", encoding='utf-8'):
            pass
    if not os.path.exists("FMCL/Help/__init__.py"):
        with open("FMCL/Help/__init__.py", "w", encoding='utf-8'):
            pass
except:
    pass
