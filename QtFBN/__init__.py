"""
QtFBN,Qt Frameless but Native
有以下几种目的:
1.自定义标题栏
2.保留原生窗口特性
3.方便的管理软件中的窗口
"""
import Globals as g
from PyQt5.QtWidgets import QPushButton
import qtawesome as qta

manager = None  # 一个软件至多有一个QFBNWindowManager

# 窗口默认大小
winwidth = 1000
winheight = 618
# 以下下内容非必要(on_any_win_ready必要)


def on_any_win_ready(win) -> None:
    pass
