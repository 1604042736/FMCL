import os
import Ui.AllHelp.JoinWriteHelp as JoinWriteHelp
import Ui.AllHelp.CustomHelp as CustomHelp

allhelp = [JoinWriteHelp, CustomHelp]

try:
    for i in os.listdir("FMCL/Help"):
        if i.endswith(".py"):
            allhelp.append(f"FMCL.Help.{os.path.splitext(i)[0]}")
except:
    pass
